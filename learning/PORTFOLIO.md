# ポートフォリオ計画

## 基礎練習プロジェクト：書籍管理API

### 位置づけ

FastAPI、Pydantic、SQLAlchemy、SQLite、PostgreSQLを使い、Web APIとデータベース操作の基礎を身につけるための練習プロジェクト。現時点では就職応募用の完成作品ではなく、今後の本格ポートフォリオに必要な基礎力を確認する場として扱う。

### 現在コード上にある機能

- 書籍登録
- 書籍一覧取得
- 著者による絞り込み
- offset・limitによるページネーション
- IDによる1件取得と404
- 書籍更新
- 書籍削除
- NOT NULL制約
- ISBNのUNIQUE制約と重複時の409レスポンス
- Pydanticによる空文字列、文字数、ISBN形式の入力検証
- AlembicによるDB構造の履歴管理
- PostgreSQL接続、外部キー、JOIN、インデックス
- 出版社名を含む書籍レスポンスと`joinedload()`によるN+1対策
- テスト専用PostgreSQLと、commit時のISBN競合を409へ変換する処理
- Argon2によるパスワードハッシュとユーザー登録
- JWTログイン、Bearer認証、`GET /users/me`
- 書籍所有者の保存と、PATCH・DELETEの所有者ベース認可
- versionを使った楽観的ロックと、本当の同時実行・分離レベルのテスト

更新・削除を含め、コードが存在するだけでは学習完了や成果物完成とは判定しない。

### 現在の到達点

- IDによる1件取得、`.first()`、404処理まで完了済みとして引き継ぐ
- `BookResponse` を作成し、POST・GET・PATCHへ `response_model` を設定済み
- DBモデルとレスポンス用Pydanticモデルを分離し、`from_attributes` を設定済み
- 1件と複数件のレスポンス型を使い分け、書籍1件のレスポンス構造を統一済み
- DELETEは204・本文なしとし、404を含めて動作確認済み
- DB接続、DBモデル、Pydanticスキーマ、Router、FastAPIアプリ本体をファイル分割済み
- `APIRouter` で書籍APIをFastAPIアプリへ登録済み
- テスト専用PostgreSQLと `TestClient` を使い、CRUD、入力境界値、DB制約、JOIN、N+1、同時実行、JWT認証、所有者認可を含む92ケースが成功
- `DATABASE_URL` を環境変数から読む構成とし、未設定時のSQLite初期値を用意済み
- `logger.exception()`で開発者向けの詳細を残し、クライアントには内部情報を隠した500レスポンスを返す
- `IntegrityError`と`SQLAlchemyError`を分け、モックと`caplog`で異常系を確認済み
- title・authorへNOT NULL制約を設定し、SQLite自身が制約違反を拒否するテストを実装済み
- Alembicのベースライン、NOT NULL変更、`stamp`、upgrade・downgradeを実装済み
- ISBNを「nullableで追加・既存データ更新・NOT NULL化」の段階に分け、安全なマイグレーションを実装済み
- POST・PATCHでISBNの重複を事前確認し、409を返すAPIを実装済み
- 空の一時DBでマイグレーションだけから最新DB構造を再現済み
- PostgreSQLへ全マイグレーションを適用し、FastAPIと`psql`の両方から読み書きと永続化を確認済み
- `publishers`とのリレーション、外部キー、JOIN、出版社名レスポンスを実装済み
- `joinedload()`とSQLAlchemyイベントによるSELECT回数テストでN+1対策を確認済み
- テスト接続先を`fastapi_study_test`へ限定し、Alembicの構造を残したまま`TRUNCATE`で行だけを初期化する安全策を実装済み
- commit時に`uq_books_isbn`違反が起きた場合も、`UniqueViolation`を判定して409へ変換する処理とテストを実装済み
- `users`テーブル、Argon2ハッシュ、重複メールの409、ログインとJWT発行・検証を実装済み
- 正常・不正・期限切れJWT、トークンなし、ユーザー不在の認証テストを実装済み
- `books.owner_id`をnullableで追加し、既存行を移行後にNOT NULL化する段階的マイグレーションを実装済み
- 書籍作成時にJWTから得たユーザーを所有者として保存し、所有者以外のPATCH・DELETEを403で拒否する認可を実装済み
- 認証済みTestClientを作るfixtureと、認可の正常系・異常系テストを実装済み
- `requirements.txt` とREADMEにより、環境構築、DBマイグレーション、起動、テスト、API仕様を他の人が確認できる
- GitHubリポジトリ `Shuhei-Hashizdume/FastAPIStudy` へ接続し、開発履歴の記録を開始済み

### 次の改善

1. CORS、秘密情報、主要なWeb API脅威を確認する
2. 現在の所有者ベース認可の対象範囲と読み取り権限を設計する
3. CRUD・認証・認可を別の要件から自力実装できるか確認する
4. READMEに認証・認可、設計理由、トレードオフを追加する

### 基礎練習プロジェクトの完了条件

- CRUDを自分で実装・説明できる
- リクエスト、レスポンス、DBモデルの役割を分けられる
- 正常系と主要な異常系をテストできる
- Session、例外処理、トランザクションを説明できる
- READMEに起動方法、API仕様、設計理由を書ける
- Must Fixを解消している

## 就職応募用ポートフォリオへの発展

書籍管理APIで基礎を確認後、利用者と解決する課題が明確な別プロジェクト、または要件を拡張したプロジェクトを作る。最低限、PostgreSQL、Alembic、認証・認可、pytest、Docker、CI、分かりやすいREADMEを含める。

評価では機能数だけでなく、次を重視する。

- なぜその機能と設計を選んだか説明できる
- Issue、ブランチ、Pull Requestに開発過程が残っている
- エラー処理、セキュリティ、トランザクションを考慮している
- テストで変更の安全性を示せる
- 改善点やトレードオフを正直に説明できる
