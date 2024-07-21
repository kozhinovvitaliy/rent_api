from datetime import datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from litestar.exceptions import NotAuthorizedException
from pydantic import UUID4, BaseModel

from settings import settings

DEFAULT_TIME_DELTA = timedelta(days=1)


class Token(BaseModel):
    exp: datetime
    iat: datetime
    sub: UUID4


def decode_jwt_token(encoded_token: str) -> Token:
    try:
        payload = jwt.decode(
            token=encoded_token,
            key=settings.security.jwt_secret,
            algorithms=[settings.security.algorithm],
        )
        return Token(**payload)
    except JWTError as e:
        raise NotAuthorizedException("Invalid token") from e  # noqa: TRY003, EM101


def encode_jwt_token(user_id: UUID, expiration: timedelta = DEFAULT_TIME_DELTA) -> str:
    """Helper function that encodes a JWT token with expiration and a given user_id."""  # noqa: D401
    token = Token(
        exp=datetime.now() + expiration,  # noqa: DTZ005
        iat=datetime.now(),  # noqa: DTZ005
        sub=user_id,
    )
    return jwt.encode(token.dict(), settings.security.jwt_secret, algorithm=settings.security.algorithm)
