from pydantic import BaseModel, ConfigDict, Field
from pydantic import EmailStr


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
    version: int = Field(ge=1)


# response_model用
class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    book_id: int
    title: str
    author: str
    isbn: str
    publisher_name: str | None
    version: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
