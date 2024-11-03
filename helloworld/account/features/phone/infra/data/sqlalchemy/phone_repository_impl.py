from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.account.features.phone import PhoneEntity
from helloworld.account.features.phone.data import PhoneRepository
from helloworld.core.infra.data.sqlalchemy import BaseRepository
from .phone_model import PhoneModel

class PhoneRepositoryImpl(PhoneRepository, BaseRepository[PhoneEntity, PhoneModel]):
    def __init__(self, session: AsyncSession, authorization: str | None = None):
        super().__init__(session=session, model_cls=PhoneModel, authorization=authorization)

    async def find(self, **kwargs) -> PhoneEntity | None:
        if 'id' in kwargs:
            return await BaseRepository._find(self, id=kwargs.get('id'))
        elif 'phone_number' in kwargs:
            return await BaseRepository._find(self, phone_number=kwargs.get('phone_number'))

        raise ValueError("You must provide either 'id' or 'phone_number'.")


