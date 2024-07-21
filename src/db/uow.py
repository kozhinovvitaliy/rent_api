from types import TracebackType
from typing import Optional

from db.postgres.base import SessionFactory
from db.repo.users_repo import UsersRepo


class UnitOfWork:
    def __init__(self) -> None:
        self.session_factory = SessionFactory()

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.session_factory
        self.users = UsersRepo(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()
