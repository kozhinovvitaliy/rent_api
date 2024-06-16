from litestar import status_codes
from litestar.exceptions import HTTPException


class _BaseException(HTTPException):
    status_code: int
    detail: str

    def __init_subclass__(cls, **kwargs):
        if not hasattr(cls, "status_code") or not isinstance(cls.status_code, int):
            raise AttributeError("Attr. status_code should be integer")

    def __init__(self, detail: str):
        self.detail = detail

    def __str__(self):
        return f"<{self.__class__.__name__}(details={self.detail})>"


class BaseNotFound(_BaseException):
    status_code = status_codes.HTTP_404_NOT_FOUND


class BaseAlreadyExists(_BaseException):
    status_code = status_codes.HTTP_409_CONFLICT
