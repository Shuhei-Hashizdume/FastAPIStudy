from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class BookDB(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False, index=True)
    isbn = Column(String, nullable=False, unique=True)
    publisher_id = Column(Integer, ForeignKey("publishers.publisher_id"), nullable=True)
    version = Column(Integer, nullable=False, server_default="1")
    publisher = relationship(
        "PublisherDB", back_populates="books"
    )  # カラムではなく、属性！

    @property
    def publisher_name(self) -> str | None:
        if self.publisher is None:
            return None
        return self.publisher.name


class PublisherDB(Base):
    __tablename__ = "publishers"
    publisher_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    books = relationship("BookDB", back_populates="publisher")  # カラムではなく、属性！


class UserDB(Base):
    __tablename__ = "users"
    user_id = Column(
        Integer,
        primary_key=True,
    )
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
