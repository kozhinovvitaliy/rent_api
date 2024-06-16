from sqlalchemy.ext.asyncio import AsyncSession

from db.uow import UnitOfWork


async def get_uow(injected_session: AsyncSession) -> UnitOfWork:
    return UnitOfWork(injected_session)
