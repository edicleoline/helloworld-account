from __future__ import annotations

from abc import ABC

from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.account.features.user.data import UserRepository

class DeleteUseCase(BaseUseCaseUnitOfWork[str, None], ABC):
    async def execute(self, user_id: str) -> None:
        raise NotImplementedError

class DeleteUseCaseImpl(DeleteUseCase):
    async def execute(self, user_id: str) -> None:
        async with self.unit_of_work as unit_of_work:
            user_repository: UserRepository = await unit_of_work.repository_factory.create(UserRepository)
            await user_repository.delete(user_id)
