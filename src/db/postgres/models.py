from datetime import datetime
from uuid import uuid4

from sqlalchemy import TIMESTAMP, FetchedValue, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class ID:
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        "id",
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        unique=True,
        nullable=False,
    )


@declarative_mixin
class Timestamp:
    __abstract__ = True
    """Mixin class for SQLAlchemy models created_at & updated_at fields."""

    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        TIMESTAMP,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        TIMESTAMP,
        server_default=func.now(),
        server_onupdate=FetchedValue(),
        nullable=False,
    )


@declarative_mixin
class Deleted:
    __abstract__ = True
    """Mixin class for SQLAlchemy models deleted_at field."""

    deleted_at: Mapped[datetime] = mapped_column(
        "deleted_at",
        TIMESTAMP,
        nullable=True,
    )
