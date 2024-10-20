from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from helloworld.account.features.device import DeviceEntity
from helloworld.core.infra.data.sqlalchemy import BaseModel

class DeviceModel(BaseModel[DeviceEntity]):
    __tablename__ = "device"
    __entity_cls__ = DeviceEntity

    model: Mapped[str] = mapped_column(String(45), nullable=True)
    os: Mapped[str] = mapped_column(String(45), nullable=True)
    os_version: Mapped[str] = mapped_column(String(45), nullable=True)
