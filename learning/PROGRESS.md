# 現在の学習状況

## 現在地

- 現在のフェーズ：PostgreSQLと実務的なDB管理
- 現在のプロジェクト：書籍管理API
- 今回の終了地点：テスト専用PostgreSQLへの統合テスト移行と、同時ISBN登録時の409変換を実装・確認
- 現在の学習状態：Alembicで作ったテストDB構造を維持し、行だけを初期化する53件のPostgreSQLテストが成功。commit時のISBN UNIQUE制約違反も409へ変換済み
- 次回講義：本当の同時実行とトランザクション分離レベルの基礎

## 今回完了した項目

- `author`へインデックスを追加し、検索速度の利点と書き込み・容量面のコストを確認した
- Alembicで`ix_books_author`を追加し、DB構造とテストから存在を確認した
- `psycopg`を導入し、`DATABASE_URL`を使ってPostgreSQLへ接続した
- PostgreSQLへ全マイグレーションを適用し、`f481e0cbd250 (head)`を確認した
- FastAPIからPOST・GETを実行し、PostgreSQLへの書き込み、読み取り、再起動後の永続化を確認した
- `psql`でテーブル、行データ、シーケンス、制約、インデックスを直接確認した
- `publishers`テーブルと`books.publisher_id`の外部キーを追加した
- SQLAlchemyの`relationship()`と`back_populates`で書籍と出版社を双方向に関連付けた
- SQLの`JOIN`で書籍名と出版社名を結合して取得した
- `BookDB.publisher_name` propertyと`BookResponse.publisher_name`で出版社名をAPIレスポンスへ追加した
- `joinedload(BookDB.publisher)`で一覧取得時のN+1問題を防いだ
- SQLAlchemyのイベントリスナーでSELECT回数を記録し、出版社付き2冊を1回のSELECTで取得するテストを追加した
- 開発用`fastapi_study`とテスト用`fastapi_study_test`を分離した
- `TEST_DATABASE_URL`のDB名を検査し、開発用DBへのテスト接続を拒否する安全確認を追加した
- Alembicでテスト用DBの構造を再現し、pytestのDB依存テストをPostgreSQLへ移行した
- `TRUNCATE TABLE books, publishers RESTART IDENTITY`でDB構造を残し、行だけを各テスト前後に初期化した
- `UniqueViolation`と制約名`uq_books_isbn`を確認し、commit時のISBN競合を409へ変換した
- API側の事前検索を通過した状況を`monkeypatch`で再現する競合テストを追加した
- pytest 53ケースすべての成功を確認した

## 学習中・未完了

- CRUD全体を別の要件から一貫して自力実装する
- ISBNのチェックディジットを含む厳密な妥当性検証
- 本当に複数処理を並列実行するテスト
- 同時更新とトランザクション分離レベル
- 認証、Docker

## 現在の強み

- FastAPI、Pydantic、SQLAlchemy、SQLite、Alembic、クライアントの担当を分けて説明できる
- `commit()`失敗時の`rollback()`、ログ記録、安全なHTTPレスポンスへの変換を実装できる
- モックでDB例外を再現し、レスポンスとログの両方を検証できる
- `offset`と`limit`を使ったページネーションと、DB側で絞り込む理由を説明できる
- Pydanticの検証とDBのNOT NULL制約がデータを守る場所の違いを説明できる
- Pydanticの入力検証とDBのUNIQUE制約を併用する理由を説明できる
- 主キーの`book_id`と、業務上の識別子であるISBNの役割の違いを説明できる
- 422と409を入力形式の不正・現在のDB状態との競合として使い分けられる
- ベースライン、revision、`stamp`、`upgrade`、`downgrade`の基本的な流れを説明・実行できる
- コード変更後に対象テストと全件テストを実行する習慣がある
- PostgreSQLへの接続経路をFastAPI、SQLAlchemy、Engine、`psycopg`、PostgreSQLに分けて説明できる
- 外部キーと`relationship()`のDB側・Python側の役割を区別できる
- N+1問題が発生する流れと`joinedload()`による事前読み込みを説明できる
- SQLiteとPostgreSQLの違いを、ファイル型・サーバー型、外部キー、同時書き込み、マイグレーション、型の具体例で説明できる
- AlembicはDB構造、pytest fixtureは行データの初期化を担当すると説明できる
- API側の重複検索は早期確認、PostgreSQLのUNIQUE制約は同時登録も防ぐ最後の防御と説明できる

## 現在の要復習

- HTTPレスポンスオブジェクト、レスポンスボディ、Pydanticモデルの違い
- スレッド、SQLiteの`check_same_thread=False`、`StaticPool`の関係
- OS、プロセス、環境変数の関係
- Alembicのベースライン、`stamp`、DB内の`alembic_version`の関係
- `nullable=True`とNOT NULL無効、`nullable=False`とNOT NULL有効の対応
- HTTPレスポンスオブジェクトと、その`status_code`・JSONボディの区別
- PATCHのISBN重複確認で、更新対象自身を`book_id`により除外する理由
- `commit()`内の`flush()`、DBのID生成、`refresh()`の役割の違い
- 関数定義、関数オブジェクト、コールバック、イベントリスナーの関係
- SQLAlchemyイベントの引数が検索結果ではなく実行直前の情報であること
- `IntegrityError`、`error.orig`、psycopgの`UniqueViolation`の関係
- 競合の再現テストと、本当に並列実行するテストの違い

## 次回の完了条件

- トランザクション分離レベルが、同時処理から見えるデータを制御する設定だと説明できる
- 今回の競合再現と、本当の並列実行テストの違いを説明できる
- PostgreSQL上で同時処理を確認する小さなテストを実装する
- 対象テストと全件テストを成功させる

## 次回開始時の講師への指示

次の3点を報告してから、目的と必要な理由を先に説明し、新しい用語を1つずつ扱う。

- 前回の終了地点：テスト専用PostgreSQLへの移行と、commit時のISBN競合を409へ変換する処理を実装・確認
- 今回の講義：本当の同時実行とトランザクション分離レベルの基礎
- 現在のプロジェクト：書籍管理API

最初に、今回の`monkeypatch`テストが本当に2つの処理を同時実行してはいない理由を確認する。その後、トランザクション分離レベルと同時処理から見えるデータの関係を1項目ずつ扱う。
