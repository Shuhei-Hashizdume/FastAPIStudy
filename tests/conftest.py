import pytest


@pytest.fixture
def reset_database():
    from tests.support import clear_test_data

    clear_test_data()
    yield
    clear_test_data()


@pytest.fixture
def authenticated_client(reset_database, monkeypatch):
    from tests.support import client

    test_secret_key = "A" * 32
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        test_secret_key,
    )

    register_response = client.post(
        "/users",
        json={
            "email": "book-owner@example.com",
            "password": "test_love",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/login",
        json={
            "email": "book-owner@example.com",
            "password": "test_love",
        },
    )

    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client
    client.headers.pop("Authorization", None)
