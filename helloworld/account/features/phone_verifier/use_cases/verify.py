from __future__ import annotations

import re
from abc import ABC
from typing import overload

from helloworld.account.features.phone_verifier.data import PhoneVerificationRepository
from helloworld.account.features.phone_verifier.entities.phone_verification_entity import PhoneVerificationEntity
from helloworld.core.error import exceptions
from helloworld.auth.error import exceptions as auth_exceptions
from helloworld.core import BaseUseCaseUnitOfWork
from helloworld.core.util.security import generate_otp
from helloworld.account.features.phone import PhoneEntity
from helloworld.account.features.phone.data import PhoneRepository
from helloworld.account.features.phone_verifier import PhoneVerifierStartEntity
from helloworld.auth.jwt.services import AbstractService

class VerifyUseCase(BaseUseCaseUnitOfWork[dict, None], ABC):
    async def execute(self, **kwargs) -> None:
        raise NotImplementedError

class VerifyUseCaseImpl(VerifyUseCase):
    @overload
    async def execute(self, token: str, otp_code: str) -> None:...

    async def execute(self, **kwargs) -> None:
        async with self.unit_of_work as unit_of_work:
            token = kwargs.get("token")
            otp_code = kwargs.get("otp_code")

            token_service: AbstractService = await self.services.get("authentication", "otp-token")
            decoded_token = await token_service.decode(token)

            if not decoded_token:
                raise auth_exceptions.InvalidTokenError

            sub = decoded_token.get("sub")

            if not decoded_token or not sub:
                raise auth_exceptions.InvalidTokenError

            print("sub", sub, decoded_token)

            phone_verification_repository: PhoneVerificationRepository = await unit_of_work.repository_factory.instance(
                PhoneVerificationRepository)

            phone_verification_entity = await phone_verification_repository.find(id=sub)




            phone_repository: PhoneRepository = await unit_of_work.repository_factory.instance(PhoneRepository)
            # print("verify!!!!!!!!!!!!!!!!!!!!!!!!!!!!", kwargs)


            raise exceptions.InvalidOTPCodeError('aaaaaaaaaaaaaaaa')
            # if not kwargs.get("phone_number"):
            #     raise Exception("We need phone_number")
            #
            # phone_number = re.sub(r'[^\d+]', '', kwargs.get("phone_number"))
            #
            # phone_entity = await phone_repository.find(phone_number=phone_number)
            #
            # if not phone_entity:
            #     phone_entity = PhoneEntity(phone_number=phone_number)
            #     phone_entity = await phone_repository.save(entity=phone_entity)
            #
            # phone_verification_repository: PhoneVerificationRepository = await unit_of_work.repository_factory.instance(PhoneVerificationRepository)
            #
            # token_service: AbstractService = await self.services.get("authentication", "otp-token")
            #
            # token_data = {}
            # token = await token_service.encode(token_data)
            #
            # otp_code = generate_otp()
            #
            # verification_entity = PhoneVerificationEntity(
            #     phone_id=phone_entity.id,
            #     token=token,
            #     otp_code=otp_code
            # )
            #
            # await phone_verification_repository.save(entity=verification_entity)
            #
            # return PhoneVerifierStartEntity(
            #     token = token,
            #     otp_code_len=len(otp_code)
            # )