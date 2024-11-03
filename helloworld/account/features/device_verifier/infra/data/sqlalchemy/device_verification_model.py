from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from helloworld.account.features.device_verifier.entities.device_verification_entity import DeviceVerificationEntity
from helloworld.core.infra.data.sqlalchemy import BaseModel

class PhoneVerificationModel(BaseModel[DeviceVerificationEntity]):
    __tablename__ = "device_verification"
    __entity_cls__ = DeviceVerificationEntity

    device_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    verification_type: Mapped[str] = mapped_column(String(15), nullable=False)
    method: Mapped[str] = mapped_column(String(15), nullable=False)
    target_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    otp_request_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
