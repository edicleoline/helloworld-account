from __future__ import annotations

from abc import ABC

from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.account.features.user import UserEntity
from helloworld.account.features.user.data import UserRepository
from helloworld.auth.jwt.services import TokenService
from helloworld.auth.error import exceptions

class MeUseCase(BaseUseCaseUnitOfWork[str, UserEntity], ABC):
    async def execute(self, **kwargs) -> UserEntity | None:
        raise NotImplementedError

class MeUseCaseImpl(MeUseCase):
    async def execute(self, **kwargs) -> UserEntity | None:
        async with self.unit_of_work as unit_of_work:
            token_service: TokenService = await self.services.get("authentication", "token")
            decoded_token = await token_service.decode(self.authorization)

            if not decoded_token or not decoded_token.get("sub"):
                raise exceptions.InvalidTokenError(f"Invalid token {self.authorization}.")

            sub = decoded_token.get("sub")

            user_repository: UserRepository = await unit_of_work.repository_factory.instance(UserRepository)
            user: UserEntity = await user_repository.find(identity_id=sub)

            return user
