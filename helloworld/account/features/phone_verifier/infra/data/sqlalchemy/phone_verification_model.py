from __future__ import annotations

from datetime import datetime

import pytz

from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from helloworld.account.features.phone_verifier.entities.phone_verification_entity import PhoneVerificationEntity
from helloworld.core.infra.data.sqlalchemy import BaseModel

class PhoneVerificationModel(BaseModel[PhoneVerificationEntity]):
    __tablename__ = "phone_verification"
    __entity_cls__ = PhoneVerificationEntity

    device_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    phone_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    token: Mapped[str] = mapped_column(String(255), nullable=False)
    otp_code: Mapped[str] = mapped_column(String(8), nullable=False)
    method: Mapped[str] = mapped_column(String(15), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(pytz.utc))
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
