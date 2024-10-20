from __future__ import annotations

from datetime import datetime

import pytz

from sqlalchemy import String, BigInteger, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from helloworld.account.features.phone_verifier.entities.otp_request_limit_entity import OTPRequestLimitEntity
from helloworld.core.infra.data.sqlalchemy import BaseModel

class OTPRequestLimitModel(BaseModel[OTPRequestLimitEntity]):
    __tablename__ = "otp_request_limit"
    __entity_cls__ = OTPRequestLimitEntity

    device_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    phone_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    method: Mapped[str] = mapped_column(String(15), nullable=False)
    last_request_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(pytz.utc))
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    cooldown_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
