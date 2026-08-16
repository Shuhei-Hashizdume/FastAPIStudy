from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class BookDB(Base):
    __tablename__ = "books"
    book_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False, index=True)
    isbn: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    publisher_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("publishers.publisher_id"), nullable=True
    )
    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    publisher: Mapped["PublisherDB | None"] = relationship(
        "PublisherDB", back_populates="books"
    )  # カラムではなく、属性！

    @property
    def publisher_name(self) -> str | None:
        if self.publisher is None:
            return None
        return self.publisher.name


class PublisherDB(Base):
    __tablename__ = "publishers"
    publisher_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    books: Mapped[list[BookDB]] = relationship(
        "BookDB", back_populates="publisher"
    )  # カラムではなく、属性！


class UserDB(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
