from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.core.services.decorators import service_manager
from helloworld.account.features.phone.data import PhoneRepository, PhoneRepositoryImpl
from helloworld.account.features.phone import FindOrCreateUseCase, FindOrCreateUseCaseImpl
from helloworld.core.data import AbstractUnitOfWork, get_unit_of_work

@service_manager("database", "auth")
async def get_phone_repository(session: AsyncSession, authorization: str | None = None) -> PhoneRepository:
    return PhoneRepositoryImpl(session, authorization)


async def get_find_or_create_use_case(authorization: str | None = None, unit_of_work: AbstractUnitOfWork | None = None) -> FindOrCreateUseCase:
    unit_of_work = get_unit_of_work(authorization) if not unit_of_work else unit_of_work
    return FindOrCreateUseCaseImpl(unit_of_work, authorization)