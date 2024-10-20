from __future__ import annotations

from abc import ABC

from helloworld.account.features.device.data import DeviceRepository
from helloworld.account.features.device import DeviceEntity
from helloworld.core import BaseUseCaseUnitOfWork

class InstallUseCase(BaseUseCaseUnitOfWork[DeviceEntity, DeviceEntity], ABC):
    async def execute(self, device: DeviceEntity) -> DeviceEntity | None:
        raise NotImplementedError

class InstallUseCaseImpl(InstallUseCase):
    async def execute(self, device: DeviceEntity) -> DeviceEntity | None:
        async with self.unit_of_work as unit_of_work:
            device_repository: DeviceRepository = await unit_of_work.repository_factory.instance(DeviceRepository)

            device.id = DeviceEntity.new_id()
            await device_repository.create(entity=device)

            return device