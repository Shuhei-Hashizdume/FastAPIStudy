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
- 理解確認済み：`Query`オブジェクトへ条件、並び順、offset、limitを積み上げ、`.all()`でSQLを実行する流れ
- 理解確認済み：`IntegrityError`はDB制約違反、`SQLAlchemyError`はSQLAlchemy関連例外の広い親クラス
- 実装・確認済み：title・author・isbnのNOT NULL制約、isbnのUNIQUE制約、実際のSQLiteによる制約違反
- 理解確認済み：主キーは行を識別する中心的なキー、UNIQUE制約は指定カラムの重複を禁止する
- 理解確認済み：API側の事前確認は分かりやすい409を返し、DB制約はAPIを通らない書き込みも防ぐ
- 今後の確認：外部キー、JOIN、インデックス

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
- `monkeypatch`で`Session.commit()`を置き換え、POST・PATCH・DELETEのDBエラーを再現した
- `caplog`でログメッセージ、例外クラス、元の例外メッセージを検証した
- `pytest.raises`で実際の`IntegrityError`、`pytest.mark.parametrize`で複数入力を検証した
- CRUD、絞り込み、ページネーション、入力境界値、422、404、409、500、DB制約、外部キー、JOIN、N+1対策、commit時のISBN競合を含む53ケースをPostgreSQLで実行した
- 今後の確認：複雑なfixture設計とテストデータの共通化

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
- `.env`は実際の秘密情報を含み得るため`.gitignore`で除外し、`.env.example`には必要な環境変数名と安全な見本値だけを記録する
- `.env.example`は説明書であり、現在のコードが自動的に読み込む設定ではない
- テストでは`monkeypatch.setenv()`が一時的なJWT秘密鍵を設定し、Uvicornでの手動確認では実行環境から別途値を渡す
- 今後の確認：OS、プロセス、環境変数の関係を自分の言葉で説明する

## ログ

- 状態：基礎学習完了・経過観察
- `logging.getLogger(__name__)`でモジュール名付きLoggerを取得した
- `logger.exception()`を`except`内で使い、ERRORレベル、メッセージ、例外情報、スタックトレースを記録した
- 開発者向けログには詳しい原因を残し、クライアント向けHTTPレスポンスには内部情報を出さない理由を説明した
- POST・PATCH・DELETEのDBエラーをログと安全な500レスポンスへ分けた
- `caplog`と`--log-cli-level=ERROR`で例外ログを確認した
- 今後の確認：リクエストID、構造化ログ、運用環境での出力先

## ページネーションとクエリ効率

- 状態：基礎学習完了・経過観察
- `offset`は読み飛ばす件数、`limit`は取得上限件数
- `order_by(BookDB.book_id)`でページ間の並び順を安定させた
- 著者条件をPython側ではなくDBクエリへ追加し、必要なレコードだけ取得する理由を説明した
- `Query(ge=0)`、`Query(ge=1, le=100)`で不正なoffset・limitを422にした
- 今後の確認：大量offsetの弱点、カーソル方式、実行計画、インデックス

## DB制約とAlembic

- 状態：基礎学習完了・経過観察
- PydanticはAPIの入口・出口、NOT NULL制約はDB保存時のデータを守る
- `Base.metadata.create_all()`は存在しないテーブルを作るが、既存テーブルの構造変更履歴は管理しない
- AlembicのマイグレーションファイルはDB構造の変更手順、`alembic_version`は各DBの適用済み現在地を表す
- ベースラインは空のDBから最初の構造を再現するための基準点
- `stamp`は既存DBへ変更処理を実行せず、現在地だけを記録する
- `upgrade()`と`downgrade()`を実装・レビューし、一時DBで`base → head → base → head`を確認した
- SQLiteのテーブル変更に`render_as_batch=True`を使い、一時テーブルへのコピー方式を学んだ
- 今後の確認：新しいカラムや制約を自力でマイグレーションし、PostgreSQLとの差を説明する

## 入力バリデーションとISBN

