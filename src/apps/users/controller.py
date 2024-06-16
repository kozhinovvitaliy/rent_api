from uuid import UUID

from litestar import MediaType, get, post

from apps.base_app.controller import BaseController
from apps.users.schemas.pydantic_schemas import CreateUserRequest, GetUserResponse, UserLoginRequest, UserLoginResponse
from apps.users.service import UserService
from db.uow import UnitOfWork


class UserController(BaseController):
    service = UserService()

    @get("/{user_id:uuid}", media_type=MediaType.JSON)
    async def get_user(
        self, user_id: UUID, injected_uow: UnitOfWork,
    ) -> GetUserResponse:
        async with injected_uow as uow:
            return await self.service.get_user(user_id, uow=uow)

    @post("", media_type=MediaType.JSON)
    async def create_user(
        self, data: CreateUserRequest, injected_uow: UnitOfWork,
    ) -> GetUserResponse:
        async with injected_uow as uow:
            data = await self.service.create_user(data=data, uow=uow)
            return GetUserResponse(
                first_name=data.first_name,
                last_name=data.last_name,
                login=data.login,
                sex=data.sex,
            )

    @post("/login", media_type=MediaType.JSON)
    async def login(
        self, data: UserLoginRequest, injected_uow: UnitOfWork,
    ) -> UserLoginResponse:
        async with injected_uow as uow:
            authentication_code = await self.service.login(data, uow)
            return UserLoginResponse(authentication_code=authentication_code)
