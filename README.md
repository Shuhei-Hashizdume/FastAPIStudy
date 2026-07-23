# FastAPIStudy

Pythonバックエンドエンジニアとしての就職と、ジュニアエンジニアとして実務へ参加できる状態を目指す学習リポジトリです。現在はPython、FastAPI、SQLAlchemy、SQLiteを使った書籍管理APIで学習しています。

## 現在地

最新の学習状況と次回の開始地点は、[learning/PROGRESS.md](learning/PROGRESS.md) を参照してくださ
い。

## 学習記録

- [ロードマップ](learning/ROADMAP.md)
- [現在の進捗](learning/PROGRESS.md)
- [セッション履歴](learning/SESSION_LOG.md)
- [苦手・要復習](learning/WEAKNESSES.md)
- [理解済み知識](learning/KNOWLEDGE.md)
- [就職・実務到達度](learning/JOB_READINESS.md)
- [ポートフォリオ計画](learning/PORTFOLIO.md)

## 初期移行の方針と結果

- 既存の書籍管理APIと、従来の指導・レビュー方針は残す
- コードが存在する項目と、学習完了条件を通過した項目を区別する
- IDによる1件取得、`.first()`、404処理までを完了済みとして引き継ぐ
- 初期移行時点では、`response_model` を基本説明まで進んだ「学習中」とした
- 初期移行時点では、レスポンス用スキーマ、`from_attributes`、更新・削除の理解確認などを推測で完了にしなかった
- 正確な日付が不明な履歴は `SESSION_LOG.md` に「移行時初期記録」として残す
- `ROADMAP.md` と `PROGRESS.md` の現在地を「PydanticスキーマとAPIレスポンス設計」に統一する

この初期移行では学習管理システムの構築だけを行い、`response_model` の講義や完成コードの追加は行っていません。

## 運用ルール

講義とレビューの進め方は [AGENTS.md](AGENTS.md) に定義しています。学習記録を更新する際は、各項目の完了条件を確認し、不明な履歴を推測で完了にしません。

## 環境構築

このプロジェクトはPython 3.14で動作確認しています。

仮想環境を作成します。

```bash
python -m venv venv
```

必要なパッケージをインストールします。

```bash
./venv/bin/python -m pip install -r requirements.txt
```

Alembicのマイグレーションを適用し、最新のDB構造を作成します。

```bash
./venv/bin/alembic upgrade head
```

## 環境変数

DBの接続先は、`DATABASE_URL`環境変数で変更できます。

環境変数を指定しない場合は、開発用の`sqlite:///book.db`を使用します。

別のSQLiteファイルを使用する例：

```bash
DATABASE_URL="sqlite:///other.db" ./venv/bin/python -m uvicorn main:app --reload
```

認証情報や秘密鍵などの機密情報は、コードやREADMEへ直接記載しないでください。

## DBマイグレーション

DB構造の作成・変更履歴はAlembicで管理します。FastAPIの起動時には
`Base.metadata.create_all()`を実行しないため、初回起動前やマイグレーション追加後に次を実行します。

```bash
./venv/bin/alembic upgrade head
```

現在適用されているrevisionを確認します。

```bash
./venv/bin/alembic current
```

マイグレーションファイルを自動生成する場合は、SQLAlchemyモデルを変更した後に次を実行します。
生成された`upgrade()`と`downgrade()`は、適用前に必ずレビューします。

```bash
./venv/bin/alembic revision --autogenerate -m "変更内容"
```

既存の`book.db`は、Alembic導入時のベースラインへ`stamp`したうえでNOT NULL制約を適用済みです。
新しい空のDBでは、ベースラインから最新revisionまでを`upgrade head`で再現できます。

## アプリの起動

UvicornでFastAPIアプリを起動します。

```bash
./venv/bin/python -m uvicorn main:app --reload
```

起動後、Swagger UIを開きます。

```text
http://127.0.0.1:8000/docs
```

## テスト

pytestでAPIテストを実行します。

```bash
./venv/bin/python -m pytest -v
```

テストでは開発用の`book.db`ではなく、テスト用のインメモリSQLiteを使用します。

## API一覧

| HTTPメソッド | パス               | 処理                                 | 主なステータスコード |
| ------------ | ------------------ | ------------------------------------ | -------------------- |
| POST         | `/books`           | 書籍を登録                           | 201、422             |
| GET          | `/books`           | 書籍一覧取得、著者絞り込み、ページネーション | 200、422        |
| GET          | `/books/{book_id}` | IDを指定して書籍を1件取得            | 200、404             |
| PATCH        | `/books/{book_id}` | IDを指定して書籍を部分更新           | 200、404、422        |
| DELETE       | `/books/{book_id}` | IDを指定して書籍を削除               | 204、404             |

### `{book_id}`の意味

`/books/{book_id}`

`{book_id}`はパスパラメータです。

例えば、IDが5なら実際のURLは`/books/5`です。

### 著者で絞り込む場合

著者で絞り込む場合は、`author`クエリパラメータを使用します。例：`GET /books?author=著者A`

ページネーションには`offset`と`limit`を使用します。`offset`は0以上、`limit`は1以上100以下です。

```text
GET /books?offset=0&limit=20
```

## 現在のアプリ

FastAPI、SQLAlchemy、SQLiteを使用した書籍管理APIです。書籍の登録、取得、部分更新、削除に対応して
います。

| ファイル              | 役割                                                      |
| --------------------- | --------------------------------------------------------- |
| `main.py`             | FastAPIアプリの作成、書籍用Routerの登録                    |
| `database.py`         | SQLiteへの接続設定とSession管理                           |
| `models.py`           | SQLAlchemyによるDBモデルの定義                            |
| `schemas.py`          | Pydanticによるリクエスト・レスポンススキーマの定義        |
| `routers/books.py`    | 書籍APIのエンドポイント                                   |
| `tests/test_books.py` | 書籍APIの正常系・異常系テスト                             |
| `alembic/`            | DB構造の変更履歴とマイグレーション実行設定                 |
| `alembic.ini`         | Alembic全体の設定                                          |
| `requirements.txt`    | 必要なPythonパッケージとバージョン                        |
