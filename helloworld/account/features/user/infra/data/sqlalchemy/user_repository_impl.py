from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.account.features.user import UserEntity
from helloworld.account.features.user.data import UserRepository
from helloworld.core.infra.data.sqlalchemy import BaseRepository
from .user_model import UserModel

class UserRepositoryImpl(UserRepository, BaseRepository[UserEntity, UserModel]):
    def __init__(self, session: AsyncSession, authorization: str | None = None):
        super().__init__(session=session, model_cls=UserModel, authorization=authorization)

    async def find(self, identity_id: str) -> UserEntity | None:
        return await self._find(identity_id=identity_id)