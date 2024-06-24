from enum import Enum
from typing import ClassVar

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from db.postgres.base import Base
from db.postgres.models import ID, Deleted, Timestamp


class SexEnum(Enum):
    MALE: ClassVar[str] = "male"
    FEMALE: ClassVar[str] = "female"


class User(Base, ID, Timestamp, Deleted):
    __tablename__: ClassVar[str] = "users"

    first_name: Mapped[str]
    last_name: Mapped[str]
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    sex: Mapped[SexEnum] = mapped_column("sex", ENUM(SexEnum, name="sex"))

    def __repr__(self) -> str:
        return f"<User(login={self.login})>"