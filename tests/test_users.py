import pytest
from pydantic import ValidationError
from schemas import UserCreate
from schemas import UserResponse
from models import UserDB


def test_user_create_accepts_valid_input():
    user = UserCreate(email="test@gmail.com", password="test_love")

    assert str(user.email) == "test@gmail.com"
    assert user.password == "test_love"


def test_user_create_rejects_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email", password="test_love")


def test_user_create_rejects_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@gmail.com",
            password="1234567",
        )


def test_user_create_rejects_too_long_password():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@gmail.com",
            password="A" * 129,
        )


@pytest.mark.parametrize(
    "password",
    [
        ("A" * 8),
        ("A" * 128),
    ],
)
def test_user_create_accepts_password_boundary_lengths(password):
    user = UserCreate(email="test@gmail.com", password=password)

    assert user.password == password


def test_user_response_reads_userdb_attributes():
    user_db = UserDB(
        user_id=1, email="test@example.com", hashed_password="not-returned-hash"
    )

    # model_validateはクラスメソッド
    response_user = UserResponse.model_validate(user_db)

    assert response_user.user_id == 1
    assert response_user.email == "test@example.com"

    response_body = response_user.model_dump()

    assert "hashed_password" not in response_body
