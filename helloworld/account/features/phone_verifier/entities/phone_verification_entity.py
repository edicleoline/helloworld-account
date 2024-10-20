from __future__ import annotations

from typing import Optional
from datetime import datetime

from helloworld.core import BaseEntity, Field

class PhoneVerificationEntity(BaseEntity):
    device_id: int = Field(None, title="Device Id")
    phone_id: int = Field(None, title="Phone Id")
    token: str = Field(None, title="Token", min_length=1, max_length=255)
    otp_code: str = Field(None, title="OTP code", min_length=1, max_length=8)
    method: str = Field(None, title="Method", min_length=1, max_length=15)
    created_at: Optional[datetime] = Field(None, title="Created at")
    verified_at: Optional[datetime] = Field(None, title="Verified at")