- 状態：基礎学習完了・経過観察
- `Field(min_length=..., max_length=...)`でtitle・authorの文字数を制限した
- `ConfigDict(str_strip_whitespace=True)`で文字列の前後の空白を除去し、空白だけの入力を空文字列として拒否した
- FastAPIはPydanticの検証に失敗したリクエストについて、エンドポイント関数を呼ばずに422レスポンスを生成する
- POSTではISBNを必須の13桁数字とし、PATCHでは未指定を許可しつつ、指定された場合だけ同じ制約を適用した
- 422は入力形式・型・必須条件への違反、409は正しい形式の入力が現在のDB状態と競合した場合に使用した
- `pattern=r"^[0-9]+$"`は先頭から末尾までASCII数字だけで構成されることを検証する
- 現在の検証は13桁数字の形式確認であり、ISBNのチェックディジットまでは検証していない

## ISBNの段階的マイグレーション

- 状態：基礎学習完了・経過観察
- 既存行があるテーブルへ必須カラムを一度に追加すると、既存行に値がなく制約違反になる
- そのため「nullableなISBNカラムとUNIQUE制約を追加」「既存データへISBNを設定」「ISBNをNOT NULL化」の順で移行した
- `58bb8935c9ad`でISBNカラムとUNIQUE制約、`de1c8b4db0bb`でNOT NULL制約を追加した
- upgrade・downgradeの往復、開発DBのhead更新、`alembic check`を確認した
- 今後の確認：別の既存データ移行でも、安全な段階を自力で設計できるか確認する

## PostgreSQL接続と永続化

- 状態：基礎学習完了・経過観察
- `source venv/bin/activate`はプロジェクト用Python環境、`DATABASE_URL`はDB接続先を現在のターミナルから子プロセスへ渡す
- SQLAlchemyのEngineは`psycopg`を介してPostgreSQLサーバーへ接続する
- `psql -h localhost -d fastapi_study`はローカルのPostgreSQL内にある`fastapi_study`へ直接接続する
- PostgreSQLはサーバープロセスが専用のデータ領域を管理し、FastAPIを停止しても行データを保持する
- `alembic current`の`head`は行データではなく、適用済みDB構造の現在地を示す
- シーケンスは次に発行する主キー番号を管理し、テーブルの行数を表すものではない
- 理解確認済み：SQLiteとPostgreSQLは、ファイル型・サーバー型、外部キー、同時書き込み、マイグレーション、型の扱いが異なる
- 理解確認済み：SQLiteで成功したテストがPostgreSQLでも必ず成功するとは限らない
- 今後の確認：テスト専用PostgreSQLを安全に構築し、DB依存テストを移行する

## テスト用DBの運用方針

- 状態：基礎学習完了・経過観察
- DBへ依存しないPydanticモデルやPython関数はDBなしの単体テストで確認する
- FastAPI、SQLAlchemy、DB制約、JOIN、マイグレーション、トランザクション、N+1対策はテスト専用PostgreSQLを使う統合テストで確認する
- 開発用`fastapi_study`とテスト用`fastapi_study_test`を分離する
- インメモリSQLiteの成功だけでPostgreSQL上の動作を保証したと判定しない
- 学習上の新しい専門用語には、初回説明時に読み仮名を付ける
- `TEST_DATABASE_URL`からDB名を取り出し、`fastapi_study_test`以外ならテスト収集時に停止する安全確認を実装した
- AlembicでテストDBを`head`まで構築し、pytestのDB依存テストをPostgreSQLへ移行した
- `Base.metadata.drop_all()`・`create_all()`をやめ、`TRUNCATE TABLE books, publishers RESTART IDENTITY`で行とシーケンスだけを初期化する
- テーブル構造、制約、インデックス、`alembic_version`は各テストの前後にも維持する
- PostgreSQLで53ケースすべての成功を確認した

## 同時ISBN登録とDB制約エラーの変換

- 状態：基礎学習完了・経過観察
- API側の重複検索は通常の重複をcommit前に発見し、分かりやすい409を返すための早期確認
- ほぼ同時の2リクエストは、両方が事前検索を通過する可能性がある
- PostgreSQLのUNIQUE制約は、同時登録を含めて重複保存を防ぐ最後の防御
- PostgreSQLのUNIQUE制約違反をpsycopgが`UniqueViolation`として受け取り、SQLAlchemyが`IntegrityError`で包む
- `error.orig`から元のpsycopg例外を確認し、`error.orig.diag.constraint_name`から違反した制約名を確認できる
- `UniqueViolation`かつ制約名が`uq_books_isbn`の場合だけ409へ変換し、その他の`IntegrityError`は500のままにした
- `Query.first()`を`None`を返す関数へ一時的に置き換え、事前検索を通過してcommit時に競合する状況を再現した
- 今回のテストは本当の並列実行ではなく、同時実行によって生じる結果を決まった順番で再現するテスト
- 今後の確認：本当の並列実行とトランザクション分離レベルをPostgreSQLで確認する

