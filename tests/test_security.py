from datetime import datetime, timezone

from security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_returns_different_string():
    input_password = "testPW"

    hashed_password = hash_password(input_password)

    assert input_password != hashed_password
    assert isinstance(hashed_password, str)


def test_verify_password_returns_true_for_correct_password():
    input_password = "testPW"

    hashed_password = hash_password(input_password)

    result = verify_password(input_password, hashed_password)

    assert result is True


def test_verify_password_returns_false_for_wrong_password():
    correct_password = "correct-password"

    hashed_password = hash_password(correct_password)

    wrong_password = "wrong-password"

    result = verify_password(wrong_password, hashed_password)

    assert result is False


def test_hash_password_uses_different_salt_each_time():
    same_password = "same_password"

    hashed_password1 = hash_password(same_password)
    hashed_password2 = hash_password(same_password)

    assert hashed_password1 != hashed_password2


def test_create_access_token_contains_subject_and_expiration(monkeypatch):
    import jwt

    from security import create_access_token

    test_secret_key = "a" * 32

    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        test_secret_key,
    )

    access_token = create_access_token(subject="1")
    decoded_payload = jwt.decode(
        access_token,
        test_secret_key,
        algorithms=["HS256"],
    )

    assert decoded_payload["sub"] == "1"
    assert "exp" in decoded_payload

    remaining_seconds = decoded_payload["exp"] - datetime.now(timezone.utc).timestamp()
    assert 29 * 60 <= remaining_seconds <= 30 * 60


def test_decode_access_token_returns_payload(monkeypatch):
    test_secret_key = "A" * 32
    monkeypatch.setenv("JWT_SECRET_KEY", test_secret_key)
    access_token = create_access_token(subject="1")
    payload = decode_access_token(token=access_token)

    assert payload["sub"] == "1"
    assert "exp" in payload
