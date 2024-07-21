
from litestar import status_codes
from litestar.exceptions import HTTPException


class _BaseException(HTTPException):

    def __init__(self, detail: str):
        self.detail = detail

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(details={self.detail})>"


class BaseNotFound(_BaseException):
    status_code = status_codes.HTTP_404_NOT_FOUND


class BaseAlreadyExists(_BaseException):
    status_code = status_codes.HTTP_409_CONFLICT
