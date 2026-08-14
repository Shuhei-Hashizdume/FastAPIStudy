# 現在の学習状況

## 現在地

- 現在のフェーズ：認証・セキュリティ
- 現在のプロジェクト：書籍管理API
- 今回の終了地点：CORS、秘密情報の分離、主要なWeb API脅威の基礎を実装・説明し、全件テスト成功を確認
- 現在の学習状態：JWT認証と所有者認可に加え、CORSの正常系・異常系テスト、`.env`除外、`.env.example`、主要脅威と既存対策の対応付けまで確認
- 次回講義：認可設計の仕上げとして、書籍読み取りAPIの公開範囲を整理する

## 今回完了した項目

- `CORSMiddleware`で許可オリジン・HTTPメソッド・ヘッダーを明示した
- 許可済み・未許可オリジンのプリフライトと、実際のGETレスポンスのCORSヘッダーを3件のテストで確認した
- `.env`をGitの対象外にし、安全な見本だけを`.env.example`で共有する構成を追加した
- JWT秘密鍵漏えい、BOLA、プロパティ単位の認可不備、リソース消費、設定不備、SQLインジェクション、レスポンス・エラーの情報漏えいを既存実装と結び付けて説明した
- CORS追加後もpytest全件成功を確認した
- Argon2を使ったパスワードのハッシュ化・検証と、平文パスワードを保存しないユーザー登録を実装した
- JWTの発行・署名検証・有効期限検証と、Bearer認証によるログイン中ユーザー取得を実装した
- `/users/me`の正常系、トークンなし、不正・期限切れJWT、DBにユーザーがいない異常系をテストした
- `books.owner_id`をnullableで追加し、既存行を移行してからNOT NULL化する2段階のAlembicマイグレーションを実施した
- `POST /books`を認証必須にし、クライアント入力ではなくJWTから得た`current_user.user_id`を所有者として保存した
- PATCH・DELETEで`owner_id`と`current_user.user_id`を比較し、所有者以外を403で拒否した
- `authenticated_client` fixtureでユーザー登録・ログイン・Authorizationヘッダー設定・後片付けを共通化した
- 広すぎる`Query.first()`モックを`find_book_by_isbn()`だけのモックへ狭め、認証用ユーザー検索への副作用を防いだ
- 本当の2スレッド同時ISBN登録、REPEATABLE READ、versionによる楽観的ロックを実装・確認した
- pytest 92ケースすべての成功を確認した

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
- 認可を別要件から自力で設計・実装する確認
- レート制限の実装と、本番環境での秘密情報管理サービスの利用
- Docker

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
- 認証は「誰か」、認可は「その操作をしてよいか」を確認する処理だと説明できる
- `HTTPBearer`、`Depends(get_current_user)`、JWT、`sub`、UserDB検索の実行順を説明できる
- ResponseオブジェクトとPydanticレスポンスモデル、JSONボディ、Headersオブジェクトを区別できる
- 外部キーは代入を可能にするものではなく、参照先IDの存在をDBで保証すると説明できる
- fixtureの戻り値を引数で受け取る場合と、`usefixtures`で準備処理だけを使う場合を区別できる
- モックは対象を狭くし、置き換え先と同じ引数形式を受け取れる必要があると説明できる
- CORSミドルウェアが許可ヘッダーを追加し、ブラウザがJavaScriptへレスポンスを渡すか判断する流れを説明できる
- `.env.example`は必要な環境変数名を共有する見本であり、実際の秘密情報を読み込ませるファイルではないと説明できる
- `book_id`による対象特定と、`owner_id`による操作権限確認を区別できる
- ページネーションの件数上限と、単位時間あたりのレート制限が守る範囲の違いを説明できる
- SQLAlchemyのパラメータバインディングがSQLと入力値を分離する理由を説明できる

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
- fixtureの実行順、`yield`前後の準備・後片付け、共有TestClientの状態管理
- 位置引数とキーワード引数、およびモック関数のシグネチャの対応
- 認可の403と、認証失敗の401の停止地点の違い

## 次回の完了条件

- 書籍一覧・1件取得を公開情報にするか、認証・所有者制限を付けるか要件から判断する
- 読み取りと変更・削除で認可方針が異なり得る理由を説明する
- 決定した認可方針をテストで示し、全件テストを成功させる

## 次回開始時の講師への指示

次の3点を報告してから、目的と必要な理由を先に説明し、新しい用語を1つずつ扱う。

- 前回の終了地点：CORS設定と3件のテスト、秘密情報の分離、主要なWeb API脅威の基礎を確認し、全件テスト成功
- 今回の講義：書籍読み取りAPIの公開範囲を決め、認可設計を仕上げる
- 現在のプロジェクト：書籍管理API

最初に、現在のGET・POST・PATCH・DELETEの認証・認可条件を表にせず1項目ずつ確認する。その後、書籍情報を誰へ公開するAPIなのかを要件から決め、必要なテストへ進む。
