from __future__ import annotations

from abc import ABC
from typing import Sequence

from helloworld.account.features.phone_verifier import MethodEntity
from helloworld.account.features.phone_verifier.data import OTPRequestLimitRepository
from helloworld.core import BaseUseCaseUnitOfWork

class MethodsUseCase(BaseUseCaseUnitOfWork[int, Sequence[MethodEntity]], ABC):
    async def execute(self, device_id: int) -> Sequence[MethodEntity]:
        raise NotImplementedError

class MethodsUseCaseImpl(MethodsUseCase):
    async def execute(self, device_id: int) -> Sequence[MethodEntity]:
        async with self.unit_of_work as unit_of_work:
            methods: list[MethodEntity] = []

            keys = ["sms", "call", "call_missed"]

            otp_request_limit_repository: OTPRequestLimitRepository = await unit_of_work.repository_factory.instance(
                OTPRequestLimitRepository)

            for key in keys:
                otp_request_limit_entity = await otp_request_limit_repository.last(device_id=device_id, method=key)

                if otp_request_limit_entity:
                    methods.append(MethodEntity(
                        id=otp_request_limit_entity.id,
                        method=key,
                        last_request_at=otp_request_limit_entity.last_request_at,
                        attempt_count=otp_request_limit_entity.attempt_count,
                        cooldown_seconds=otp_request_limit_entity.cooldown_seconds))

            return methods