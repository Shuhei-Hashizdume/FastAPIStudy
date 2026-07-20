import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(bind=test_engine)


def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# 登録
def test_create_book():
    response = client.post(
        "/books",
        json={
            "title": "pytest入門",
            "author": "テスト太郎",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "book_id": 1,
        "title": "pytest入門",
        "author": "テスト太郎",
    }


# 登録　異常系
def test_create_book_without_author():
    response = client.post(
        "/books",
        json={"title": "著者のいない本"},
    )
    assert response.status_code == 422


# 取得
def test_get_book():
    create_response = client.post(
        "/books",
        json={
            "title": "GETテスト用の本",
            "author": "取得太郎",
        },
    )

    assert create_response.status_code == 201

    book_id = create_response.json()["book_id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json() == {
        "book_id": book_id,
        "title": "GETテスト用の本",
        "author": "取得太郎",
    }


# 全件取得
def test_show_books():
    first_response = client.post(
        "/books",
        json={
            "title": "1冊目",
            "author": "著者A",
        },
    )
    assert first_response.status_code == 201

    second_response = client.post(
        "/books",
        json={
            "title": "2冊目",
            "author": "著者B",
        },
    )

    assert second_response.status_code == 201

    first_book = first_response.json()
    second_book = second_response.json()

    response = client.get("/books")

    assert response.status_code == 200
    assert response.json() == [first_book, second_book]


# 条件による一部取得
def test_show_books_by_author():
    first_response = client.post(
        "/books",
        json={
            "title": "著者Aの1冊目",
            "author": "著者A",
        },
    )
    assert first_response.status_code == 201

    second_response = client.post(
        "/books",
        json={
            "title": "著者Bの1冊目",
            "author": "著者B",
        },
    )

    assert second_response.status_code == 201

    third_response = client.post(
        "/books",
        json={
            "title": "著者Aの2冊目",
            "author": "著者A",
        },
    )

    assert third_response.status_code == 201

    first_book = first_response.json()
    third_book = third_response.json()

    response = client.get("/books", params={"author": "著者A"})

    assert response.status_code == 200
    assert response.json() == [first_book, third_book]


# 取得　異常系
def test_get_book_not_found():
    response = client.get("/books/9999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "該当する本がありません。"}


# 更新　正常系
def test_update_book_title():
    create_response = client.post(
        "/books",
        json={
            "title": "更新前タイトル",
            "author": "変更しない著者",
        },
    )
    assert create_response.status_code == 201

    book_id = create_response.json()["book_id"]

    response = client.patch(
        f"/books/{book_id}",
        json={"title": "変更後のタイトル"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "book_id": book_id,
        "title": "変更後のタイトル",
        "author": "変更しない著者",
    }


# 削除　正常系
def test_delete_book():
    create_response = client.post(
        "/books",
        json={
            "title": "削除用の本",
            "author": "削除太郎",
        },
    )
    assert create_response.status_code == 201

    book_id = create_response.json()["book_id"]
    delete_response = client.delete(f"/books/{book_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "該当する本がありません。"}


def test_delete_book_not_found():
    response = client.delete("/books/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "該当する本がありません。"}
