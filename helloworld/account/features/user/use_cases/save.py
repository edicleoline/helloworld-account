from __future__ import annotations

from abc import ABC
from typing import Optional

from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.account.features.user import UserEntity
from helloworld.account.features.user.data import UserRepository

class SaveUseCase(BaseUseCaseUnitOfWork[UserEntity, UserEntity], ABC):
    async def execute(self, user: UserEntity) -> Optional[UserEntity]:
        raise NotImplementedError

class SaveUseCaseImpl(SaveUseCase):
    async def execute(self, user: UserEntity) -> Optional[UserEntity]:
        async with self.unit_of_work as unit_of_work:
            user_repository: UserRepository = await unit_of_work.repository_factory.instance(UserRepository)
            saved_user = await user_repository.save(user)
            return saved_user