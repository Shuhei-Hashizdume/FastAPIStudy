# 現在の学習状況

## 現在地

- 現在のフェーズ：PostgreSQLと実務的なDB管理
- 現在のプロジェクト：書籍管理API
- 今回の終了地点：PostgreSQL接続、インデックス、外部キー・JOIN、出版社レスポンス、N+1対策を実装・確認
- 現在の学習状態：PostgreSQLでマイグレーション、CRUD、永続化、外部キー・JOINを確認し、`joinedload()`によるN+1対策を52テストで検証済み
- 次回講義：SQLiteとPostgreSQLの違い

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
- pytest 52ケースすべての成功を確認した

## 学習中・未完了

- CRUD全体を別の要件から一貫して自力実装する
- SQLiteとPostgreSQLの違いを体系的に説明する
- PostgreSQLを使う統合テストを設計する
- ISBNのチェックディジットを含む厳密な妥当性検証
- 同時リクエストによるISBN競合時も409へ変換する設計
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

## 現在の要復習

- HTTPレスポンスオブジェクト、レスポンスボディ、Pydanticモデルの違い
- スレッド、SQLiteの`check_same_thread=False`、`StaticPool`の関係
- OS、プロセス、環境変数の関係
- `fixture`、Dependency Override、テスト用DBの役割分担
- Alembicのベースライン、`stamp`、DB内の`alembic_version`の関係
- `nullable=True`とNOT NULL無効、`nullable=False`とNOT NULL有効の対応
- HTTPレスポンスオブジェクトと、その`status_code`・JSONボディの区別
- PATCHのISBN重複確認で、更新対象自身を`book_id`により除外する理由
- `commit()`内の`flush()`、DBのID生成、`refresh()`の役割の違い
- 関数定義、関数オブジェクト、コールバック、イベントリスナーの関係
- SQLAlchemyイベントの引数が検索結果ではなく実行直前の情報であること

## 次回の完了条件

- SQLiteのファイル型DBとPostgreSQLのサーバー型DBの違いを説明できる
- データ型、制約、SQL、同時実行、マイグレーションの差があることを具体例で説明できる
- SQLiteによる単体テストだけではPostgreSQL固有の動作を保証できない理由を説明できる
- PostgreSQLを使う統合テストが必要になる範囲を考えられる

## 次回開始時の講師への指示

次の3点を報告してから、目的と必要な理由を先に説明し、新しい用語を1つずつ扱う。

- 前回の終了地点：PostgreSQL接続、インデックス、外部キー・JOIN、出版社レスポンス、N+1対策を実装・確認
- 今回の講義：SQLiteとPostgreSQLの違い
- 現在のプロジェクト：書籍管理API

最初に、現在のAPIはPostgreSQL、pytestはインメモリSQLiteを使っている全体像を確認する。その後、「SQLiteの52テストが成功すれば、PostgreSQLでもすべて同じ動作になると言い切れるか」を考えてもらう。
