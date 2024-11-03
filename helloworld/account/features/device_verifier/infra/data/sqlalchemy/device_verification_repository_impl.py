from __future__ import annotations

from typing import List, overload
from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.account.features.device_verifier import DeviceVerificationEntity
from helloworld.account.features.device_verifier.data import DeviceVerificationRepository
from helloworld.core.infra.data.sqlalchemy import BaseRepository
from .device_verification_model import PhoneVerificationModel

class DeviceVerificationRepositoryImpl(DeviceVerificationRepository, BaseRepository[DeviceVerificationEntity, PhoneVerificationModel]):
    def __init__(self, session: AsyncSession, authorization: str | None = None):
        super().__init__(session=session, model_cls=PhoneVerificationModel, authorization=authorization)

    @overload
    async def find(self, id: int) -> DeviceVerificationEntity | None: ...

    @overload
    async def find(self, otp_request_id: int) -> DeviceVerificationEntity | None: ...

    async def find(self, **kwargs) -> DeviceVerificationEntity | None:
        if 'id' in kwargs:
            return await self._find(id=kwargs['id'])
        elif 'otp_request_id' in kwargs:
            return await self._find(otp_request_id=kwargs['otp_request_id'])
        return None

    async def filter(self, target_id: int) -> List[DeviceVerificationEntity]:
        return await BaseRepository.filter(self, target_id=target_id)