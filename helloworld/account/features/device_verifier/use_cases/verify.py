from __future__ import annotations

from abc import ABC
from typing import Tuple

from helloworld.account.features.device_verifier.data import DeviceVerificationRepository
from helloworld.auth.features.identity.data import IdentityRepository
from helloworld.auth.features.identity import IdentityEntity
from helloworld.core.error import exceptions
from helloworld.auth.error import exceptions as auth_exceptions
from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.auth.features.identity.data import IdentityVerificationRepository
from helloworld.auth.jwt.services import TokenService
from helloworld.auth.features.otp.use_cases import ValidateUseCase
from helloworld.auth.features.otp.const import SUB

class VerifyUseCase(BaseUseCaseUnitOfWork[Tuple[str, str], IdentityEntity], ABC):
    async def execute(self, token: str, otp_code: str) -> IdentityEntity | None:
        raise NotImplementedError

class VerifyUseCaseImpl(VerifyUseCase):
    async def execute(self, token: str, otp_code: str) -> IdentityEntity | None:
        async with self.unit_of_work as unit_of_work:
            otp_validate_use_case: ValidateUseCase = await unit_of_work.use_case_factory.instance(ValidateUseCase)
            valid = await otp_validate_use_case.execute(token=token, code=otp_code)

            if not valid:
                raise exceptions.InvalidOTPCodeError

            token_service: TokenService = await self.services.get("authentication", "otp-token")
            decoded_token = await token_service.decode(token)

            if not decoded_token:
                raise auth_exceptions.InvalidTokenError

            sub = decoded_token.get(SUB)

            device_verification_repository: DeviceVerificationRepository = await unit_of_work.repository_factory\
                .instance(DeviceVerificationRepository)

            device_verification_entity = await device_verification_repository.find(otp_request_id=sub)

            identity_verification_repository: IdentityVerificationRepository = await unit_of_work.repository_factory\
                .instance(IdentityVerificationRepository)

            identity_verification_entity = await identity_verification_repository.find(
                criteria="and",
                target_id=device_verification_entity.target_id,
                verification_type=device_verification_entity.verification_type
            )

            identity_repository: IdentityRepository = await unit_of_work.repository_factory.instance(IdentityRepository)

            identity_entity: IdentityEntity | None = await identity_repository\
                .find(id=identity_verification_entity.identity_id) if identity_verification_entity else None

            return identity_entity

            # from helloworld.account.features.device_verifier.entities.device_verification_entity import \
            #     DeviceVerificationEntity
            # from helloworld.auth.features.identity import IdentityVerificationEntity
            # if not identity_verification_entity:
            #     identity_entity = await identity_repository.create(IdentityEntity(
            #         id=IdentityEntity.new_id()
            #     ))
            #
            #     await identity_verification_repository.create(IdentityVerificationEntity(
            #         id=IdentityVerificationEntity.new_id(),
            #         identity_id=identity_entity.id,
            #         target_id=device_verification_entity.target_id,
            #         verification_type=device_verification_entity.verification_type
            #     ))

            # token_service: TokenService = await self.services.get("authentication", "token")
            # refresh_token_service: TokenService = await self.services.get("authentication", "refresh-token")

            # access_token = await token_service.encode({SUB: identity_entity.id})
            # refresh_token = await refresh_token_service.encode({SUB: identity_entity.id})