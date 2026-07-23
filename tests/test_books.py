import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import BookDB
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


# 書籍一覧取得　　ページネーションテスト
def test_show_books_with_pagination():
    first_response = client.post(
        "/books",
        json={
            "title": "ページネーション本A",
            "author": "著者A",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/books",
        json={
            "title": "ページネーション本B",
            "author": "著者B",
        },
    )

    assert second_response.status_code == 201

    third_response = client.post(
        "/books",
        json={
            "title": "ページネーション本C",
            "author": "著者C",
        },
    )

    assert third_response.status_code == 201

    response = client.get(
        "/books",
        params={
            "offset": 1,
            "limit": 1,
        },
    )

    assert response.status_code == 200

    second_book = second_response.json()

    assert response.json() == [second_book]


# 一覧取得　offset異常系
def test_show_books_with_invalid_offset():
    response = client.get(
        "/books",
        params={"offset": -1},
    )

    assert response.status_code == 422


# 一覧取得　limit異常系
def test_show_books_with_too_large_limit():
    response = client.get(
        "/books",
        params={"limit": 101},
    )

    assert response.status_code == 422


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


# 削除　異常系
def test_delete_book_not_found():
    response = client.delete("/books/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "該当する本がありません。"}


# 登録　DBエラー　　integrity
def test_create_book_db_integrity_error(monkeypatch, caplog):
    def raise_commit_error(self):
        raise IntegrityError(
            "テスト用SQL",
            {},
            Exception("NOT NULL制約違反"),
        )

    monkeypatch.setattr(Session, "commit", raise_commit_error)
    response = client.post(
        "/books", json={"title": "DBエラーテスト", "author": "テスト太郎"}
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "書籍の登録処理中に失敗しました。"}
    assert "書籍データがDB制約に違反しました。" in caplog.text
    assert "IntegrityError" in caplog.text
    assert "NOT NULL制約違反" in caplog.text


# 登録　DBエラー　　モックテスト
def test_create_book_sqlalchemy_error(monkeypatch, caplog):
    def raise_commit_error(self):
        raise SQLAlchemyError("テスト用DB接続エラー")

    monkeypatch.setattr(Session, "commit", raise_commit_error)

    response = client.post(
        "/books",
        json={
            "title": "一般DBエラーテスト",
            "author": "テスト太郎",
        },
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "書籍の登録処理中に失敗しました。"}
    assert "書籍の登録に失敗しました。" in caplog.text
    assert "SQLAlchemyError" in caplog.text
    assert "テスト用DB接続エラー" in caplog.text


# 一部更新　　 モックテスト
def test_update_book_sqlalchemy_error(monkeypatch, caplog):
    post_response = client.post(
        "/books",
        json={
            "title": "更新前タイトル",
            "author": "更新エラーテスト著者",
        },
    )

    assert post_response.status_code == 201

    book_id = post_response.json()["book_id"]

    def raise_commit_error(self):
        raise SQLAlchemyError("テスト用更新DBエラー")

    monkeypatch.setattr(Session, "commit", raise_commit_error)

    response = client.patch(
        f"/books/{book_id}",
        json={"title": "更新後タイトル"},
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "書籍の更新処理中に失敗しました。"}
    assert "書籍の更新に失敗しました。" in caplog.text
    assert "SQLAlchemyError" in caplog.text
    assert "テスト用更新DBエラー" in caplog.text


# 削除　モックテスト
def test_delete_book_sqlalchemy_error(monkeypatch, caplog):
    api_post_response = client.post(
        "/books", json={"title": "テストA", "author": "著者A"}
    )

    assert api_post_response.status_code == 201

    book_id = api_post_response.json()["book_id"]

    def raise_commit_error(self):
        raise SQLAlchemyError("テスト用削除DBエラー")

    monkeypatch.setattr(Session, "commit", raise_commit_error)

    response = client.delete(f"/books/{book_id}")

    assert response.status_code == 500
    assert response.json() == {"detail": "書籍の削除処理中に失敗しました。"}
    assert "書籍の削除に失敗しました。" in caplog.text
    assert "テスト用削除DBエラー" in caplog.text
    assert "SQLAlchemyError" in caplog.text


@pytest.mark.parametrize(
    "title, author",
    [
        (None, "テスト太郎"),
        ("テスト本", None),
    ],
)
def test_book_not_null_constraint(title, author):
    with TestingSessionLocal() as session:
        with pytest.raises(IntegrityError):
            book_db = BookDB(title=title, author=author)
            session.add(book_db)
            session.commit()
