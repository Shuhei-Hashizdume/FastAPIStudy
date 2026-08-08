import pytest
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from schemas import UserCreate
from schemas import UserResponse
from models import UserDB
from security import verify_password


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


def test_create_user(reset_database):
    from tests.support import client

    response = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "test_love",
        },
    )

    assert response.status_code == 201
    response_body = response.json()
    assert "user_id" in response_body
    assert response_body["user_id"] == 1
    assert "email" in response_body
    assert response_body["email"] == "test@example.com"
    assert "password" not in response_body
    assert "hashed_password" not in response_body


def test_create_user_saves_hashed_password(reset_database):
    from tests.support import TestingSessionLocal, client

    plain_password = "test_love"

    response = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": plain_password,
        },
    )

    assert response.status_code == 201
    user_email = response.json()["email"]

    with TestingSessionLocal() as session:
        saved_user = session.query(UserDB).filter(UserDB.email == user_email).first()
        assert saved_user is not None
        assert saved_user.hashed_password != plain_password
        assert verify_password(plain_password, saved_user.hashed_password) is True


def test_create_user_returns_409_when_email_is_duplicated(reset_database):
    from tests.support import client

    first_post_response = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "test_love",
        },
    )

    assert first_post_response.status_code == 201

    second_post_response = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "past_love",
        },
    )

    assert second_post_response.status_code == 409
    assert (
        second_post_response.json()["detail"]
        == "同じメールアドレスのユーザーがすでに登録されています。"
    )


def test_create_user_returns_500_when_database_fails(
    reset_database, monkeypatch, caplog
):
    from tests.support import client

    def raise_commit_error(self):
        raise SQLAlchemyError("テスト用DBエラー")

    monkeypatch.setattr(Session, "commit", raise_commit_error)

    response = client.post(
        "/users",
        json={
            "email": "test@example.com",
            "password": "past_love",
        },
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "ユーザーの登録処理中に失敗しました。"
    assert "ユーザーの登録に失敗しました。" in caplog.text
    assert "テスト用DBエラー" in caplog.text
    assert "SQLAlchemyError" in caplog.text