## インデックス、外部キー、JOIN

- 状態：基礎学習完了・経過観察
- インデックスは検索を速くする候補になる一方、INSERT・UPDATE・DELETE時の更新処理と保存容量が必要
- `ix_books_author`をAlembicで追加し、PostgreSQLの`\\d books`とSQLAlchemyのInspectorによるテストで確認した
- `ForeignKey`はDB側で存在しない関連先IDの保存を防ぎ、`relationship()`はPython側で関連オブジェクトを操作できるようにする
- `back_populates`は`book.publisher`と`publisher.books`の双方向の関係を同期する
- `JOIN`は検索中だけ関連行を組み合わせ、元のテーブルを永久に合体させない
- 今後の確認：別の要件から外部キーとJOINを自力設計できるか確認する

## 出版社レスポンスとN+1問題

- 状態：基礎学習完了・経過観察
- `BookDB.publisher_name` propertyは`publisher`があれば名前、なければ`None`を返す
- `BookResponse.publisher_name: str | None`により、Pydanticが`from_attributes=True`でpropertyを読み取る
- DBモデルが属性を保持していても、レスポンス用Pydanticモデルにない項目はAPIレスポンスへ含まれない
- 遅延読み込みで書籍一覧1回と出版社N回のSELECTが発生する状態をN+1問題という
- `joinedload(BookDB.publisher)`をQueryへ設定し、`.all()`で書籍と出版社を1回のSQLで取得する
- SQLAlchemyの`before_cursor_execute`イベントへコールバックを登録し、実行予定のSELECT文を記録した
- 関数定義は関数オブジェクトを作り、`event.listen()`はその関数オブジェクトをSQLAlchemyへ登録する
- `event.remove()`を`finally`で実行し、テストが追加した監視を後続テストへ残さない
- 出版社付き書籍2冊のレスポンスとSELECT 1回をテストし、全53ケースの成功を確認した
- 今後の確認：別のリレーションでもN+1を発見し、適切な読み込み方法を選べるか確認する

## トランザクション分離レベルと同時更新

- 状態：基礎学習完了・経過観察
- 分離レベルは、同時に動くトランザクションから見えるデータを制御する設定の枠である
- PostgreSQLのREAD COMMITTEDとREPEATABLE READを比較し、REPEATABLE READでは同じトランザクション中に同じスナップショットを維持することを確認した
- `session.connection(execution_options={"isolation_level": "REPEATABLE READ"})`でSessionが使うConnectionへ分離レベルを設定した
- 2つのThread、Barrier、Queueを使い、同じISBNの同時登録で1件だけcommitされ、もう1件がUNIQUE競合になることを確認した
- `books.version`と条件付き`Query.update()`を使い、同じversionを基にした同時更新の片方を409にする楽観的ロックを実装した
- `Query.update()`は更新内容の辞書を受け取り、更新件数を整数で返す。0件ならversionが一致しない競合として扱う
- `synchronize_session=False`ではSession内の既存オブジェクトを自動同期せず、commit後の`refresh()`でDBの最新値を読み直す

## パスワードハッシュとJWT認証

- 状態：基礎学習完了・経過観察
- `pwdlib`とArgon2で平文パスワードからハッシュを作り、ログイン時は平文へ戻さず検証する
- `UserDB.hashed_password`はAPIレスポンスへ含めず、`UserResponse`で公開項目を制限する
- JWTはheader、payload、signatureからなり、payloadはBase64URL表現されるが暗号化されていないため秘密情報を入れない
- JWTの`sub`へユーザーID、`exp`へ有効期限を入れ、HS256と環境変数の秘密鍵で署名する
- `HTTPBearer`がAuthorizationヘッダーを読み、`HTTPAuthorizationCredentials.credentials`からJWT文字列を取得する
- `Depends(get_current_user)`により、FastAPIはエンドポイント関数より先にJWT検証とUserDB検索を実行する
- トークンなし、不正・期限切れJWT、ユーザー不在を401としてテストした
- `client.get()`などの戻り値はResponseオブジェクトで、`.json()`はJSONボディをPython値へ変換し、`.headers`はHeadersオブジェクトを返す

## 所有者ベース認可

