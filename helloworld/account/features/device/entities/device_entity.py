from __future__ import annotations

from typing import Optional

from helloworld.core import BaseEntity, Field

class DeviceEntity(BaseEntity):
    model: Optional[str] = Field(None, title="Model", min_length=1, max_length=45)
    os: Optional[str] = Field(None, title="OS", min_length=1, max_length=45)
    os_version: Optional[str] = Field(None, title="OS version", min_length=1, max_length=45)