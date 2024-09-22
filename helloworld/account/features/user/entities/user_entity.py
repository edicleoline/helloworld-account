from __future__ import annotations

from typing import Optional

from helloworld.core import BaseEntity, Field

class UserEntity(BaseEntity):
    identity_id: Optional[str] = Field(None, title="Identity Id")
    first_name: Optional[str] = Field(None, title="User Name", min_length=1, max_length=100)