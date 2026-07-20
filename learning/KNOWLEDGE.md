# 知識・理解確認台帳

「説明を受けた」と「自力で使える」を区別して記録する。完了判定は `ROADMAP.md` の完了条件に従う。

## Git・GitHub接続

- 状態：基礎学習済み
- 実施済み：`git init`、`.gitignore`、`git add`、初回commit、remote登録、初回push
- 接続先：`https://github.com/Shuhei-Hashizdume/FastAPIStudy.git`
- 理解確認済み：`git init`、`git add`、commit、pushの基本的な役割
- 今後の確認：変更差分を確認し、小さな単位のコミットとPull Requestを自力で行えるか確認する

## Python基礎

- 状態：学習済み
- 内容：基本文法、変数、データ型、条件分岐、ループ、関数、リスト、辞書、例外処理、クラス、インスタンス、オブジェクト指向の基礎
- 今後の確認：API実装やテストで自力使用できるか継続確認する

## FastAPI基礎

- 状態：基礎学習済み
- 内容：アプリ起動、GET、POST、パスパラメータ、クエリパラメータ、リクエストボディ、Pydantic入力、基本ステータスコード、`HTTPException`、404
- 今後の確認：類似エンドポイントを自力で設計・実装・説明できるか確認する

## SQLAlchemy・SQLite基礎

- 状態：基礎学習済み
- 内容：SQLite接続、Engine、Session、モデル、登録、`add()`、`commit()`、`refresh()`、`rollback()`、`query()`、`filter()`、`all()`、`first()`
- 理解確認済み：`commit()`、`refresh()`、`rollback()` の役割と、commit失敗後にrollbackが必要な理由
- 今後の確認：制約違反などの具体的なDB例外とクエリ効率

## IDによる1件取得と404

- 状態：学習済み・経過観察
- できていること：IDで検索し、`.first()` の結果が `None` の場合に404を返すコードがある
- 今後の確認：別の対象でも自力で実装し、正常系と異常系を説明できるか確認する

## `response_model`

- 状態：基礎学習完了・経過観察
- 理解済み：FastAPIがエンドポイント関数の戻り値を検証・整形するときに、レスポンス用Pydanticモデルを使用する
- 実装済み：POST、GET全件、GET1件、PATCH
- 動作確認済み：200、201、404、422
- 今後の確認：別のAPIでも適切なレスポンスモデルを自力設計できるか確認する

## レスポンス用Pydanticスキーマ

- 状態：基礎学習完了・経過観察
- `BookResponse` に `book_id`、`title`、`author` を定義した
- `BookRequest`、`BookDB`、`BookResponse` の役割を説明した
- 1件は `BookResponse`、複数件は `list[BookResponse]` とする理由を確認した

## `from_attributes`

- 状態：基礎学習完了・経過観察
- `ConfigDict(from_attributes=True)` を実装した
- Pydanticが `book.book_id`、`book.title`、`book.author` のような属性から値を読み取る設定だと説明できた
- DBへ保存する設定ではないことを確認した

## 更新・削除API

- 状態：基礎学習完了・経過観察
- 更新：検索、`None` 判定、部分更新、`commit()`、`refresh()`、更新後レスポンスを実装した
- 削除：検索、`None` 判定、`delete()`、`commit()`、204・404の使い分けを実装した
- 動作確認：PATCHの200・404・422、DELETEの204・404を確認した
- 今後の確認：別の要件からの自力設計と、制約違反発生時の例外処理

## HTTPレスポンスと処理主体

- 状態：基礎理解・要復習
- エンドポイントはHTTPメソッドとパスで表される窓口
- エンドポイント関数は実際の処理を行い、Pythonの値を返す
- FastAPIはエンドポイント関数を呼び出し、HTTPレスポンスを生成する
- Pydanticはモデル定義に基づく検証・変換を担当する
- SQLAlchemyはPythonオブジェクトとDB操作を橋渡しする
- UvicornはHTTP通信を受け取り、HTTPレスポンスをクライアントへ送信する

## ファイル分割と `APIRouter`

- 状態：基礎学習完了・経過観察
- `main.py` はFastAPIアプリ本体とRouterの登録を担当する
- `database.py` はDB接続、Session、Baseを担当する
- `models.py` はSQLAlchemyのDBモデルを担当する
- `schemas.py` はリクエスト・レスポンス用Pydanticモデルを担当する
- `routers/books.py` は書籍APIのエンドポイント関数を担当する
- `app.include_router(books_router)` は、書籍RouterのルートをFastAPIアプリへ登録する

## pytestとFastAPI APIテスト

- 状態：基礎学習完了・経過観察
- `TestClient` がHTTPリクエストを再現し、返ったHTTPレスポンスを検証する
- `app.dependency_overrides[get_db] = override_get_db` で、テスト中の `get_db` をテスト用DBの依存関係に置き換えた
- autouse fixtureで各テスト前後にテーブルを初期化し、テスト間の影響を防いだ
- POST、GET、PATCH、DELETE、著者絞り込みの正常系・異常系を含む9件のテストを実行した
- 今後の確認：fixtureの応用、モック、複雑なテストデータ管理

## 仮想環境・依存関係・README

- 状態：基礎学習済み
- `venv` はプロジェクトごとにPythonパッケージを分ける仮想環境
- `venv/bin` には仮想環境用の `python`、`pip`、`pytest` などの実行コマンドがある
- `requirements.txt` に必要なライブラリとバージョンを記録し、環境を再現できるようにした
- READMEに環境構築、起動、テスト、API仕様、ファイルの役割を記載した

## 環境変数とDB接続設定

- 状態：基礎学習済み・要復習
- `os.getenv("DATABASE_URL", "sqlite:///book.db")` は実行中のプロセスが持つ環境変数を読み、未設定ならSQLiteの初期値を使う
- DB接続先をコードから分けると、開発・テスト・本番で設定を切り替えやすい
- 今後の確認：OS、プロセス、環境変数の関係を自分の言葉で説明する

## ログ

- 状態：学習開始前
- 確認済み：ログがないとエラー発生箇所や原因調査が難しくなると考えた
- 次回：`print()` と `logging`、ログレベル、機密情報、例外ログを段階的に学ぶ
