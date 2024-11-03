from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.account.features.device import DeviceEntity
from helloworld.account.features.device.data import DeviceRepository
from helloworld.core.infra.data.sqlalchemy import BaseRepository
from .device_model import DeviceModel

class DeviceRepositoryImpl(DeviceRepository, BaseRepository[DeviceEntity, DeviceModel]):
    def __init__(self, session: AsyncSession, authorization: str | None = None):
        super().__init__(session=session, model_cls=DeviceModel, authorization=authorization)

    async def find(self, id: str) -> DeviceEntity | None:
        return await self._find(id=id)