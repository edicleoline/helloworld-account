from __future__ import annotations

from abc import ABC
from typing import Optional, overload

from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.account.features.user import UserEntity
from helloworld.account.features.user.data import UserRepository

class FindUseCase(BaseUseCaseUnitOfWork[dict, UserEntity], ABC):
    async def execute(self, **kwargs) -> Optional[UserEntity]:
        raise NotImplementedError

class FindUseCaseImpl(FindUseCase):
    @overload
    async def execute(self, id: str) -> Optional[UserEntity]:...

    async def execute(self, **kwargs) -> Optional[UserEntity]:
        async with self.unit_of_work as unit_of_work:
            user_repository: UserRepository = await unit_of_work.repository_factory.create(UserRepository)
            return await user_repository.find(**kwargs)
