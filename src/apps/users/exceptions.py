from litestar import status_codes

from apps.base_app.exceptions import BaseAlreadyExists, BaseNotFound


class UserNotFoundException(BaseNotFound):
    status_code = status_codes.HTTP_404_NOT_FOUND

    def __init__(self, detail: str = "user not found"):
        super().__init__(detail=detail)


class UserAlreadyExistsException(BaseAlreadyExists):
    status_code = status_codes.HTTP_409_CONFLICT

    def __init__(self, detail: str = "user already exists"):
        super().__init__(detail=detail)
