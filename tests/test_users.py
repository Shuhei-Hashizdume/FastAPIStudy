import pytest
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import UserDB
from schemas import TokenResponse, UserCreate, UserLogin, UserResponse
from security import verify_password

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test_love"


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


def test_user_login_accepts_valid_input():

    login_data = UserLogin(
        email=TEST_EMAIL,
        password=TEST_PASSWORD,
    )

    assert str(login_data.email) == TEST_EMAIL
    assert login_data.password == TEST_PASSWORD


def test_authenticate_user_returns_user_for_valid_credentials(reset_database):
    from routers.users import authenticate_user
    from tests.support import TestingSessionLocal, client

    response = client.post(
        "/users",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )
    assert response.status_code == 201

    with TestingSessionLocal() as session:
        authenticated_user = authenticate_user(
            email=TEST_EMAIL,
            password=TEST_PASSWORD,
            db=session,
        )

        assert authenticated_user is not None
        assert str(authenticated_user.email) == TEST_EMAIL


def test_authenticate_user_returns_none_for_wrong_password(reset_database):
    from routers.users import authenticate_user
    from tests.support import TestingSessionLocal, client

    response = client.post(
        "/users",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 201

    with TestingSessionLocal() as session:
        authenticated_user = authenticate_user(
            email=TEST_EMAIL, password="wrong_password", db=session
        )

        assert authenticated_user is None


def test_authenticate_user_returns_none_for_unknown_email(reset_database):
    from routers.users import authenticate_user
    from tests.support import TestingSessionLocal

    with TestingSessionLocal() as session:
        authenticated_user = authenticate_user(
            email=TEST_EMAIL, password=TEST_PASSWORD, db=session
        )
        assert authenticated_user is None


def test_token_response_accepts_access_token_and_type():
    token_response = TokenResponse(access_token="JWT文字列", token_type="bearer")
    assert token_response.access_token == "JWT文字列"
    assert token_response.token_type == "bearer"


def test_login_returns_access_token_for_valid_credentials(reset_database, monkeypatch):
    import jwt

    from tests.support import client

    test_secret_key = "A" * 32

    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        test_secret_key,
    )

    post_response = client.post(
        "/users",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    assert post_response.status_code == 201

    user_id = post_response.json()["user_id"]

    login_response = client.post(
        "/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"

    response_body = login_response.json()
    assert isinstance(response_body["access_token"], str)

    decoded_payload = jwt.decode(
        response_body["access_token"], test_secret_key, algorithms=["HS256"]
    )

    assert decoded_payload["sub"] == str(user_id)


def test_login_returns_401_for_wrong_password(reset_database):
    from tests.support import client

    response = client.post(
        "/users",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 201

    login_response = client.post(
        "/login",
        json={
            "email": TEST_EMAIL,
            "password": "wrong_password",
        },
    )

    assert login_response.status_code == 401
    assert (
        login_response.json()["detail"]
        == "メールアドレスまたはパスワードが正しくありません。"
    )


def test_login_returns_401_for_unknown_email(reset_database):
    from tests.support import client

    response = client.post(
        "/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "メールアドレスまたはパスワードが正しくありません。"
    )

    assert response.headers["www-authenticate"] == "Bearer"


def test_read_current_user_returns_authenticated_user(reset_database, monkeypatch):
    from tests.support import client

    test_secret_key = "A" * 32
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        test_secret_key,
    )

    post_response = client.post(
        "/users",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )
    assert post_response.status_code == 201
    user_id = post_response.json()["user_id"]

    login_response = client.post(
        "/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    get_response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert get_response.status_code == 200
    assert get_response.json()["user_id"] == user_id
    assert get_response.json()["email"] == TEST_EMAIL
    assert "hashed_password" not in get_response.json()


def test_read_current_user_returns_401_without_token():
    from tests.support import client

    response = client.get("/users/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
    assert response.headers["www-authenticate"] == "Bearer"


def test_read_current_user_returns_401_for_invalid_token(monkeypatch):
    from tests.support import client

    test_secret_key = "A" * 32
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        test_secret_key,
    )

    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "認証情報を確認できませんでした。"
    assert response.headers["www-authenticate"] == "Bearer"


def test_read_current_user_returns_401_when_token_user_does_not_exist(
    reset_database, monkeypatch
):
    from security import create_access_token
    from tests.support import client

    test_secret_key = "A" * 32
    monkeypatch.setenv("JWT_SECRET_KEY", test_secret_key)

    access_token = create_access_token(subject="999")

    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "認証情報を確認できませんでした。"
    assert response.headers["www-authenticate"] == "Bearer"


def test_read_current_user_returns_401_for_expired_token(monkeypatch):
    from datetime import datetime, timedelta, timezone

    import jwt

    from tests.support import client

    test_secret_key = "A" * 32
    monkeypatch.setenv("JWT_SECRET_KEY", test_secret_key)

    expired_at = datetime.now(timezone.utc) - timedelta(minutes=1)

    payload = {"sub": "999", "exp": expired_at}

    access_token = jwt.encode(payload, test_secret_key, algorithm="HS256")

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "認証情報を確認できませんでした。"
    assert response.headers["www-authenticate"] == "Bearer"
