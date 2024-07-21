from typing import ClassVar, Optional
from uuid import UUID

from litestar import MediaType, get, post

from apps.base_app.controller import BaseController
from apps.users.schemas.pydantic_schemas import (
    CreateUserRequest,
    GetUserResponse,
    UserLoginRequest,
    UserLoginResponse,
)
from apps.users.service import UserService
from db.uow import UnitOfWork
from apps.middlewares import auth_middleware


class UserController(BaseController):
    service: ClassVar[UserService] = UserService()

    @get("/{user_id:uuid}", media_type=MediaType.JSON, middleware=[auth_middleware])
    async def get_user(
            self,
            user_id: UUID,
            injected_uow: UnitOfWork,
    ) -> GetUserResponse:
        return await self.service.get_user(user_id, uow=injected_uow)

    @post("", media_type=MediaType.JSON)
    async def create_user(  # type: ignore[return]
            self,
            data: CreateUserRequest,
            injected_uow: UnitOfWork,
    ) -> Optional[GetUserResponse]:
        user = await self.service.create_user(data=data, uow=injected_uow)
        if user:
            return GetUserResponse(
                first_name=user.first_name,
                last_name=user.last_name,
                login=user.login,
                sex=user.sex,
            )
        return None

    @post("/login", media_type=MediaType.JSON)
    async def login(
            self,
            data: UserLoginRequest,
            injected_uow: UnitOfWork,
    ) -> UserLoginResponse:
        authentication_code = await self.service.login(login_data=data, uow=injected_uow)
        schema = UserLoginResponse(authentication_code=authentication_code)
        return UserLoginResponse(authentication_code=authentication_code)
