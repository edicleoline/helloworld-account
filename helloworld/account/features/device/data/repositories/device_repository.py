from __future__ import annotations

from abc import ABC

from helloworld.core.data import AbstractRepository, TModel
from helloworld.account.features.device import DeviceEntity

class DeviceRepository(AbstractRepository[DeviceEntity, TModel], ABC):
    async def find(self, id: str) -> DeviceEntity | None: ...
