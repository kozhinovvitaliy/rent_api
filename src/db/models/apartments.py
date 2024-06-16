from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from db.postgres.base import Base
from db.postgres.models import ID, Deleted, Timestamp


class Apartments(Base, ID, Timestamp, Deleted):
    __tablename__ = "apartments"

    user_id: Mapped[UUID] = mapped_column("user_id", ForeignKey("users.id"))
    name: Mapped[str]
    room_count: Mapped[int]
    square: Mapped[float]
    benefits: Mapped[list] = mapped_column("benefits", ARRAY(String))

    def __repr__(self) -> str:
        return f"<Apartment(id={self.id}, name={self.name}>"
