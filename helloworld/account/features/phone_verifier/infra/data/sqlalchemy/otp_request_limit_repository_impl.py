from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.account.features.phone_verifier import OTPRequestLimitEntity
from helloworld.account.features.phone_verifier.data import OTPRequestLimitRepository
from helloworld.core.infra.data.sqlalchemy import BaseRepository
from .otp_request_limit_model import OTPRequestLimitModel

from sqlalchemy import select

class OTPRequestLimitRepositoryImpl(OTPRequestLimitRepository, BaseRepository[List[OTPRequestLimitEntity], OTPRequestLimitModel]):
    def __init__(self, session: AsyncSession, authorization: str | None = None):
        super().__init__(session=session, model_cls=OTPRequestLimitModel, authorization=authorization)

    async def find(self, device_id: int, method: str, phone_id: int) -> List[OTPRequestLimitEntity]:
        return await self._find_criteria(criteria="and", device_id=device_id, method=method, phone_id=phone_id)

    async def filter(self, device_id: int) -> List[OTPRequestLimitEntity]:
        stmt = select(self.model_cls).filter_by(device_id=device_id)
        result = await self.session.execute(stmt)
        return [model.to_entity() for model in result.scalars()]

    async def last(self, device_id: int, method: str) -> OTPRequestLimitEntity | None:
        time_limit = datetime.now(timezone.utc) - timedelta(hours=48)

        stmt = (select(self.model_cls)
                .filter_by(device_id=device_id, method=method)
                .filter(self.model_cls.last_request_at >= time_limit)
                .order_by(self.model_cls.last_request_at.desc())
                .limit(1))

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()