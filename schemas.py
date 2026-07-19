from pydantic import BaseModel, ConfigDict


class BookRequest(BaseModel):
    title: str
    author: str


# response_model用
class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int
    title: str
    author: str


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
