from __future__ import annotations

from pydantic import BaseModel, Field

class PhoneVerifierStartEntity(BaseModel):
    phone_id: int = Field(None, title="Phone id")
    method: str = Field(None, title="Method", min_length=1, max_length=15)
    token: str = Field(None, title="Token", min_length=1, max_length=255)
    otp_code_len: int = Field(None, title="OTP code len")