from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.core.data import AbstractUnitOfWork, get_unit_of_work
from helloworld.core.services.decorators import service_manager
from helloworld.account.features.user.data import UserRepository, UserRepositoryImpl
from helloworld.account.features.user import (DeleteUseCase, DeleteUseCaseImpl, SaveUseCase, SaveUseCaseImpl, FindUseCase, FindUseCaseImpl)

@service_manager("database", "main")
async def get_user_repository(session: AsyncSession, authorization: str | None = None) -> UserRepository:
    return UserRepositoryImpl(session, authorization)

async def get_find_use_case(unit_of_work: AbstractUnitOfWork | None = None, authorization: str | None = None) -> FindUseCase:
    unit_of_work = get_unit_of_work(authorization) if not unit_of_work else unit_of_work
    return FindUseCaseImpl(unit_of_work, authorization)

async def get_save_use_case(unit_of_work: AbstractUnitOfWork | None = None, authorization: str | None = None) -> SaveUseCase:
    unit_of_work = get_unit_of_work(authorization) if not unit_of_work else unit_of_work
    return SaveUseCaseImpl(unit_of_work, authorization)

async def get_delete_use_case(unit_of_work: AbstractUnitOfWork | None = None, authorization: str | None = None) -> DeleteUseCase:
    unit_of_work = get_unit_of_work(authorization) if not unit_of_work else unit_of_work
    return DeleteUseCaseImpl(unit_of_work, authorization)