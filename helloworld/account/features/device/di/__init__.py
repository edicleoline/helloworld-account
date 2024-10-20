from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from helloworld.core.services.decorators import service_manager
from helloworld.account.features.device.data import DeviceRepository, DeviceRepositoryImpl
from helloworld.core.data import AbstractUnitOfWork, get_unit_of_work
from helloworld.account.features.device import InstallUseCase, InstallUseCaseImpl

@service_manager("database", "auth")
async def get_device_repository(session: AsyncSession, authorization: str | None = None) -> DeviceRepository:
    return DeviceRepositoryImpl(session, authorization)

async def get_install_use_case(authorization: str | None = None, unit_of_work: AbstractUnitOfWork | None = None) -> InstallUseCase:
    unit_of_work = get_unit_of_work(authorization) if not unit_of_work else unit_of_work
    return InstallUseCaseImpl(unit_of_work, authorization)