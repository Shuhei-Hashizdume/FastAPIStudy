from pydantic import BaseModel, ConfigDict, Field


class BookRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    isbn: str = Field(min_length=13, max_length=13, pattern=r"^[0-9]+$")


class BookUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    author: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    isbn: str | None = Field(
        default=None,
        min_length=13,
        max_length=13,
        pattern=r"^[0-9]+$",
    )


# response_model用
class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int
    title: str
    author: str
    isbn: str
