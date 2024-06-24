from typing import Any

from sqlalchemy import Column

from db.models import User
from db.repo.base_repo import CRUD, Table


class UsersRepo(CRUD[User]):
    model = User

    async def upsert(
        self,
        data: dict[str, Any],
        conflict_cols: tuple[Column, ...] = (User.id, User.login),
    ) -> Table:
        return await super().upsert(data, conflict_cols)

    async def get_by_login(self, login: str) -> User:
        return await self.get_first([User.login == login])
