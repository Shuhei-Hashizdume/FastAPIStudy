# ポートフォリオ計画

## 基礎練習プロジェクト：書籍管理API

### 位置づけ

FastAPI、Pydantic、SQLAlchemy、SQLiteを使い、Web APIとデータベース操作の基礎を身につけるための練習プロジェクト。現時点では就職応募用の完成作品ではなく、今後の本格ポートフォリオに必要な基礎力を確認する場として扱う。

### 現在コード上にある機能

- 書籍登録
- 書籍一覧取得
- 著者による絞り込み
- offset・limitによるページネーション
- IDによる1件取得と404
- 書籍更新
- 書籍削除
- NOT NULL制約
- AlembicによるDB構造の履歴管理

更新・削除を含め、コードが存在するだけでは学習完了や成果物完成とは判定しない。

### 現在の到達点

- IDによる1件取得、`.first()`、404処理まで完了済みとして引き継ぐ
- `BookResponse` を作成し、POST・GET・PATCHへ `response_model` を設定済み
- DBモデルとレスポンス用Pydanticモデルを分離し、`from_attributes` を設定済み
- 1件と複数件のレスポンス型を使い分け、書籍1件のレスポンス構造を統一済み
- DELETEは204・本文なしとし、404を含めて動作確認済み
- DB接続、DBモデル、Pydanticスキーマ、Router、FastAPIアプリ本体をファイル分割済み
- `APIRouter` で書籍APIをFastAPIアプリへ登録済み
- テスト用インメモリDBと `TestClient` を使い、CRUD、絞り込み、ページネーション、DB例外、NOT NULL制約を含む18ケースが成功
- `DATABASE_URL` を環境変数から読む構成とし、未設定時のSQLite初期値を用意済み
- `logger.exception()`で開発者向けの詳細を残し、クライアントには内部情報を隠した500レスポンスを返す
- `IntegrityError`と`SQLAlchemyError`を分け、モックと`caplog`で異常系を確認済み
- title・authorへNOT NULL制約を設定し、SQLite自身が制約違反を拒否するテストを実装済み
- Alembicのベースライン、NOT NULL変更、`stamp`、upgrade・downgradeを実装済み
- 空の一時DBでマイグレーションだけから最新DB構造を再現済み
- `requirements.txt` とREADMEにより、環境構築、DBマイグレーション、起動、テスト、API仕様を他の人が確認できる
- GitHubリポジトリ `Shuhei-Hashizdume/FastAPIStudy` へ接続し、開発履歴の記録を開始済み

### 次の改善

1. 空文字列・文字数を含む入力バリデーションとエラーレスポンスを設計する
2. CRUD全体を別の要件から自力実装できるか確認する
3. 一意制約、外部キー、JOIN、インデックスを追加する
4. PostgreSQLへ移行し、SQLiteとの違いを説明する
5. READMEに設計理由とトレードオフを追加する

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
