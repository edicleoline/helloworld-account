from __future__ import annotations

from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from helloworld.account.features.device import DeviceEntity
from helloworld.core.infra.data.sqlalchemy import BaseModel

class DeviceModel(BaseModel[DeviceEntity]):
    __tablename__ = "device"
    __entity_cls__ = DeviceEntity

    brand: Mapped[str | None] = mapped_column(String(255), nullable=True)
    design_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    device_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    device_year_class: Mapped[int | None] = mapped_column(Integer, nullable=True)
    manufacturer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    os_build_fingerprint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    os_build_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    os_internal_build_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    os_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    os_version: Mapped[str | None] = mapped_column(String(255), nullable=True)
    platform_api_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    product_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    total_memory: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
