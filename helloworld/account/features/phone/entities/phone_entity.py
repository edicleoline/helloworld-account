from __future__ import annotations

from helloworld.core import BaseEntity, Field

class PhoneEntity(BaseEntity):
    phone_number: str = Field(None, title="Phone number", min_length=1, max_length=20)