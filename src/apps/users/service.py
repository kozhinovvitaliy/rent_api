import hashlib
import uuid
from uuid import UUID

from apps.base_app.service import BaseService
from apps.users.exceptions import UserAlreadyExistsException, UserNotFoundException
from apps.users.schemas import CreateUserRequest, UserLoginRequest
from db.models import User
from db.uow import UnitOfWork


class UserService(BaseService):

    @staticmethod
    async def get_user(user_id: UUID, uow: UnitOfWork) -> User:
        if user := await uow.users.get(user_id):
            return user
        detail = f"user {user_id} not found"
        raise UserNotFoundException(detail)

    async def create_user(self, data: CreateUserRequest, uow: UnitOfWork) -> User:
        if await uow.users.get_by_login(data.login):
            detail = f"user {data.login} already exists"
            raise UserAlreadyExistsException(detail)
        raw_data = data.model_dump(exclude={"password"})
        hashed_password = self.__hash_user_password(data.password)
        raw_data["password"] = hashed_password
        user = await uow.users.create(raw_data)
        await uow.commit()
        return user

    async def login(self, login_data: UserLoginRequest, uow: UnitOfWork) -> UUID:
        user = await uow.users.get_by_login(login_data.login)
        if not user or self.__hash_user_password(login_data.password) != user.password:
            detail = f"User {login_data.login} not found"
            raise UserNotFoundException(detail)
        return uuid.uuid4()

    @staticmethod
    def __hash_user_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
