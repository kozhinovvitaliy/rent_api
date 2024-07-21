import hashlib
import uuid
from typing import TYPE_CHECKING, Optional, Union
from uuid import UUID

from apps.base_app.service import BaseService
from apps.users.exceptions import UserAlreadyExistsException, UserNotFoundException
from db.models import User
from db.uow import UnitOfWork

from apps.users.schemas import CreateUserRequest, UserLoginRequest, GetUserResponse


class UserService(BaseService):

    @staticmethod
    async def get_user(user_id: UUID, uow: UnitOfWork) -> GetUserResponse:
        async with uow:
            if user := await uow.users.get(user_id):
                return GetUserResponse(
                    login=user.login,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    sex=user.sex
                )
            detail = f"user {user_id} not found"
            raise UserNotFoundException(detail=detail)

    async def create_user(self, data: "CreateUserRequest", uow: UnitOfWork) -> Optional[User]:
        async with uow:
            if await uow.users.get_by_login(data.login):
                detail = f"User with login {data.login} already exists"
                raise UserAlreadyExistsException(detail=detail)
            raw_data = data.model_dump(exclude={"password"})
            hashed_password = self.__hash_user_password(data.password)
            raw_data["password"] = hashed_password
            user = await uow.users.create(raw_data)
            await uow.commit()
            return user

    async def login(self, login_data: "UserLoginRequest", uow: UnitOfWork) -> Optional[Union[UUID, Exception]]:
        async with uow:
            user = await uow.users.get_by_login(login_data.login)
            if not user or self.__hash_user_password(login_data.password) != user.password:
                detail = f"User {login_data.login} not found"
                raise UserNotFoundException(detail)
            return user.id

    @staticmethod
    def __hash_user_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
