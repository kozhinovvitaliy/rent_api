from uuid import UUID
from typing import Any

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.uow import UnitOfWork
from db.models import User


def is_uuid(value: Any) -> bool:
    try:
        val = UUID(value)
        return True
    except ValueError:
        return False


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:  # type: ignore[type-arg]

        user_id = connection.headers.get("x-api-key")
        if not user_id or not is_uuid(user_id):
            raise NotAuthorizedException

        async with UnitOfWork() as uow:  # noqa: SIM117
            user = await uow.users.get(user_id)
            if not user:
                raise NotAuthorizedException
        return AuthenticationResult(user=user, auth=user_id)
