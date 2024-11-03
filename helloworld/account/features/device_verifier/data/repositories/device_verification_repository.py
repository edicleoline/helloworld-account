from __future__ import annotations

from abc import ABC
from typing import List, overload

from helloworld.core.data import AbstractRepository, TModel
from helloworld.account.features.device_verifier import DeviceVerificationEntity

class DeviceVerificationRepository(AbstractRepository[DeviceVerificationEntity, TModel], ABC):
    @overload
    async def find(self, id: int) -> DeviceVerificationEntity | None: ...

    @overload
    async def find(self, otp_request_id: int) -> DeviceVerificationEntity | None: ...

    async def find(self, **kwargs) -> DeviceVerificationEntity | None: ...

    async def filter(self, target_id: int) -> List[DeviceVerificationEntity]: ...
