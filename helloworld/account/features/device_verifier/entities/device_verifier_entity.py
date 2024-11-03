from __future__ import annotations

from typing import Dict, Any

from pydantic import BaseModel, Field

class DeviceVerifierStartEntity(BaseModel):
    target_id: int = Field(None, title="Target id")
    method: str = Field(None, title="Method", min_length=1, max_length=15)
    token: str = Field(None, title="Token", min_length=1, max_length=255)
    otp_code_len: int | None = Field(None, title="OTP code len")
    params: Dict[str, Any] | None = Field(None, title="Params")