import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from database import get_db
from main import app

TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]
test_database_name = make_url(TEST_DATABASE_URL).database
if test_database_name != "fastapi_study_test":
    raise RuntimeError("テスト用DB fastapi_study_test 以外への接続を拒否しました。")

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=test_engine)


def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def clear_test_data():
    with test_engine.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE books, publishers, users RESTART IDENTITY")
        )
