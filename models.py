from database import Base
from sqlalchemy import Column, Integer, String


class BookDB(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
