from __future__ import annotations

from abc import ABC
from typing import List

from helloworld.core.data import AbstractRepository, TModel
from helloworld.account.features.phone_verifier import OTPRequestLimitEntity

class OTPRequestLimitRepository(AbstractRepository[OTPRequestLimitEntity, TModel], ABC):
    async def find(self, device_id: int, method: str, phone_id: int) -> OTPRequestLimitEntity | None: ...

    async def filter(self, device_id: int) -> List[OTPRequestLimitEntity]: ...

    async def last(self, device_id: int, method: str) -> OTPRequestLimitEntity | None: ...
