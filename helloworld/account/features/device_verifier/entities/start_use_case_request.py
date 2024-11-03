from __future__ import annotations

from helloworld.core import BaseEntity, Field
from helloworld.auth.features.device_otp import OTPType

class StartUseCaseRequest(BaseEntity):
    target_id: int = Field(title="Target id")
    device_id: int = Field(title="Device id")
    otp_type: OTPType = Field(title="OTP Type")