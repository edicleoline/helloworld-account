from __future__ import annotations

from abc import ABC

from helloworld.core.data import AbstractRepository, TModel
from helloworld.account.features.phone_verifier import PhoneVerificationEntity

class PhoneVerificationRepository(AbstractRepository[PhoneVerificationEntity, TModel], ABC):
    async def find(self, id: int) -> PhoneVerificationEntity | None: ...
