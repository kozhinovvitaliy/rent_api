from typing import Any

from sqlalchemy import Column, select

from db.models import Users
from db.repo.base_repo import CRUD, Table


class UsersRepo(CRUD[Users]):
    model = Users

    async def upsert(
        self,
        data: dict[str, Any],
        conflict_cols: tuple[Column, ...] = (Users.id, Users.login),
    ) -> Table:
        return await super().upsert(data, conflict_cols)

    async def get_by_login(self, login: str) -> Users:
        return await self.get_first([Users.login == login])
