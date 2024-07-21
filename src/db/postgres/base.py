from sqlalchemy import MetaData
from sqlalchemy.ext import asyncio as sa_async
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker

from settings import settings

METADATA = MetaData(
    naming_convention={
        "all_column_names": lambda constraint, _: "_".join(
            [column.name for column in constraint.columns.values()],  # type: ignore[attr-defined]
        ),
        "pk": "pk__%(table_name)s",
        "ix": "ix__%(table_name)s__%(all_column_names)s",
        "fk": "fk__%(table_name)s__%(all_column_names)s__" "%(referred_table_name)s",
        "uq": "uq__%(table_name)s__%(all_column_names)s",
        "ck": "ck__%(table_name)s__%(constraint_name)s",
    },
)

engine: sa_async.AsyncEngine = sa_async.create_async_engine(
    url=settings.postgres.url,
    echo=settings.app.debug,
    future=True,
)

SessionFactory = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False,
)

Base = declarative_base(metadata=METADATA)
from db.models import *
