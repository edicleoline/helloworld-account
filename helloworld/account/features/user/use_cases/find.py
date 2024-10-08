from __future__ import annotations

from abc import ABC
from typing import overload

from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.account.features.user import UserEntity
from helloworld.account.features.user.data import UserRepository

class FindUseCase(BaseUseCaseUnitOfWork[dict, UserEntity], ABC):
    async def execute(self, **kwargs) -> UserEntity | None:
        raise NotImplementedError

class FindUseCaseImpl(FindUseCase):
    @overload
    async def execute(self, id: str) -> UserEntity | None:...

    async def execute(self, **kwargs) -> UserEntity | None:
        async with self.unit_of_work as unit_of_work:
            user_repository: UserRepository = await unit_of_work.repository_factory.instance(UserRepository)
            return await user_repository.find(**kwargs)
