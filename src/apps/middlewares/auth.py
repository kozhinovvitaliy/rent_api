from typing import TYPE_CHECKING, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from apps.security.schema import decode_jwt_token
from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
)
from settings import settings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine

API_KEY_HEADER = settings.app.key


class JWTAuthenticationMiddleware(AbstractAuthenticationMiddleware):
    async def authenticate_request(self, connection: ASGIConnection) -> AuthenticationResult:

        auth_header = connection.headers.get(API_KEY_HEADER)
        if not auth_header:
            raise NotAuthorizedException()

        # decode the token, the result is a ``Token`` model instance
        token = decode_jwt_token(encoded_token=auth_header)

        engine = cast("AsyncEngine", connection.app.state.postgres_connection)
        async with AsyncSession(engine) as async_session:
            async with async_session.begin():
                user = await async_session.execute(select(User).where(User.id == token.sub))
        if not user:
            raise NotAuthorizedException()
        return AuthenticationResult(user=user, auth=token)