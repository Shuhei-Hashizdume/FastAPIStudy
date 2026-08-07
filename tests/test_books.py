import pytest
from sqlalchemy import inspect, event
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import BookDB, PublisherDB
from threading import Barrier, Thread
from queue import Queue
from psycopg.errors import UniqueViolation
from tests.support import client, test_engine, TestingSessionLocal

TEST_ISBN_1 = "9780000000002"
TEST_ISBN_2 = "9780000000019"
TEST_ISBN_3 = "9780000000026"


pytestmark = pytest.mark.usefixtures("reset_database")


# 登録
def test_create_book():
    response = client.post(
        "/books",
        json={
            "title": "pytest入門",
            "author": "テスト太郎",
            "isbn": "9781234567890",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "book_id": 1,
        "title": "pytest入門",
        "author": "テスト太郎",
        "isbn": "9781234567890",
        "publisher_name": None,
        "version": 1,
    }


# 登録　異常系
def test_create_book_without_author():
    response = client.post(
        "/books",
        json={
            "title": "著者のいない本",
            "isbn": TEST_ISBN_1,
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "author"]


# 登録　  空文字テスト
@pytest.mark.parametrize(
    "title, author, error_field",
    [
        ("", "テスト太郎", "title"),
        ("テスト太郎", "", "author"),
    ],
)
def test_create_book_with_empty_error(title, author, error_field):
    response = client.post(
        "/books",
        json={
            "title": title,
            "author": author,
            "isbn": TEST_ISBN_1,
        },
    )

    assert response.status_code == 422
    response_body = response.json()
    assert response_body["detail"][0]["loc"] == ["body", error_field]


# 　登録
@pytest.mark.parametrize(
    "title, author, error_field",
    [
        ("A" * 201, "テスト太郎", "title"),
        ("テスト本", "A" * 101, "author"),
    ],
)
def test_create_book_with_too_long_field(title, author, error_field):
    response = client.post(
        "/books",
        json={
            "title": title,
            "author": author,
            "isbn": TEST_ISBN_1,
        },
    )

    assert response.status_code == 422
    response_body = response.json()
    assert response_body["detail"][0]["loc"] == ["body", error_field]
    assert response_body["detail"][0]["type"] == "string_too_long"


def test_create_book_with_max_length_fields():
    response = client.post(
        "/books",
        json={
            "title": "A" * 200,
            "author": "B" * 100,
            "isbn": TEST_ISBN_1,
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "A" * 200
    assert response.json()["author"] == "B" * 100


# 取得
def test_get_book():
    create_response = client.post(
        "/books",
        json={
            "title": "GETテスト用の本",
            "author": "取得太郎",
            "isbn": TEST_ISBN_1,
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
        "isbn": TEST_ISBN_1,
        "publisher_name": None,
        "version": 1,
    }


# 全件取得
def test_show_books():
    first_response = client.post(
        "/books",
        json={
            "title": "1冊目",
            "author": "著者A",
            "isbn": TEST_ISBN_1,
        },
    )
    assert first_response.status_code == 201

    second_response = client.post(
        "/books",
        json={
            "title": "2冊目",
            "author": "著者B",
            "isbn": TEST_ISBN_2,
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
            "isbn": TEST_ISBN_1,
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/books",
        json={
            "title": "ページネーション本B",
            "author": "著者B",
            "isbn": TEST_ISBN_2,
        },
    )

    assert second_response.status_code == 201

    third_response = client.post(
        "/books",
        json={
            "title": "ページネーション本C",
            "author": "著者C",
            "isbn": TEST_ISBN_3,
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
            "isbn": TEST_ISBN_1,
        },
    )
    assert first_response.status_code == 201

    second_response = client.post(
        "/books",
        json={
            "title": "著者Bの1冊目",
            "author": "著者B",
            "isbn": TEST_ISBN_2,
        },
    )

    assert second_response.status_code == 201

    third_response = client.post(
        "/books",
        json={
            "title": "著者Aの2冊目",
            "author": "著者A",
            "isbn": TEST_ISBN_3,
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
            "isbn": TEST_ISBN_1,
        },
    )
    assert create_response.status_code == 201

    book_id = create_response.json()["book_id"]
    current_version = create_response.json()["version"]

    response = client.patch(
        f"/books/{book_id}",
        json={"title": "変更後のタイトル", "version": current_version},
    )

    assert response.status_code == 200
    assert response.json() == {
        "book_id": book_id,
        "title": "変更後のタイトル",
        "author": "変更しない著者",
        "isbn": TEST_ISBN_1,
        "publisher_name": None,
        "version": 2,
    }


# 更新　異常系
def test_update_book_returns_409_when_version_is_stale():
    response = client.post(
        "/books",
        json={
            "title": "テスト本",
            "author": "テスト太郎",
            "isbn": "1234567899876",
        },
    )

    book_id = response.json()["book_id"]
    current_version = response.json()["version"]

    assert response.status_code == 201

    patch_response = client.patch(
        f"/books/{book_id}", json={"title": "テスト書籍", "version": current_version}
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["title"] == "テスト書籍"
    assert patch_response.json()["version"] == 2

    second_patch_response = client.patch(
        f"/books/{book_id}", json={"title": "テスト", "version": current_version}
    )

    assert second_patch_response.status_code == 409
    assert (
        second_patch_response.json()["detail"] == "該当の書籍がすでに更新されています。"
    )


# 削除　正常系
def test_delete_book():
    create_response = client.post(
        "/books",
        json={
            "title": "削除用の本",
            "author": "削除太郎",
            "isbn": TEST_ISBN_1,
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


# 登録　DBエラー　　モックテスト
def test_create_book_db_integrity_error(monkeypatch, caplog):
    def raise_commit_error(self):
        raise IntegrityError(
            "テスト用SQL",
            {},
            Exception("NOT NULL制約違反"),
        )

    monkeypatch.setattr(Session, "commit", raise_commit_error)
    response = client.post(
        "/books",
        json={
            "title": "DBエラーテスト",
            "author": "テスト太郎",
            "isbn": TEST_ISBN_1,
        },
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
            "isbn": TEST_ISBN_1,
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
            "isbn": TEST_ISBN_1,
        },
    )

    assert post_response.status_code == 201

    book_id = post_response.json()["book_id"]
    current_version = post_response.json()["version"]

    def raise_commit_error(self):
        raise SQLAlchemyError("テスト用更新DBエラー")

    monkeypatch.setattr(Session, "commit", raise_commit_error)

    response = client.patch(
        f"/books/{book_id}",
        json={"title": "更新後タイトル", "version": current_version},
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "書籍の更新処理中に失敗しました。"}
    assert "書籍の更新に失敗しました。" in caplog.text
    assert "SQLAlchemyError" in caplog.text
    assert "テスト用更新DBエラー" in caplog.text


# 削除　モックテスト
def test_delete_book_sqlalchemy_error(monkeypatch, caplog):
    api_post_response = client.post(
        "/books",
        json={
            "title": "テストA",
            "author": "著者A",
            "isbn": TEST_ISBN_1,
        },
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


# 登録　　null　パラメータ化　テスト
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
            book_db = BookDB(title=title, author=author, isbn=TEST_ISBN_1)
            session.add(book_db)
            session.commit()


def test_book_isbn_not_null_constraint():
    with TestingSessionLocal() as session:
        book_db = BookDB(title="テストA", author="著者A", isbn=None)
        session.add(book_db)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()


@pytest.mark.parametrize(
    "update_body, error_field",
    [
        ({"title": ""}, "title"),
        ({"author": ""}, "author"),
    ],
)
def test_update_book_with_empty_error(update_body, error_field):
    post_response = client.post(
        "/books",
        json={
            "title": "テスト本",
            "author": "著者A",
            "isbn": TEST_ISBN_1,
        },
    )

    assert post_response.status_code == 201

    book_id = post_response.json()["book_id"]

    response = client.patch(
        f"/books/{book_id}",
        json=update_body,
    )

    assert response.status_code == 422
    response_body = response.json()
    assert response_body["detail"][0]["loc"] == ["body", error_field]

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "テスト本"
    assert get_response.json()["author"] == "著者A"


@pytest.mark.parametrize(
    "update_body, error_field",
    [
        ({"title": "A" * 201}, "title"),
        ({"author": "A" * 101}, "author"),
    ],
)
def test_update_book_with_too_long_field(update_body, error_field):
    post_response = client.post(
        "/books",
        json={
            "title": "テストA",
            "author": "著者A",
            "isbn": TEST_ISBN_1,
        },
    )

    assert post_response.status_code == 201

    book_id = post_response.json()["book_id"]

    response = client.patch(
        f"/books/{book_id}",
        json=update_body,
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", error_field]
    assert response.json()["detail"][0]["type"] == "string_too_long"

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "テストA"
    assert get_response.json()["author"] == "著者A"


@pytest.mark.parametrize(
    "title, author, error_field",
    [
        (None, "著者A", "title"),
        ("テストA", None, "author"),
    ],
)
def test_create_book_with_null_field(title, author, error_field):
    response = client.post(
        "/books",
        json={
            "title": title,
            "author": author,
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", error_field]


@pytest.mark.parametrize(
    "update_body, expected_title, expected_author",
    [
        ({"title": None, "author": "変更後著者"}, "変更前タイトル", "変更後著者"),
        ({"title": "変更後タイトル", "author": None}, "変更後タイトル", "変更前著者"),
    ],
)
def test_update_book_with_null(update_body, expected_title, expected_author):
    post_response = client.post(
        "/books",
        json={
            "title": "変更前タイトル",
            "author": "変更前著者",
            "isbn": TEST_ISBN_1,
        },
    )

    assert post_response.status_code == 201

    book_id = post_response.json()["book_id"]
    current_version = post_response.json()["version"]

    update_body["version"] = current_version

    response = client.patch(
        f"/books/{book_id}",
        json=update_body,
    )

    assert response.status_code == 200
    assert response.json()["title"] == expected_title
    assert response.json()["author"] == expected_author

    get_response = client.get(f"/books/{book_id}")

    assert get_response.status_code == 200
    assert get_response.json()["title"] == expected_title
    assert get_response.json()["author"] == expected_author


@pytest.mark.parametrize(
    "request_body, error_field",
    [
        ({"title": "   ", "author": "著者A"}, "title"),
        ({"title": "テストB", "author": "   "}, "author"),
    ],
)
def test_create_book_with_whitespace_field(request_body, error_field):
    response = client.post(
        "/books",
        json=request_body,
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", error_field]
    assert response.json()["detail"][0]["type"] == "string_too_short"


@pytest.mark.parametrize(
    "update_body, error_field",
    [
        ({"title": "   ", "author": "変更後著者"}, "title"),
        ({"title": "変更後タイトル", "author": "   "}, "author"),
    ],
)
def test_update_book_with_whitespace_field(update_body, error_field):
    post_response = client.post(
        "/books",
        json={
            "title": "変更前タイトル",
            "author": "変更前著者",
            "isbn": TEST_ISBN_1,
        },
    )

    assert post_response.status_code == 201

    book_id = post_response.json()["book_id"]

    response = client.patch(f"/books/{book_id}", json=update_body)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", error_field]
    assert response.json()["detail"][0]["type"] == "string_too_short"

    get_response = client.get(f"/books/{book_id}")

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "変更前タイトル"
    assert get_response.json()["author"] == "変更前著者"


def test_create_book_with_surrounding_whitespace():
    response = client.post(
        "/books",
        json={
            "title": "  Python入門  ",
            "author": "  山田太郎  ",
            "isbn": TEST_ISBN_1,
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Python入門"
    assert response.json()["author"] == "山田太郎"


def test_create_book_with_isbn():
    post_response = client.post(
        "/books",
        json={
            "title": "ISBNテスト本",
            "author": "テスト著者",
            "isbn": TEST_ISBN_2,
        },
    )
    assert post_response.status_code == 201
    assert post_response.json()["isbn"] == TEST_ISBN_2

    book_id = post_response.json()["book_id"]

    response = client.get(f"/books/{book_id}")

    assert response.status_code == 200
    assert response.json() == {
        "book_id": book_id,
        "title": "ISBNテスト本",
        "author": "テスト著者",
        "isbn": TEST_ISBN_2,
        "publisher_name": None,
        "version": 1,
    }


def test_create_book_with_duplicate_isbn():
    post_response = client.post(
        "/books", json={"title": "テストA", "author": "著者A", "isbn": "9780192837465"}
    )

    assert post_response.status_code == 201

    response = client.post(
        "/books", json={"title": "テストB", "author": "著者B", "isbn": "9780192837465"}
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "同じISBNの書籍がすでに登録されています。"}


def test_book_isbn_unique_constraint():
    with TestingSessionLocal() as session:
        first_book = BookDB(title="テストA", author="著者A", isbn="1234567890123")
        session.add(first_book)
        session.commit()

        second_book = BookDB(title="テストB", author="著者B", isbn="1234567890123")
        session.add(second_book)

        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()


@pytest.mark.parametrize(
    "isbn, expected_error_type",
    [
        ("123456789012", "string_too_short"),
        ("12345678901234", "string_too_long"),
        ("123456789012A", "string_pattern_mismatch"),
    ],
)
def test_create_book_with_invalid_isbn(isbn, expected_error_type):
    response = client.post(
        "/books",
        json={
            "title": "テストA",
            "author": "著者A",
            "isbn": isbn,
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == expected_error_type


def test_update_book_isbn():
    post_response = client.post(
        "/books",
        json={
            "title": "テストA",
            "author": "著者A",
            "isbn": TEST_ISBN_1,
        },
    )

    assert post_response.status_code == 201
    book_id = post_response.json()["book_id"]
    current_version = post_response.json()["version"]

    response = client.patch(
        f"/books/{book_id}",
        json={"isbn": TEST_ISBN_2, "version": current_version},
    )

    assert response.status_code == 200
    assert response.json()["isbn"] == TEST_ISBN_2

    get_response = client.get(f"/books/{book_id}")

    assert get_response.status_code == 200
    assert get_response.json()["isbn"] == TEST_ISBN_2


def test_update_book_with_duplicate_isbn():
    first_post_response = client.post(
        "/books",
        json={
            "title": "テストA",
            "author": "著者A",
            "isbn": "1234567890123",
        },
    )

    assert first_post_response.status_code == 201

    second_post_response = client.post(
        "/books",
        json={
            "title": "テストB",
            "author": "著者B",
            "isbn": "2345678901234",
        },
    )

    assert second_post_response.status_code == 201

    book_id = second_post_response.json()["book_id"]
    current_version = second_post_response.json()["version"]

    response = client.patch(
        f"/books/{book_id}",
        json={"isbn": "1234567890123", "version": current_version},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "同じISBNの書籍がすでに登録されています。"}

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 200
    assert get_response.json()["isbn"] == "2345678901234"


def test_create_book_without_isbn():
    response = client.post(
        "/books",
        json={
            "title": "ISBNなしの本",
            "author": "テスト著者",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.json()["detail"][0]["loc"] == ["body", "isbn"]


def test_book_author_index():
    inspector = inspect(test_engine)
    indexes = inspector.get_indexes("books")
    index_names = [index["name"] for index in indexes]
    index_columns = [index["column_names"] for index in indexes]

    assert "ix_books_author" in index_names
    assert ["author"] in index_columns


def test_book_publisher_relationship():
    with TestingSessionLocal() as session:
        publisher = PublisherDB(name="技術出版")
        session.add(publisher)
        session.commit()
        session.refresh(publisher)

        book = BookDB(
            title="リレーション入門",
            author="テスト太郎",
            isbn="9780000000033",
            publisher=publisher,
        )
        session.add(book)
        session.commit()
        session.refresh(book)

        assert book.publisher_id == publisher.publisher_id
        assert book.publisher.name == "技術出版"
        assert publisher.books[0].title == "リレーション入門"

        results = (
            session.query(BookDB, PublisherDB)
            .join(
                PublisherDB,
                BookDB.publisher_id == PublisherDB.publisher_id,
            )
            .all()
        )

        joined_book, joined_publisher = results[0]

        assert joined_book.title == "リレーション入門"
        assert joined_publisher.name == "技術出版"


def test_book_publisher_foreign_key_constraint():
    with TestingSessionLocal() as session:
        book = BookDB(
            title="外部キー違反の本",
            author="テスト太郎",
            isbn="9780000000040",
            publisher_id=999,
        )
        session.add(book)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()


def test_left_outer_join_includes_book_without_publisher():
    with TestingSessionLocal() as session:
        book = BookDB(
            title="出版社なしの本",
            author="テスト太朗",
            isbn="9780000000057",
        )
        session.add(book)
        session.commit()
        session.refresh(book)

        results = (
            session.query(BookDB, PublisherDB)
            .outerjoin(
                PublisherDB,
                BookDB.publisher_id == PublisherDB.publisher_id,
            )
            .all()
        )

        joined_book, joined_publisher = results[0]

        assert joined_book.title == "出版社なしの本"
        assert joined_publisher is None


def test_get_book_returns_publisher_name():
    with TestingSessionLocal() as session:
        publisher = PublisherDB(name="技術出版")
        session.add(publisher)
        session.commit()
        session.refresh(publisher)

        book = BookDB(
            title="テストA",
            author="テスト太郎",
            isbn="1234567890987",
            publisher=publisher,
        )
        session.add(book)
        session.commit()
        session.refresh(book)

        book_id = book.book_id

        response = client.get(f"/books/{book_id}")

        assert response.status_code == 200
        assert response.json()["publisher_name"] == "技術出版"


def test_list_books_loads_publishers_in_one_select():
    select_statements = []

    def record_select(
        _connection,
        _cursor,
        statement,
        _parameters,
        _context,
        _executemany,
    ):
        if statement.lstrip().upper().startswith("SELECT"):
            select_statements.append(statement)

    with TestingSessionLocal() as session:
        publisher_a = PublisherDB(name="出版社A")
        publisher_b = PublisherDB(name="出版社B")

        session.add(publisher_a)
        session.add(publisher_b)
        session.commit()
        session.refresh(publisher_a)
        session.refresh(publisher_b)

        book_a = BookDB(
            title="書籍A", author="著者A", isbn="9780000000071", publisher=publisher_a
        )

        book_b = BookDB(
            title="書籍B", author="著者B", isbn="9780000000088", publisher=publisher_b
        )

        session.add(book_a)
        session.add(book_b)
        session.commit()

    event.listen(
        test_engine,
        "before_cursor_execute",
        record_select,
    )

    try:
        response = client.get("/books")
    finally:
        event.remove(
            test_engine,
            "before_cursor_execute",
            record_select,
        )
    assert response.status_code == 200

    response_body = response.json()

    assert len(response_body) == 2
    assert response_body[0]["publisher_name"] == "出版社A"
    assert response_body[1]["publisher_name"] == "出版社B"
    assert len(select_statements) == 1


def test_create_book_returns_409_when_unique_constraint_fails(monkeypatch):
    with TestingSessionLocal() as session:
        existing_book = BookDB(
            title="既存の本",
            author="既存の著者",
            isbn=TEST_ISBN_1,
        )
        session.add(existing_book)
        session.commit()

    def return_none(_query):
        return None

    monkeypatch.setattr(
        Query,
        "first",
        return_none,
    )

    response = client.post(
        "/books",
        json={
            "title": "重複する本",
            "author": "別の著者",
            "isbn": TEST_ISBN_1,
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "同じISBNの書籍がすでに登録されています。"}


def test_uncommitted_book_is_not_visible_to_other_session():
    with (
        TestingSessionLocal() as session_a,
        TestingSessionLocal() as session_b,
    ):
        book = BookDB(
            title="未確定の本",
            author="テスト著者",
            isbn=TEST_ISBN_1,
        )
        session_a.add(book)
        session_a.flush()

        book_seen_by_a = (
            session_a.query(BookDB).filter(BookDB.isbn == TEST_ISBN_1).first()
        )

        assert book_seen_by_a is not None

        book_seen_by_b = (
            session_b.query(BookDB).filter(BookDB.isbn == TEST_ISBN_1).first()
        )

        assert book_seen_by_b is None

        session_a.commit()

        book_seen_by_b_after_commit = (
            session_b.query(BookDB).filter(BookDB.isbn == TEST_ISBN_1).first()
        )

        assert book_seen_by_b_after_commit is not None


def test_repeatable_read_keeps_same_snapshot_until_transaction_ends():
    with (
        TestingSessionLocal() as session_a,
        TestingSessionLocal() as session_b,
    ):
        connection_b = session_b.connection(
            execution_options={"isolation_level": "REPEATABLE READ"}
        )
        assert connection_b.get_isolation_level() == "REPEATABLE READ"

        book_before_commit = (
            session_b.query(BookDB).filter(BookDB.isbn == TEST_ISBN_1).first()
        )

        assert book_before_commit is None

        book = BookDB(
            title="追加本",
            author="テスト著者",
            isbn=TEST_ISBN_1,
        )
        session_a.add(book)
        session_a.commit()

        book_after_commit = (
            session_b.query(BookDB).filter(BookDB.isbn == TEST_ISBN_1).first()
        )

        assert book_after_commit is None

        session_b.commit()

        book_in_new_transaction = (
            session_b.query(BookDB).filter(BookDB.isbn == TEST_ISBN_1).first()
        )

        assert book_in_new_transaction is not None


def test_two_sessions_compete_for_same_isbn():
    barrier = Barrier(2)
    results: Queue[str] = Queue()

    def register_book():
        with TestingSessionLocal() as session:
            existing_book = (
                session.query(BookDB).filter(BookDB.isbn == TEST_ISBN_1).first()
            )
            if existing_book is not None:
                results.put("precheck_found")
                return
            barrier.wait(timeout=5)

            book = BookDB(
                title="同時登録される本", author="テスト著者", isbn=TEST_ISBN_1
            )
            session.add(book)

            try:
                session.commit()
                results.put("committed")
            except IntegrityError as error:
                session.rollback()

                if (
                    isinstance(error.orig, UniqueViolation)
                    and error.orig.diag.constraint_name == "uq_books_isbn"
                ):
                    results.put("conflict")
                else:
                    results.put("unexpected_integrity_error")

    thread_a = Thread(target=register_book)
    thread_b = Thread(target=register_book)

    thread_a.start()
    thread_b.start()

    thread_a.join(timeout=10)
    thread_b.join(timeout=10)

    assert thread_a.is_alive() is False
    assert thread_b.is_alive() is False

    actual_results = sorted(
        [
            results.get(timeout=1),
            results.get(timeout=1),
        ]
    )

    assert actual_results == ["committed", "conflict"]

    with TestingSessionLocal() as session:
        saved_books = session.query(BookDB).filter(BookDB.isbn == TEST_ISBN_1).all()

        assert len(saved_books) == 1


def test_update_book_returns_422_when_version_is_missing():
    post_response = client.post(
        "/books",
        json={
            "title": "テスト本A",
            "author": "テスト太郎",
            "isbn": "1234567899876",
        },
    )

    assert post_response.status_code == 201

    book_id = post_response.json()["book_id"]

    response = client.patch(
        f"/books/{book_id}",
        json={
            "title": "テスト本B",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.json()["detail"][0]["loc"] == ["body", "version"]


def test_update_book_returns_422_when_version_is_zero():
    post_response = client.post(
        "/books",
        json={
            "title": "テスト本A",
            "author": "テスト太郎",
            "isbn": "1234567899876",
        },
    )

    assert post_response.status_code == 201

    book_id = post_response.json()["book_id"]

    response = client.patch(
        f"/books/{book_id}", json={"title": "テスト本B", "version": 0}
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "greater_than_equal"
    assert response.json()["detail"][0]["loc"] == ["body", "version"]


def test_two_requests_compete_to_update_same_book():

    barrier = Barrier(2)
    results: Queue[int] = Queue()

    post_response = client.post(
        "/books",
        json={
            "title": "テスト本A",
            "author": "テスト太郎",
            "isbn": "1234567899876",
        },
    )

    assert post_response.status_code == 201

    book_id = post_response.json()["book_id"]
    current_version = post_response.json()["version"]

    def update_book_in_thread(title: str):
        barrier.wait(timeout=5)

        response = client.patch(
            f"/books/{book_id}",
            json={
                "title": title,
                "version": current_version,
            },
        )

        results.put(response.status_code)

    thread_a = Thread(target=update_book_in_thread, args=("テスト書籍A",))
    thread_b = Thread(target=update_book_in_thread, args=("テスト書籍B",))

    thread_a.start()
    thread_b.start()

    thread_a.join(timeout=10)
    thread_b.join(timeout=10)

    assert thread_a.is_alive() is False
    assert thread_b.is_alive() is False

    actual_results = sorted(
        [
            results.get(timeout=1),
            results.get(timeout=1),
        ]
    )

    assert actual_results == [200, 409]

    get_response = client.get(f"/books/{book_id}")

    assert get_response.status_code == 200
    assert get_response.json()["version"] == 2
    assert get_response.json()["title"] in ["テスト書籍A", "テスト書籍B"]
