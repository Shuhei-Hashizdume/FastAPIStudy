# 現在の学習状況

## 現在地

- 現在のフェーズ：Docker・デプロイ・運用基礎
- 現在のプロジェクト：書籍管理API
- 今回の終了地点：PR #3でレビュー指摘の理解・修正・確認・追加コミット・返信・マージを行い、FastAPIとPydanticの公式ドキュメントをバージョン確認付きで調査した
- 現在の学習状態：テスト・品質・チーム開発の基礎項目を一通り経験し、Dockerによる実行環境の再現へ進める状態
- 次回講義：Dockerが解決する問題と、イメージ・コンテナ・Dockerfileの役割

## 今回完了した項目

- PR #3のレビュー指摘について、記載場所の責務が不適切という意図を自分の言葉で整理した
- 同じ作業ブランチで`PORTFOLIO.md`の記載を移動し、重複・移動先・`git diff --check`を確認した
- レビュー修正を追加コミットして同じPRへpushし、修正内容・確認結果・pytest未実施理由をコメントで返信した
- PR #3をマージし、ローカル`main`更新とローカル・リモート作業ブランチの整理を行った
- FastAPI公式リファレンスから`HTTPBearer.auto_error`の型、デフォルト値、`False`時の依存関係の結果を確認した
- Pydantic 2.13.4と公式ドキュメントの対象バージョンを照合し、`dev`・`latest`・固定バージョンの違いを確認した
- Pydantic公式Modelsから`from_attributes=True`がPythonオブジェクトの属性を読む設定であることを確認し、`BookDB`から`BookResponse`への変換へ適用した
- 公式ドメイン、対応バージョン、型・デフォルト値・戻り値、翻訳と原文、現在の要件への適用を順番に確認する調査手順を説明した

- READMEと実装の不一致を問題として整理し、GitHub Issue #1へ問題・目的・完了条件を記載した
- Issueの完了条件を調査・変更・確認のタスクへ分解した
- `docs/issue-1-update-readme-quality-checks`ブランチを作成し、READMEのテスト用DB説明をインメモリSQLiteからテスト専用PostgreSQLへ更新した
- `TEST_DATABASE_URL`付きpytest、Ruffのlint・format確認、mypyの実行手順をREADMEへ追加した
- README記載のpytest・Ruff・mypyを実行し、古いSQLite記載、意図しない変更、空白エラーがないことを確認した
- コミットとpushを行い、PR #2へ変更理由・変更内容・確認内容・`Closes #1`を記載した
- `Files changed`がREADMEだけであることをレビューし、PR #2を`main`へマージしてIssue #1が自動で閉じることを確認した
- ローカル`main`を`git pull --ff-only`で更新し、ローカル・リモートの作業ブランチを削除した
- pushは作業ブランチをGitHubへ共有する操作、Pull Requestは変更の確認と`main`への取り込みを提案する仕組みだと説明した

- Ruff 0.16.0を導入し、lintとformatが解決する問題をpytest・mypyと区別して説明した
- import順、未使用import、複数`with`文を修正し、FastAPIの`Depends()`に対するB008はフレームワーク固有の例外として設定した
- Alembicの`import models`が`Base.metadata`登録のために必要な副作用importであると判断し、`env.py`だけF401を無視した
- 過去のマイグレーション履歴`alembic/versions/`をRuffの検査対象外にし、`ruff.toml`へチーム共通設定を記録した
- mypy 2.3.0を導入し、基本検査・`--check-untyped-defs`・`--strict`の検査範囲を段階的に確認した
- `declarative_base()`を`DeclarativeBase`へ変更し、全モデルのカラムを`Mapped`・`mapped_column()`へ移行した
- nullableな`publisher_id`を`Mapped[int | None]`、単数relationshipを`PublisherDB | None`、複数relationshipを`list[BookDB]`として型付けした
- `get_db()`を`Generator[Session, None, None]`、JWT payloadを`dict[str, Any]`、各エンドポイント関数を実際のPython戻り値で型付けした
- SQLAlchemyのSQL式を含む`update_values`を外部ライブラリとの境界として`dict[Any, Any]`で明示した
- `mypy.ini`へPython 3.14・strict・アプリ本体の検査対象を記録し、キャッシュを`.gitignore`へ追加した
- `ruff check`、`ruff format --check`、mypy strict、pytest全件、`alembic check`をすべて成功させ、DB構造差分がないことを確認した

- `GET /books`を認証必須にし、`owner_id == current_user.user_id`で本人の書籍だけをDB検索した
- `GET /books/{book_id}`を認証必須にし、他人の書籍を存在しない書籍と同じ404として扱った
- 一覧では本人の書籍が0件なら正常結果として200と`[]`、1件取得では他人の書籍を隠すため404とする違いを説明した
- 未ログインの一覧・1件取得を401、他人の一覧を空リスト、他人の1件取得を404としてテストした
- 認証追加によるSELECT増加、所有者切り替え後の確認GET、CORSテストへの影響を修正し、pytest全件成功を確認した
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
- `book_id`による対象特定だけでは読み取り認可にならず、DBクエリへ所有者条件を含める必要があると説明できる
- 一覧の0件は正常な検索結果、他人の1件取得は存在を隠す404として使い分けられる
- 認証追加後のN+1テストでは、利用者検索1回と書籍・出版社の一括取得1回の合計2回になると説明できる
- Issueを問題・目的・完了条件へ整理し、調査・変更・確認の実行可能なタスクへ分解できる
- push、Pull Request、mergeの役割を、共有・レビュー依頼・`main`への統合として区別できる
- PR本文に変更理由・変更内容・確認結果を書き、`Closes #1`でIssueと関連付けられる
- マージ後にローカル`main`を更新し、ローカル・リモートの作業ブランチを安全に削除できる
- レビュー指摘を修正前に自分の言葉で整理し、同じブランチへの追加コミット・push・返信で既存PRを更新できる
- Pythonコードを変更していない文書修正では、pytestを実行しない理由と代わりに必要な差分確認を説明できる
- 公式ドメインだけでなく、使用中のライブラリとドキュメントの対象バージョンを照合できる
- `dev`・`latest`・固定バージョンのドキュメントを区別し、公式仕様と現在のコードへの判断を分けて記録できる

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

- Dockerが解決する環境差の問題を説明する
- イメージとコンテナの役割を区別する
- Dockerfileが何を定義するファイルか説明する
- 書籍管理API用の最小Dockerfileを段階的に作成する
- イメージをビルドし、コンテナでFastAPIを起動して確認する

## 次回開始時の講師への指示

次の3点を報告してから、目的と必要な理由を先に説明し、新しい用語を1つずつ扱う。

- 前回の終了地点：PR #3のレビュー対応と、FastAPI・Pydantic公式ドキュメントのバージョン確認付き調査を完了
- 今回の講義：Dockerが解決する問題と、イメージ・コンテナ・Dockerfileの役割
- 現在のプロジェクト：書籍管理API

最初に、現在はMacへPython・venv・PostgreSQLを個別導入している状態を示し、別PCで環境差が起きる問題を説明する。その後、イメージを実行環境のひな型、コンテナをイメージから作られた実行中の環境として区別し、Dockerfileへ進む。
