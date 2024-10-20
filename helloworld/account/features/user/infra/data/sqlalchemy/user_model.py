from __future__ import annotations

from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from helloworld.core.infra.data.sqlalchemy import BaseModel
from helloworld.account.features.user import UserEntity

class UserModel(BaseModel[UserEntity]):
    __tablename__ = "user_account"
    __entity_cls__ = UserEntity

    identity_id: Mapped[str] = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String(50))
