from types import TracebackType
from typing import Optional, Type

from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession

from db.repo.users_repo import UsersRepo


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> "UnitOfWork":
        self.users = UsersRepo(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[Type[BaseException]],
        exc_tb: Optional[Type[TracebackType]],
    ) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()
