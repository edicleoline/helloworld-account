from __future__ import annotations

from datetime import datetime
from typing import Dict, Union

from helloworld.core import BaseEntity, Field

class MethodEntity(BaseEntity):
    key: str = Field(..., title="Method", min_length=1, max_length=15)
    title: str = Field(..., title="Title")
    label: str = Field(..., title="Label")
    params: Dict[str, Union[str, int, bool]] | None = Field(None, title="Params")
    icon: str | None = Field(None, title="Icon")
    last_request_at: datetime | None = Field(None, title="Last request time")
    attempt_count: int = Field(0, title="Attempt try count")
    cooldown_seconds: int | None = Field(None, title="Cooldown time")

    class Config:
        exclude_none = True