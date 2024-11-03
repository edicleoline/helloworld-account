from __future__ import annotations

from abc import ABC
from typing import Sequence, Tuple, List

from helloworld.account.features.phone.data import PhoneRepository
from helloworld.account.features.device_verifier import MethodEntity
from helloworld.auth.features.otp.data import OTPRequestLimitRepository
from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.core.error.exceptions import ArgumentError
from helloworld.core.phoning.services import PhoneService
from helloworld.auth.features.device_otp.types import OTPType
from helloworld.account.features.device_verifier.use_cases.device_by_verified_phone import DeviceByVerifiedPhoneUseCase

class MethodsUseCase(BaseUseCaseUnitOfWork[Tuple[int, int], Sequence[MethodEntity]], ABC):
    async def execute(self, device_id: int, target_id: int) -> Sequence[MethodEntity]:
        raise NotImplementedError

class MethodsUseCaseImpl(MethodsUseCase):
    async def execute(self, device_id: int, target_id: int) -> Sequence[MethodEntity]:
        async with self.unit_of_work as unit_of_work:
            phone_repository: PhoneRepository = await unit_of_work.repository_factory.instance(PhoneRepository)

            phone_entity = await phone_repository.find(id=target_id)

            if not phone_entity:
                raise ArgumentError

            phone_service: PhoneService = await self.services.get("phoning", "main")
            phone_number = phone_service.format_number_and_mask(phone_entity.phone_number)

            methods: List[MethodEntity] = []

            device_by_verified_phone_use_case: DeviceByVerifiedPhoneUseCase = await unit_of_work.use_case_factory.instance(
                DeviceByVerifiedPhoneUseCase)

            verified_device_entity = await device_by_verified_phone_use_case.execute(target_id=target_id, not_in=[device_id])

            if verified_device_entity:
                methods.append(MethodEntity(
                    key=OTPType.APP.value,
                    title="Try again in other device",
                    label="Receive the code on device {{model}}",
                    params={"model": verified_device_entity.name},
                    icon='<svg xmlns="http://www.w3.org/2000/svg" stroke="currentColor" viewBox="0 0 512 512">'
                         '<rect x="128" y="16" width="256" height="480" rx="48" ry="48" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke-width="32"></rect><path d="M176 16h24a8 8 0 018 8h0a16 16 0 0016 16h64a16 16 0 0016-16h0a8 8 0 018-8h24" stroke-linecap="round" stroke-linejoin="round" cfill="none" stroke-width="32"></path></svg>'
                ))

            methods += [
                MethodEntity(
                    key=OTPType.SMS.value,
                    title="Resend SMS",
                    label="Receive the code at the number {{phone}}",
                    params={"phone": phone_number},
                    icon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" stroke="currentColor">'
                         '<path d="M408 64H104a56.16 56.16 0 00-56 56v192a56.16 56.16 0 0056 56h40v80l93.72-78.14a8 8 0 015.13-1.86H408a56.16 56.16 0 0056-56V120a56.16 56.16 0 00-56-56z" stroke-linejoin="round" fill="none" stroke-width="32"></path>'
                         '<circle cx="160" cy="216" r="32" fill="currentColor"></circle>'
                         '<circle cx="256" cy="216" r="32" fill="currentColor"></circle>'
                         '<circle cx="352" cy="216" r="32" fill="currentColor"></circle></svg>'
                ),
                MethodEntity(
                    key=OTPType.CALL.value,
                    title="Voice call",
                    label="Receive the code at the number {{phone}}",
                    params={"phone": phone_number},
                    icon='<svg xmlns="http://www.w3.org/2000/svg" stroke="currentColor" viewBox="0 0 512 512">'
                         '<path d="M451 374c-15.88-16-54.34-39.35-73-48.76-24.3-12.24-26.3-13.24-45.4.95-12.74 9.47-21.21 17.93-36.12 14.75s-47.31-21.11-75.68-49.39-47.34-61.62-50.53-76.48 5.41-23.23 14.79-36c13.22-18 12.22-21 .92-45.3-8.81-18.9-32.84-57-48.9-72.8C119.9 44 119.9 47 108.83 51.6A160.15 160.15 0 0083 65.37C67 76 58.12 84.83 51.91 98.1s-9 44.38 23.07 102.64 54.57 88.05 101.14 134.49S258.5 406.64 310.85 436c64.76 36.27 89.6 29.2 102.91 23s22.18-15 32.83-31a159.09 159.09 0 0013.8-25.8C465 391.17 468 391.17 451 374z" stroke-miterlimit="10" fill="none" stroke-width="32"></path></svg>'
                ),
                MethodEntity(
                    key=OTPType.MISSED_CALL.value,
                    title="Missed call",
                    label="Automatic confirmation for the number {{phone}}",
                    params={"phone": phone_number},
                    icon='<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24" fill="currentColor"><path d="M0 0h24v24H0z" fill="none"/><path d="M19.59 7L12 14.59 6.41 9H11V7H3v8h2v-4.59l7 7 9-9z"/></svg>'
                ),
            ]

            otp_request_limit_repository: OTPRequestLimitRepository = await unit_of_work.repository_factory.instance(
                OTPRequestLimitRepository)

            for method in methods:
                otp_request_limit_entity = await otp_request_limit_repository.last(device_id=device_id, method=method.key)

                if otp_request_limit_entity:
                    method.last_request_at = otp_request_limit_entity.last_request_at
                    method.attempt_count = otp_request_limit_entity.attempt_count
                    method.cooldown_seconds = otp_request_limit_entity.cooldown_seconds
                else:
                    method.last_request_at = None
                    method.attempt_count = 0
                    method.cooldown_seconds = 0

            return methods