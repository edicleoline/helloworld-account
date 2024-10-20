from __future__ import annotations

from abc import ABC
from typing import overload

from helloworld.core.data import AbstractRepository, TModel
from helloworld.account.features.phone import PhoneEntity

class PhoneRepository(AbstractRepository[PhoneEntity, TModel], ABC):
    @overload
    async def find(self, phone_number: str) -> PhoneEntity | None: ...

    @overload
    async def find(self, id: int) -> PhoneEntity | None: ...

    async def find(self, **kwargs) -> PhoneEntity | None: ...
