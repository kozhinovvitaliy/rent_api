from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy import ColumnExpressionArgument, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres.base import Base

Table = TypeVar("Table", bound=Base)


class CRUD(Generic[Table]):
    model: Type[Table]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, obj_id: str | UUID) -> Table | None:
        stmt = select(self.model).where(self.model.id == obj_id)  # type: ignore[attr-defined]
        return (await self.session.execute(stmt)).scalars().one_or_none()

    async def create(self, data: dict[str, Any]) -> Table | None:
        stmt = insert(self.model).values(**data).returning(self.model)
        return (await self.session.execute(stmt)).scalars().first()

    async def get_first(self, filters: list[ColumnExpressionArgument[Any]]) -> Table | None:
        stmt = select(self.model).where(*filters)
        return (await self.session.execute(stmt)).scalars().first()
