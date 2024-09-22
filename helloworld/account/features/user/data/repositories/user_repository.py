from __future__ import annotations

from abc import ABC

from helloworld.core.data import AbstractRepository, TModel
from helloworld.account.features.user import UserEntity

class UserRepository(AbstractRepository[UserEntity, TModel], ABC):
    async def find(self, identity_id: str) -> UserEntity | None: ...
