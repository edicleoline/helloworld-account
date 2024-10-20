from __future__ import annotations

from typing import Optional
from datetime import datetime

from helloworld.core import BaseEntity, Field

class OTPRequestLimitEntity(BaseEntity):
    device_id: int = Field(..., title="Device Id")
    phone_id: int = Field(..., title="Phone Id")
    method: str = Field(..., title="Method", min_length=1, max_length=15)
    last_request_at: Optional[datetime] = Field(None, title="Last request time")
    attempt_count: int = Field(0, title="Attempt try count")
    cooldown_seconds: int = Field(60, title="Cooldown time")
