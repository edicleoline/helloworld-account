from __future__ import annotations

import re
from abc import ABC
from datetime import datetime

from helloworld.account.features.phone_verifier.data import PhoneVerificationRepository
from helloworld.account.features.phone_verifier.data import OTPRequestLimitRepository
from helloworld.account.features.phone_verifier.entities.otp_request_limit_entity import OTPRequestLimitEntity
from helloworld.account.features.phone_verifier.entities.phone_verification_entity import PhoneVerificationEntity
from helloworld.account.features.phone_verifier.utils import can_request_otp
from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.core.util.security import generate_otp
from helloworld.account.features.phone.data import PhoneRepository
from helloworld.account.features.phone_verifier import PhoneVerifierStartEntity
from helloworld.core.error import exceptions as core_exceptions
from helloworld.auth.jwt.services import AbstractService

import pytz

def calculate_cooldown(attempt_count: int, base_cooldown: int = 60) -> int:
    max_cooldown = 3600 * 48
    if attempt_count < 5:
        cooldown_seconds = base_cooldown * (2 ** attempt_count)
    else:
        cooldown_seconds = base_cooldown * 10 * (2 ** (attempt_count - 5))

    return min(cooldown_seconds, max_cooldown)

class StartUseCase(BaseUseCaseUnitOfWork[dict, PhoneVerifierStartEntity], ABC):
    async def execute(self, phone_id: int, device_id: int, method: str) -> PhoneVerifierStartEntity | None:
        raise NotImplementedError

class StartUseCaseImpl(StartUseCase):
    async def execute(self, phone_id: int, device_id: int, method: str) -> PhoneVerifierStartEntity | None:
        async with self.unit_of_work as unit_of_work:
            phone_repository: PhoneRepository = await unit_of_work.repository_factory.instance(PhoneRepository)

            phone_entity = await phone_repository.find(id=phone_id)

            otp_request_limit_repository: OTPRequestLimitRepository = await unit_of_work.repository_factory.instance(OTPRequestLimitRepository)

            otp_request_limit_entity = await otp_request_limit_repository.find(device_id=device_id, method=method, phone_id=phone_id)

            otp_request_limits = await otp_request_limit_repository.filter(device_id=device_id)
            total_attempt_count = sum(otp_request_limit.attempt_count for otp_request_limit in otp_request_limits)

            if not otp_request_limit_entity:
                otp_request_limit_entity = OTPRequestLimitEntity(
                    device_id=device_id,
                    phone_id=phone_entity.id,
                    method=method,
                    attempt_count=0,
                    cooldown_seconds=60,
                    last_request_at=datetime.now(pytz.utc)
                )

            if otp_request_limit_entity.id and not can_request_otp(otp_request_limit_entity.last_request_at, otp_request_limit_entity.cooldown_seconds):
                raise core_exceptions.OTPRequestLimitError

            otp_request_limit_entity.last_request_at = datetime.now(pytz.utc)
            otp_request_limit_entity.cooldown_seconds = calculate_cooldown(total_attempt_count)
            otp_request_limit_entity.attempt_count = otp_request_limit_entity.attempt_count + 1

            otp_request_limit_entity = await otp_request_limit_repository.save(otp_request_limit_entity)

            phone_verification_repository: PhoneVerificationRepository = await unit_of_work.repository_factory.instance(PhoneVerificationRepository)

            token_service: AbstractService = await self.services.get("authentication", "otp-token")

            phone_verification_id = PhoneVerificationEntity.new_id()

            token_data = { "sub": phone_verification_id }
            token = await token_service.encode(token_data)

            otp_code = generate_otp()

            verification_entity = PhoneVerificationEntity(
                id=phone_verification_id,
                phone_id=phone_entity.id,
                token=token,
                otp_code=otp_code,
                method=method,
                device_id=device_id
            )

            await phone_verification_repository.create(entity=verification_entity)

            return PhoneVerifierStartEntity(
                phone_id=phone_entity.id,
                method=method,
                token = token,
                otp_code_len=len(otp_code),
            )