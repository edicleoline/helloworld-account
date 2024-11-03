from __future__ import annotations

from abc import ABC
from typing import List, Tuple

from helloworld.account.features.device.data.repositories.device_repository import DeviceRepository
from helloworld.account.features.device_verifier.data import DeviceVerificationRepository
from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.account.features.device import DeviceEntity

class DeviceByVerifiedPhoneUseCase(BaseUseCaseUnitOfWork[Tuple[int, List[int]], DeviceEntity], ABC):
    async def execute(self, target_id: int, not_in: List[int] | None) -> DeviceEntity | None:
        raise NotImplementedError

class DeviceByVerifiedPhoneUseCaseImpl(DeviceByVerifiedPhoneUseCase):
    async def execute(self, target_id: int, not_in: List[int] | None) -> DeviceEntity | None:
        async with self.unit_of_work as unit_of_work:
            device_verification_repository: DeviceVerificationRepository = await unit_of_work.repository_factory\
                .instance(DeviceVerificationRepository)

            phone_verification_entities = await device_verification_repository.filter(target_id=target_id)

            if not phone_verification_entities: return None

            device_verifications = [
                entity for entity in phone_verification_entities
                if entity.verified_at and entity.device_id not in not_in
            ]

            if not device_verifications: return None

            device_verification = device_verifications[-1]

            device_repository: DeviceRepository = await unit_of_work.repository_factory.instance(DeviceRepository)
            device_entity = await device_repository.find(id=device_verification.device_id)

            return device_entity