- 状態：基礎学習完了・経過観察
- 認証は「誰か」、認可は「その利用者が操作してよいか」を確認する
- `books.owner_id`を`users.user_id`への外部キー・NOT NULLとして追加し、既存行を守るためnullable追加、データ移行、NOT NULL化の2段階で進めた
- `owner_id=current_user.user_id`と代入できるのは`BookDB.owner_id`カラムがあるためで、ForeignKeyは保存時に参照先ユーザーの存在をDBで保証する
- クライアントへ`owner_id`を指定させず、JWTから取得したユーザーIDをサーバーが設定することで所有者の偽装を防ぐ
- PATCH・DELETEでは対象書籍の存在を404で確認した後、`target_book.owner_id`と`current_user.user_id`を比較し、不一致を403にする
- 401は認証できない状態、403は認証済みだが操作権限がない状態として使い分ける
- 他人によるPATCH・DELETEが403となり、書籍が変更・削除されないことをGETで確認した

## 認証済みfixtureと狭いモック

- 状態：基礎学習完了・要経過観察
- `authenticated_client` fixtureはDB初期化、秘密鍵設定、ユーザー登録、ログイン、JWTヘッダー設定を行い、`yield`後に共有clientのAuthorizationを削除する
- `pytestmark = pytest.mark.usefixtures("authenticated_client")`はfixtureの準備処理を各テスト前に実行し、引数で受け取る場合は`yield client`の値を直接利用できる
- fixtureがcommitしたユーザー行は、テスト内の別Sessionから検索できる。Python変数を直接共有しているわけではない
- `Query.first()`全体のモックは認証用UserDB検索まで`None`にして401を起こしたため、ISBN検索を`find_book_by_isbn()`へ分離し、その関数だけをモックした
- モック関数は置き換え対象と同じ呼び出し方を受け取る必要があり、キーワード引数`isbn=`・`db=`に対して引数名`_isbn`・`_db`ではTypeErrorになる
- テスト対象ではないNOT NULL・外部キーには正常値を与え、確認したい制約や振る舞いだけを意図的に変える

## CORSと主要なWeb API脅威

- 状態：基礎学習完了・経過観察
- CORSはブラウザが別オリジンのJavaScriptへレスポンスを公開してよいか判断する仕組みで、認証・認可の代わりではない
- `CORSMiddleware`へ`localhost:3000`、許可メソッド、`Authorization`・`Content-Type`を設定した
- ブラウザは`OPTIONS`でプリフライトを送り、CORSミドルウェアは許可済みオリジンへ`Access-Control-Allow-Origin`を付ける
- 許可済みプリフライト、未許可プリフライト、実際のGETレスポンスの3テストを追加した
- `book_id`は対象特定、`owner_id == current_user.user_id`はBOLAを防ぐ権限確認を担当する
- `owner_id`を入力スキーマへ含めずJWTから設定し、クライアントによる所有者プロパティの偽装を防ぐ
- `limit <= 100`は1回の取得件数を制限するが、短時間の大量リクエストを防ぐレート制限は未実装である
- SQLAlchemyの通常のクエリはSQLと値を分離するが、生SQLをf文字列で組み立てるとSQLインジェクションの危険が残る
- `UserResponse`で`hashed_password`を除外し、詳細ログと安全なHTTPエラーを分けて情報漏えいを防ぐ

## 個人用書籍APIの読み取り認可

- 状態：基礎学習完了・経過観察
- 公開カタログではなく個人用サービスと要件を決め、一覧・1件取得も`Depends(get_current_user)`で認証必須にした
- 一覧は`BookDB.owner_id == current_user.user_id`をクエリへ追加し、他人の書籍をPythonへ取得する前にPostgreSQL側で除外する
- 1件取得は`book_id`と`owner_id`を同じ`.filter()`へ渡し、両方に一致しなければ`.first()`が`None`となる
- 他人の1件取得は書籍の存在を知らせないため404、本人の一覧が0件なら正常な検索結果として200と空リストを返す
- 未ログインではHTTPBearerが401を返し、エンドポイント関数や書籍検索まで進まない
- 非所有者の更新・削除後にDB状態を確認するテストでは、GET前に保存済みの所有者Authorizationへ戻す
- 認証追加により一覧取得のSELECTは利用者検索1回と書籍・出版社の一括取得1回になり、N+1テストの期待値を合計2回へ更新した
- CORSの実レスポンステストでは、認証必須の`/books`へ`authenticated_client`でAuthorizationとOriginを両方送る
