from __future__ import annotations

import re
from abc import ABC

from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.account.features.phone import PhoneEntity
from helloworld.account.features.phone.data import PhoneRepository
from helloworld.core.error.exceptions import ArgumentError


class FindOrCreateUseCase(BaseUseCaseUnitOfWork[str, PhoneEntity], ABC):
    async def execute(self, phone_number: str) -> PhoneEntity:
        raise NotImplementedError

class FindOrCreateUseCaseImpl(FindOrCreateUseCase):
    async def execute(self, phone_number: str) -> PhoneEntity:
        async with self.unit_of_work as unit_of_work:
            phone_repository: PhoneRepository = await unit_of_work.repository_factory.instance(PhoneRepository)

            phone_number = re.sub(r'[^\d+]', '', phone_number)

            if not phone_number:
                raise ArgumentError("Invalid phone number.")

            phone_entity = await phone_repository.find(phone_number=phone_number)

            if not phone_entity:
                phone_entity = PhoneEntity(phone_number=phone_number)
                phone_entity = await phone_repository.save(entity=phone_entity)

            return phone_entity