from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from helloworld.account.features.phone.entities.phone_entity import PhoneEntity
from helloworld.core.infra.data.sqlalchemy import BaseModel

class PhoneModel(BaseModel[PhoneEntity]):
    __tablename__ = "phone"
    __entity_cls__ = PhoneEntity

    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
