from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres.base import SessionFactory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()
