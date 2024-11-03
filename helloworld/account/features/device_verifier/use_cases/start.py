from __future__ import annotations

from abc import ABC
import random
from datetime import datetime, timezone

from helloworld.account.features.device_verifier.data import DeviceVerificationRepository
from helloworld.auth.features.otp.data import OTPRequestLimitRepository
from helloworld.auth.features.otp.entities.otp_request_limit_entity import OTPRequestLimitEntity
from helloworld.account.features.device_verifier.entities.device_verification_entity import DeviceVerificationEntity
from helloworld.account.features.device_verifier.use_cases.device_by_verified_phone import DeviceByVerifiedPhoneUseCase
from helloworld.account.features.device_verifier.utils import can_request_otp
from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.account.features.phone.data import PhoneRepository
from helloworld.account.features.device_verifier import DeviceVerifierStartEntity, StartUseCaseRequest
from helloworld.account.features.device_verifier.types import VerificationType
from helloworld.core.error import exceptions as core_exceptions
from helloworld.auth.features.device_otp import DeviceOTPRequestEntity, OTPType
from helloworld.auth.features.device_otp.use_cases.send import SendUseCase
from helloworld.core.phoning.services import PhoneService
from helloworld.auth.features.otp.use_cases import GenerateUseCase
from helloworld.core.util.security import generate_otp
from helloworld.account.features.device.data import DeviceRepository

def calculate_cooldown(attempt_count: int, base_cooldown: int = 60) -> int:
    max_cooldown = 3600 * 48
    if attempt_count < 5:
        cooldown_seconds = base_cooldown * (2 ** attempt_count)
    else:
        cooldown_seconds = base_cooldown * 10 * (2 ** (attempt_count - 5))

    return min(cooldown_seconds, max_cooldown)

class StartUseCase(BaseUseCaseUnitOfWork[StartUseCaseRequest, DeviceVerifierStartEntity], ABC):
    async def execute(self, request: StartUseCaseRequest) -> DeviceVerifierStartEntity | None:
        raise NotImplementedError

class StartUseCaseImpl(StartUseCase):
    async def execute(self, request: StartUseCaseRequest) -> DeviceVerifierStartEntity | None:
        async with self.unit_of_work as unit_of_work:
            verification_type: VerificationType = VerificationType.PHONE if request.otp_type in [OTPType.SMS, OTPType.CALL,
                                                                                                 OTPType.MISSED_CALL] else None
            verification_type = VerificationType.DEVICE if request.otp_type in [OTPType.APP] else verification_type
            verification_type = VerificationType.EMAIL if request.otp_type in [OTPType.EMAIL] else verification_type

            if not verification_type:
                raise core_exceptions.InvalidRequestError

            device_repository: DeviceRepository = await unit_of_work.repository_factory.instance(DeviceRepository)
            device_entity = await device_repository.find(id=request.device_id)

            if not device_entity:
                raise core_exceptions.InvalidRequestError

            phone_repository: PhoneRepository = await unit_of_work.repository_factory.instance(PhoneRepository)
            phone_entity = await phone_repository.find(id=request.target_id) if verification_type == VerificationType.PHONE else None

            target_id = request.target_id if not verification_type == VerificationType.DEVICE else device_entity.id

            otp_request_limit_repository: OTPRequestLimitRepository = await unit_of_work.repository_factory.instance(OTPRequestLimitRepository)

            otp_request_limit_entity = await otp_request_limit_repository.find(
                device_id=device_entity.id,
                method=request.otp_type.value,
                target_id=target_id
            )

            otp_request_limits = await otp_request_limit_repository.filter(device_id=device_entity.id)
            total_attempt_count = sum(otp_request_limit.attempt_count for otp_request_limit in otp_request_limits)

            if not otp_request_limit_entity:
                otp_request_limit_entity = OTPRequestLimitEntity(
                    device_id=device_entity.id,
                    target_id=target_id,
                    method=request.otp_type.value,
                    attempt_count=0,
                    cooldown_seconds=60,
                    last_request_at=datetime.now(timezone.utc)
                )

            if otp_request_limit_entity.id and not can_request_otp(otp_request_limit_entity.last_request_at, otp_request_limit_entity.cooldown_seconds):
                raise core_exceptions.OTPRequestLimitError

            otp_request_limit_entity.last_request_at = datetime.now(timezone.utc)
            otp_request_limit_entity.cooldown_seconds = calculate_cooldown(total_attempt_count)
            otp_request_limit_entity.attempt_count = otp_request_limit_entity.attempt_count + 1

            await otp_request_limit_repository.save(otp_request_limit_entity)

            device_verification_repository: DeviceVerificationRepository = await unit_of_work.repository_factory.instance(DeviceVerificationRepository)

            otp_generate_use_case: GenerateUseCase = await unit_of_work.use_case_factory.instance(GenerateUseCase)

            code = generate_otp(random.choice([4, 6]))
            otp_req_entity = await otp_generate_use_case.execute(data={}, code=code)

            send_use_case: SendUseCase = await unit_of_work.use_case_factory.instance(SendUseCase)

            device_otp_req_entity = DeviceOTPRequestEntity(
                otp_type=request.otp_type,
                code=otp_req_entity.code,
                phone_number=phone_entity.phone_number if phone_entity else None,
                priority="critical",
                template="otp",
                lang="en"
            )
            await send_use_case.execute(request=device_otp_req_entity)

            device_verification_id = DeviceVerificationEntity.new_id()

            device_verification_entity = DeviceVerificationEntity(
                id=device_verification_id,
                device_id=device_entity.id,
                verification_type=verification_type.value,
                method=request.otp_type.value,
                target_id=target_id,
                otp_request_id=otp_req_entity.id,
            )

            await device_verification_repository.create(entity=device_verification_entity)

            phone_service: PhoneService = await self.services.get("phoning", "main")
            phone_number = phone_service.format_number_and_mask(phone_entity.phone_number) if phone_entity else None

            device_by_verified_phone_use_case: DeviceByVerifiedPhoneUseCase = await unit_of_work.use_case_factory\
                .instance(DeviceByVerifiedPhoneUseCase)

            verified_device_entity = await device_by_verified_phone_use_case\
                .execute(target_id=request.target_id, not_in=[device_entity.id])

            return DeviceVerifierStartEntity(
                target_id=target_id,
                method=request.otp_type.value,
                token = otp_req_entity.token,
                otp_code_len=len(str(otp_req_entity.code)) if request.otp_type is not OTPType.MISSED_CALL else None,
                params={
                    "device": verified_device_entity.name if verified_device_entity else None,
                    "phone_number": phone_number
                }
            )

