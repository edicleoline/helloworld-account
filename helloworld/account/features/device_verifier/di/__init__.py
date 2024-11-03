from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.core.data import AbstractUnitOfWork, get_unit_of_work
from helloworld.core.services.decorators import service_manager
from helloworld.account.features.device_verifier import (
    StartUseCase, StartUseCaseImpl, VerifyUseCase, VerifyUseCaseImpl, MethodsUseCase, MethodsUseCaseImpl,
    DeviceByVerifiedPhoneUseCase, DeviceByVerifiedPhoneUseCaseImpl)
from helloworld.account.features.device_verifier.data import (DeviceVerificationRepository, DeviceVerificationRepositoryImpl)

@service_manager("database", "auth")
async def get_phone_verification_repository(session: AsyncSession, authorization: str | None = None) -> DeviceVerificationRepository:
    return DeviceVerificationRepositoryImpl(session, authorization)

async def get_start_use_case(authorization: str | None = None, unit_of_work: AbstractUnitOfWork | None = None) -> StartUseCase:
    unit_of_work = get_unit_of_work(authorization) if not unit_of_work else unit_of_work
    return StartUseCaseImpl(unit_of_work, authorization)

async def get_verify_use_case(authorization: str | None = None, unit_of_work: AbstractUnitOfWork | None = None) -> VerifyUseCase:
    unit_of_work = get_unit_of_work(authorization) if not unit_of_work else unit_of_work
    return VerifyUseCaseImpl(unit_of_work, authorization)

async def get_methods_use_case(authorization: str | None = None, unit_of_work: AbstractUnitOfWork | None = None) -> MethodsUseCase:
    unit_of_work = get_unit_of_work(authorization) if not unit_of_work else unit_of_work
    return MethodsUseCaseImpl(unit_of_work, authorization)

async def get_device_by_verified_phone_use_case(authorization: str | None = None, unit_of_work: AbstractUnitOfWork | None = None) -> DeviceByVerifiedPhoneUseCase:
    unit_of_work = get_unit_of_work(authorization) if not unit_of_work else unit_of_work
    return DeviceByVerifiedPhoneUseCaseImpl(unit_of_work, authorization)