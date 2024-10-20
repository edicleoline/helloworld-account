from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.account.features.phone_verifier import PhoneVerificationEntity
from helloworld.account.features.phone_verifier.data import PhoneVerificationRepository
from helloworld.core.infra.data.sqlalchemy import BaseRepository
from .phone_verification_model import PhoneVerificationModel

class PhoneVerificationRepositoryImpl(PhoneVerificationRepository, BaseRepository[PhoneVerificationEntity, PhoneVerificationModel]):
    def __init__(self, session: AsyncSession, authorization: str | None = None):
        super().__init__(session=session, model_cls=PhoneVerificationModel, authorization=authorization)

    async def find(self, id: int) -> PhoneVerificationEntity | None:
        return await self._find(id=id)