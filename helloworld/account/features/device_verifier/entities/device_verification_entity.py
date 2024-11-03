from __future__ import annotations

from datetime import datetime

from helloworld.core import BaseEntity, Field

class DeviceVerificationEntity(BaseEntity):
    device_id: int = Field(title="Device Id")
    verification_type: str = Field(title="Verification type", min_length=1, max_length=15)
    method: str = Field(None, title="Method", min_length=1, max_length=15)
    target_id: int = Field(title="Target Id")
    otp_request_id: int = Field(title="OTP Request Id")
    created_at: datetime = Field(default_factory=datetime.now, title="Created at")
    verified_at: datetime | None = Field(None, title="Verified at")