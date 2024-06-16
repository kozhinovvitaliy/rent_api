from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy import Column, ColumnExpressionArgument, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres.base import Base

Table = TypeVar("Table", bound=Base)


class CRUD(Generic[Table]):
    model: Type[Table]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, obj_id: str | UUID) -> Table | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        return (await self.session.execute(stmt)).scalars().one_or_none()

    async def create(self, data: dict[str, Any]) -> Table:
        stmt = insert(self.model).values(**data).returning(self.model)
        return (await self.session.execute(stmt)).scalars().first()

    async def upsert(
        self,
        data: dict[str, Any],
        conflict_cols: tuple[Column, ...],
    ) -> Table:
        stmt = (
            insert(self.model)
            .values(**data)
            .on_conflict_do_update(index_elements=conflict_cols, set_=data)
            .returning(self.model)
        )
        return (await self.session.execute(stmt)).scalars().one()

    async def get_first(self, filters: list[ColumnExpressionArgument]) -> Table:
        stmt = select(self.model).where(*filters)
        return (await self.session.execute(stmt)).scalars().first()
