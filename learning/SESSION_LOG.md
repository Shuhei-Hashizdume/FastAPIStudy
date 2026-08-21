# 学習セッション記録

正確な学習日が分からない過去の内容には日付を付けず、「移行時初期記録」とする。今後の記録日は `YYYY-MM-DD` 形式を使う。

## 移行時初期記録

### プロジェクト

書籍管理API

### 完了済みとして引き継ぐ内容

- FastAPIの基本的なGET、POST
- パスパラメータ、クエリパラメータ、リクエストボディ
- Pydanticによる入力
- SQLAlchemyとSQLiteによる登録と取得
- `.query()`、`.filter()`、`.all()`、`.first()`
- IDを使った1件取得
- 存在しない書籍への404処理

### 前回行った内容

- `response_model` の基本的な目的について説明を受けた

### 未完了

- `response_model` の実装
- `response_model` の役割を自分の言葉で説明する理解確認
- レスポンス用Pydanticスキーマ
- Swagger UIでの確認
- DBモデルとAPIレスポンスの分離
- 応用課題

### コード上には存在するが学習完了未確認

- 更新API
- 削除API

### 次回開始地点

`response_model` の理解確認と、書籍管理APIへの実装。

## 2026-07-15：GitHub接続と初回push

### 実施内容

- `git status` でGit管理状態を確認した
- `git init` でローカルリポジトリを初期化した
- `.gitignore` を作成し、`__pycache__/`、`venv/`、`book.db` を除外した
- `git add .` と初回コミットを実行した
- GitHubに `Shuhei-Hashizdume/FastAPIStudy` リポジトリを作成した
- `origin` を登録し、誤って登録した `otigin` を削除した
- `main` を `origin/main` へ初回pushし、対応付けを確認した

### 理解確認できた内容

- `git init` はGit管理を開始する操作
- `git add` は次のコミットに含める変更を選ぶ操作
- `commit` は選んだ変更をローカル履歴へ保存する操作
- `push` はローカルのコミットをGitHubへ送る操作
- `__pycache__/` はPythonが再生成できるキャッシュであり、通常はGit管理しない

### 継続確認

- 今後の学習変更で、差分確認、適切なコミットメッセージ、pushまでを繰り返す
- 小さな単位でのコミットとPull Requestでの説明は今後の課題とする

### FastAPI学習の次回開始地点

`response_model` の理解確認と、書籍管理APIへの実装。今回のGit学習による変更はない。

## 2026-07-16：`response_model` とCRUDレスポンス改善

### 実施内容

- `BookResponse` を作成し、`book_id`、`title`、`author` を定義した
- GET1件へ `response_model=BookResponse` を設定した
- GET全件へ `response_model=list[BookResponse]` を設定した
- `ConfigDict(from_attributes=True)` を設定した
- POSTの入れ子レスポンスをやめ、登録した書籍を直接返す設計へ変更した
- PATCHのレスポンスを `BookResponse` に統一した
- DELETEを `204 No Content` に変更した
- 講義で処理主体を明確にするルールを `AGENTS.md` へ追加した

### 理解確認できた内容

- `response_model` は、FastAPIがエンドポイント関数の戻り値を検証・整形するときに使うレスポンス用Pydanticモデルを指定する
- `BookRequest` はクライアントから受け取るリクエストボディを検証する
- `BookDB` はSQLAlchemyでテーブルと1レコード分のデータを扱う
- `BookResponse` はクライアントへ公開する項目と型を定義する
- `from_attributes=True` は、PydanticがSQLAlchemyオブジェクトの属性から値を読み取るための設定
- 1件は `BookResponse`、複数件は `list[BookResponse]` で表す
- API間でレスポンス構造を統一すると、クライアント側の処理が単純になる
- `204` は成功したが返す本文がないことを表す
- 422のJSON構文エラーと必須フィールド不足をエラー内容から区別した

### 動作確認

- POST正常系：201と `BookResponse`
- GET全件正常系：200と `list[BookResponse]`
- GET1件正常系：200、存在しないID：404
- PATCH正常系：200、存在しないID：404
- DELETE正常系：204、削除済みまたは存在しないID：404
- POSTの `author` 欠落：422

### 完了判定

- 完了：`response_model`
- 完了：レスポンス用Pydanticスキーマ
- 完了：DBモデルとPydanticスキーマの分離
- 完了：`from_attributes`
- 完了：APIレスポンスの統一
- 学習継続：更新・削除API全体の自力実装とトランザクションの説明

### 次回開始地点

更新・削除APIの処理を最初から説明し、`commit()`、`refresh()`、`rollback()` と例外処理を理解確認する。

## 2026-07-20：更新・削除からAPIテスト、環境設定まで

### 実施内容

- PATCHとDELETEを実装し、正常系・異常系を確認した
- `commit()`、`refresh()`、`rollback()` とSessionの状態を復習した
- Ruffの保存時フォーマットを導入し、不要importを削除した
- DB接続、DBモデル、Pydanticスキーマ、書籍Router、FastAPIアプリ本体へファイルを分割した
- `APIRouter` と `app.include_router()` を実装した
- pytest、`TestClient`、テスト用インメモリDB、Dependency Override、autouse fixtureを導入した
- POST、GET、PATCH、DELETE、著者絞り込みの正常系・異常系を含む9件のテストを成功させた
- `venv`、`bin`、`python -m`、`requirements.txt` の役割を学び、依存バージョンを記録した
- READMEに環境構築、起動、テスト、API仕様、ファイルの役割を追加した
- `DATABASE_URL` を環境変数から読み、未設定時はSQLiteを使うようにした
- 未経験者向けに、新しい概念の目的と用語を説明してから小さな1ステップずつ進める講義ルールを `AGENTS.md` へ追加した

### 理解確認できた内容

- `db.delete()` は削除予定にし、`db.commit()` がDBへ削除を確定する
- 204は処理が成功し、返すレスポンスボディがないことを表す
- 404は指定されたリソースが存在しないことを表す
- commit失敗後のSessionは失敗状態のため、`rollback()` で正常な状態へ戻す必要がある
- 各ファイルの責務と、`app.include_router()` がRouterのルートをFastAPIアプリへ登録すること
- `response.status_code` はHTTPレスポンスオブジェクトの属性であり、`from_attributes=True` とは無関係であること
- `response.json()` はJSONのレスポンスボディをPythonの辞書やリストへ変換すること
- fixtureはテストの準備と片付けを担当し、`yield` がその境界になること
- Dependency Overrideに登録すると、FastAPIがテスト中に `get_db` の代わりに `override_get_db` を使うこと
- DELETEは204の確認だけでなく、再度GETして404を確認すると実際の削除を検証できること
- 仮想環境と `requirements.txt` により、他の人が同じ依存関係を再現しやすくなること
- 環境変数は、実行中のプロセスにOSから渡される設定値であること

### 完了判定

- 完了：更新APIと削除APIの基本実装・説明・正常系・異常系確認
- 完了：Sessionとトランザクションの基本的な流れ
- 完了：ファイル分割と `APIRouter`
- 完了：pytestと `TestClient` による基本的な正常系・異常系テスト
- 完了：テスト用DBと開発用DBの分離
- 完了：環境変数によるDB接続設定の分離
- 完了：READMEの環境構築、起動方法、API仕様
- 経過観察：fixture、Dependency Override、環境変数の詳細な仕組み
- 未完了：ログの実装とログを使った例外調査
- 未完了：DB制約違反などを想定した例外テスト
- 未完了：別の要件からCRUD全体を一貫して自力実装する確認

### 次回開始地点

ログが必要な理由を復習し、`print()` と `logging` の違い、ログレベル、機密情報を順番に学ぶ。その後、例外処理へ1箇所ずつログを追加する。

## 2026-07-24：ログ、DB例外処理、ページネーション、NOT NULL制約、Alembic

### 実施内容

- `logging.getLogger(__name__)`と`logger.exception()`をPOST・PATCH・DELETEのDB例外処理へ追加した
- `HTTPException`はそのままFastAPIへ伝え、`SQLAlchemyError`ではログ、`rollback()`、安全な500レスポンスを行う構成にした
- `IntegrityError`と一般的な`SQLAlchemyError`を分け、制約違反用とDB操作失敗用のログを実装した
- `monkeypatch`で`Session.commit()`を一時的に置き換え、POST・PATCH・DELETEのDBエラーを再現した
- `caplog`でログメッセージ、例外クラス、元の例外メッセージを検証した
- 一覧取得へ`offset`、`limit`、`order_by(BookDB.book_id)`を追加した
- ページネーションの正常系と、offset・limit不正時の422をテストした
- `BookDB.title`と`BookDB.author`へ`nullable=False`を追加した
- TestClientを通さずテスト用Sessionを直接使い、SQLiteのNOT NULL制約が`IntegrityError`を発生させることを確認した
- `with`、コンテキストマネージャー、`pytest.raises`、`pytest.mark.parametrize`を学び、title・authorの2ケースを検証した
- Alembic 1.18.5を導入し、`requirements.txt`へ追加した
- `alembic init`で設定ファイルを作り、`DATABASE_URL`、`Base.metadata`、`render_as_batch=True`を設定した
- Alembic導入前のbooksテーブルを表すベースラインを手動作成した
- 既存`book.db`へベースラインを`stamp`し、NOT NULL制約追加マイグレーションを自動生成・レビュー・適用した
- 既存の書籍データ1件が移行後も維持され、title・authorのNOT NULL設定が有効になったことを確認した
- `/tmp`の空DBで`base → head → base → head`を実行し、upgrade・downgrade・空DB再現を確認した
- FastAPI起動時の`Base.metadata.create_all()`を削除し、DB構造管理をAlembicへ統一した
- READMEへマイグレーション手順とAlembic関連ファイルの役割を追加した

### 理解確認できた内容

- `logger.exception()`は開発者向けに例外種別、メッセージ、スタックトレースを残す
- クライアントには内部情報を隠し、`HTTPException`で安全なエラーレスポンスを返す
- `IntegrityError`はDBが報告した制約違反をSQLAlchemyがPython側へ伝える例外
- モックは本物の処理をテスト中だけ置き換える仕組みであり、今回は意図的なDBエラー再現に使用した
- `db.query(BookDB)`は検索条件を組み立てる`Query`オブジェクトを返し、`.all()`でSQLを実行する
- ページネーションは、必要な範囲だけDBから取得してレスポンス量と処理負荷を抑える
- PydanticはAPIの入口・出口、NOT NULL制約はDB保存時の最後の防御を担当する
- `with`はコンテキストマネージャー側に定義された開始・終了処理を呼び、例外時にも片付けを行う
- `pytest.raises`は期待した例外、`pytest.mark.parametrize`は複数の入力ケースを検証する
- AlembicはレコードではなくDB構造と変更履歴を管理する
- ベースラインは、空のDBから最初の構造を再現するための基準となる履歴
- `stamp`はマイグレーション処理を実行せず、既存DBの現在地だけを記録する
- マイグレーションファイルは変更手順、DB内の`alembic_version`は各DBの適用済み現在地を表す
- `render_as_batch=True`はSQLiteでテーブル作り直し方式の変更コードを生成するために必要
- `create_all()`は履歴を管理しないため、共有・本番DBの構造管理はAlembicへ任せる

### 動作確認

- pytest：18ケースすべて成功
- Python構文確認：成功
- 開発DB：`58b89d046d4a (head)`
- 開発DB：title・authorのNOT NULL有効、既存書籍データ維持
- 一時DB：空の状態から`upgrade head`成功
- 一時DB：`downgrade -1`、`downgrade base`、再度`upgrade head`成功

### 完了判定

- 完了：ログの追加とスタックトレースによるDB例外調査の基礎
- 完了：`IntegrityError`・`SQLAlchemyError`を想定した例外処理
- 完了：fixture、モック、`caplog`、パラメータ化の基礎
- 完了：ページネーションとクエリ効率の基礎
- 完了：NOT NULL制約の実装と実DBによる制約違反テスト
- 完了：Alembicのベースライン、`stamp`、upgrade、downgrade、空DB再現
- 経過観察：Alembicの各ファイルとDB内の現在地を、次回以降も自力で説明できるか
- 未完了：空文字列・文字数を含む入力バリデーション設計
- 未完了：別要件からCRUD全体を一貫して自力実装する確認

### 次回開始地点

`title: str`が`None`と空文字列をどう扱うかを確認し、Pydanticの入力バリデーションとDB制約の役割を復習する。その後、タイトル・著者の文字数制約と422レスポンスを小さく実装・テストする。

## 2026-07-27：入力バリデーション、ISBN、一意制約

### 実施内容

- `Field`でtitleを1〜200文字、authorを1〜100文字に制限した
- `ConfigDict(str_strip_whitespace=True)`で前後の空白を除去した
- 必須項目不足、`null`、空文字列、空白だけの文字列、長すぎる文字列、境界値をテストした
- PATCHで項目未指定・`null`・不正な空文字列を区別し、更新後のDB状態をGETでも確認した
- booksテーブルと各PydanticスキーマへISBNを追加した
- ISBNを必須の13桁数字として検証し、12桁・14桁・英字混入を422にした
- POSTとPATCHでISBN重複を事前確認し、409レスポンスを返す処理を追加した
- DBへISBNのUNIQUE制約とNOT NULL制約を追加した
- SQLAlchemyのSessionから直接登録し、APIを通らない書き込みでもUNIQUE・NOT NULL制約が働くことを確認した
- 既存データを維持するため、ISBNをnullableで追加して既存行を更新した後、別のマイグレーションでNOT NULL化した
- 2つのマイグレーションでupgrade・downgradeを行い、開発DBも最新revisionへ更新した

### 理解確認できた内容

- `title: str`だけでは空文字列を拒否できず、`Field(min_length=1)`などの制約が必要
- PydanticはFastAPIから入る値を検証し、DB制約はFastAPIを通らない書き込みも含めて保存データを守る
- 422は入力形式・型・必須条件の違反、409は正しい形式の入力と現在のDB状態の競合を表す
- `book_id`はDB内部で各行を識別する主キー、ISBNは本を表す業務上の識別番号
- API側の事前確認は分かりやすい409を返すため、DBのUNIQUE制約は最後の防御として必要
- `nullable=True`はNULLを許可し、`nullable=False`はNOT NULL制約を有効にする
- 既存行があるテーブルへ必須カラムを追加するときは、複数段階のマイグレーションが必要になる場合がある

### 動作確認

- pytest：46ケースすべて成功
- Alembic：ISBN追加とNOT NULL化のupgrade・downgrade成功
- 開発DB：`de1c8b4db0bb (head)`
- `alembic check`：未反映のDB構造変更なし
- `git diff --check`：問題なし

### 完了判定

- 完了：title・authorの空文字列、空白、文字数、`null`、必須項目の入力バリデーション
- 完了：PATCHで項目未指定・`null`・不正入力を区別する基本
- 完了：ISBNの形式検証、レスポンス、更新処理
- 完了：ISBNのUNIQUE・NOT NULL制約と409レスポンス
- 完了：既存データを守る段階的なAlembicマイグレーション
- 経過観察：主キーとUNIQUE制約の役割を、別の題材でも説明できるか
- 経過観察：APIの事前確認とDB制約を併用する理由を、自力で設計へ反映できるか
- 未完了：ISBNのチェックディジットを含む厳密な妥当性検証
- 未完了：同時リクエストによるISBN競合を409へ変換する設計
- 未完了：インデックス

### 次回開始地点

DBインデックスが必要になる理由から開始する。まず、インデックスがないDBがISBNや著者を探す流れを考え、検索速度の利点と書き込み・容量の欠点を確認する。その後、対象カラムを選び、Alembicで追加・削除して動作確認する。

## 2026-08-01：PostgreSQL、外部キー・JOIN、出版社レスポンス、N+1対策

### 実施内容

- `author`へインデックスを追加し、AlembicマイグレーションとDB構造テストで確認した
- `psycopg`を導入し、`DATABASE_URL`でHomebrew PostgreSQLの`fastapi_study`へ接続した
- PostgreSQLへベースラインから最新revisionまで適用し、`f481e0cbd250 (head)`を確認した
- FastAPIのPOST・GETと再起動後のGETにより、PostgreSQLへの読み書きと永続化を確認した
- `psql`で`books`、`publishers`、シーケンス、主キー、UNIQUE、インデックス、外部キーを直接確認した
- `publishers`テーブルと`books.publisher_id`を追加し、`relationship()`と`back_populates`で双方向の関連を実装した
- 出版社を登録して書籍へ関連付け、SQLの`JOIN`で書籍名と出版社名を取得した
- `BookDB.publisher_name` propertyと`BookResponse.publisher_name`で出版社名をAPIレスポンスへ追加した
- `joinedload(BookDB.publisher)`で一覧取得時に出版社を同時取得した
- SQLAlchemyの`before_cursor_execute`イベントでSELECTを記録し、出版社付き2冊を1回のSELECTで取得するテストを追加した
- 学習時の説明順序、情報量、理解確認頻度を`AGENTS.md`へ反映した

### 理解確認できた内容

- `DATABASE_URL`はターミナルのプロセス環境へ設定され、ターミナルを閉じると再設定が必要になる
- `alembic current`の`head`は行データではなくDB構造の変更履歴が最新であることを表す
- FastAPIを再起動してもデータが残るのは、PostgreSQLがデータを永続化しているため
- `psql`はPostgreSQLサーバーではなく、サーバーへ直接指示を送るクライアント
- シーケンスは次に発行する主キー番号を管理する
- インデックスは検索を速くする一方、書き込み時の更新処理と保存容量が必要になる
- `ForeignKey`はDB側の参照整合性、`relationship()`はPython側のオブジェクト操作を担当する
- `JOIN`は検索時に別テーブルの関連行を組み合わせ、テーブルを永久に合体させない
- `BookDB.publisher`は`PublisherDB`オブジェクトまたは`None`を保持する
- `@property`で`book.publisher.name`を`book.publisher_name`としてPydanticへ公開できる
- `response_model`にない属性は、SQLAlchemyオブジェクトが保持していてもレスポンスへ含まれない
- `Query`オブジェクトは条件と読み込み方法を保持し、`.all()`でSQLを実行する
- `joinedload()`は関連オブジェクトを事前取得し、レスポンス変換時の追加SELECTを防ぐ
- 関数定義は関数オブジェクトを作り、SQLAlchemyは登録されたコールバックをSQL実行直前に呼ぶ
- `before_cursor_execute`がコールバックへ渡す値は検索結果ではなく、実行直前の接続、SQL文、パラメータなど
- `event.remove()`と`finally`で一時的な監視を必ず解除し、後続テストへの影響を防ぐ

### 動作確認

- PostgreSQL：`f481e0cbd250 (head)`
- FastAPI：PostgreSQLへのPOSTは201、1件・全件GETは200
- PostgreSQL：FastAPI再起動後も登録した書籍を取得
- `psql`：書籍・出版社・外部キー・JOIN結果を確認
- pytest：52ケースすべて成功
- N+1対策テスト：出版社付き2冊をSELECT 1回で取得

### 完了判定

- 完了：DBインデックスの目的、利点、書き込み・容量面の欠点、実装、DB・テスト確認
- 完了：PostgreSQLの導入、接続、マイグレーション、CRUD、永続化の基礎
- 完了：外部キー、`relationship()`、`back_populates`、JOINの基礎
- 完了：出版社名をAPIレスポンスへ変換する設計とテスト
- 完了：N+1問題の説明、`joinedload()`による対策、SELECT回数テスト
- 経過観察：関数オブジェクト、コールバック、イベントリスナーを別の例でも説明できるか
- 経過観察：`commit()`内の`flush()`と`refresh()`の役割を混同せず説明できるか
- 未完了：SQLiteとPostgreSQLの違いを体系的に説明する
- 未完了：PostgreSQLを使う統合テスト
- 未完了：トランザクション分離レベルと同時更新

### 次回開始地点

現在のAPIはPostgreSQL、pytestはインメモリSQLiteを使っていることを確認する。ファイル型DBとサーバー型DBの違いから始め、データ型、制約、SQL、同時実行、マイグレーションの差を1項目ずつ扱う。その後、SQLiteのテストだけでは保証できない範囲とPostgreSQL統合テストの役割を考える。

## 2026-08-02：テスト専用PostgreSQLと同時ISBN競合

### 実施内容

- 開発用`fastapi_study`とテスト用`fastapi_study_test`を分離した
- `TEST_DATABASE_URL`から接続先DB名を検査し、テスト用DB以外への接続を拒否する安全確認を追加した
- Alembicでテスト用PostgreSQLへ全マイグレーションを適用した
- pytestのDB接続をインメモリSQLiteからテスト専用PostgreSQLへ変更した
- `drop_all()`・`create_all()`をやめ、`TRUNCATE`と`RESTART IDENTITY`で各テスト前後の行と連番だけを初期化した
- 入力バリデーションを復習し、空文字列、空白、`None`、未指定、Pydantic、NOT NULLの違いを確認した
- commit時に発生したISBNの`UniqueViolation`を、制約名`uq_books_isbn`まで確認して409へ変換した
- `Query.first()`を一時的に置き換え、API側の事前検索を通過してPostgreSQLのUNIQUE制約で失敗する状況を再現した

### 理解確認できた内容

- AlembicはDB構造と変更履歴、pytest fixtureは各テスト前後の行データ初期化を担当する
- `TRUNCATE`で外部キーの参照先だけを削除すると拒否される理由と、今回は`books`と`publishers`を両方明示していることを説明できた
- `title: str`だけでは空文字列を拒否できず、`Field(min_length=1)`が必要だと説明できた
- API側の事前検索は通常の重複を早期発見し、PostgreSQLのUNIQUE制約は同時登録を含めてデータを最後に守る
- `db.commit()`は呼ばれるが、制約違反によって完了せず`IntegrityError`になる
- ほぼ同時のリクエストは、両方が事前検索を通過する可能性がある
- 今回のテストは本当の同時実行ではなく、競合の結果を決まった順番で再現している

### 動作確認

- テスト専用PostgreSQLの接続先安全確認：開発用DBを指定するとcollection時に停止
- PostgreSQLへの対象テスト：成功
- ISBN以外の`IntegrityError`が500のままである対象テスト：成功
- pytest：53ケースすべて成功

### 完了判定

- 完了：開発用DBとテスト用DBの分離
- 完了：Alembicで構築したテストDB構造を残し、行だけを初期化するfixture
- 完了：DB依存テストのテスト専用PostgreSQLへの移行
- 完了：API側の事前検索を通過したISBN競合を、commit時の制約情報から409へ変換する処理とテスト
- 経過観察：`IntegrityError`、`error.orig`、`UniqueViolation`の関係を別の制約違反でも説明できるか
- 未完了：本当に複数処理を並列実行するテスト
- 未完了：トランザクション分離レベルと同時更新

### 次回開始地点

今回の`monkeypatch`テストが本当の同時実行ではない理由を復習する。その後、トランザクション分離レベルが同時処理から見えるデータへどう影響するかを、小さなPostgreSQLテストで確認する。

## 2026-08-13：JWT認証と書籍所有者ベース認可

### 実施内容

- Argon2によるパスワードのハッシュ化・検証、ユーザー登録、メール重複時の409変換を実装した
- JWTの作成・検証、ログイン、Bearer認証、`GET /users/me`を実装した
- トークンなし、不正JWT、期限切れJWT、JWTのユーザーがDBに存在しない場合を401としてテストした
- `books.owner_id`を`users.user_id`への外部キーとして追加した
- 既存書籍を安全に移行するため、nullableで追加して既存行を更新後、別マイグレーションでNOT NULL化した
- 開発用・テスト用PostgreSQLへ2つのマイグレーションを適用し、`8972e235fa78 (head)`と実際の制約を確認した
- `POST /books`を認証必須にし、JWTから取得した`current_user.user_id`を`owner_id`として保存した
- PATCH・DELETEで書籍所有者とログイン中ユーザーを比較し、所有者以外を403で拒否した
- `authenticated_client` fixtureで登録・ログイン・JWTヘッダー設定・後片付けを共通化した
- 既存のDB直接操作テストへ有効な`owner_id`を追加し、元の検証対象以外の制約違反を防いだ
- `Query.first()`全体のモックが認証用UserDB検索まで壊したため、ISBN検索を`find_book_by_isbn()`へ分離してモック対象を狭めた
- 本当の2スレッド同時ISBN登録、REPEATABLE READ、version条件付きUPDATEによる楽観的ロックを実装・確認した

### 理解確認できた内容

- 認証は利用者が誰かを確認し、認可はその利用者が操作してよいかを確認する
- `HTTPBearer`は`Depends(bearer_scheme)`によりエンドポイント関数より先にAuthorizationヘッダーを処理する
- `client.get()`・`post()`の戻り値はResponseオブジェクトであり、PydanticレスポンスモデルやJSONボディとは別である
- `response.headers`は辞書のように扱えるHTTP専用のHeadersオブジェクトである
- `owner_id=current_user.user_id`と代入できる直接の理由は`BookDB.owner_id`カラムがあるためで、外部キーは参照先IDの存在をDBで保証する
- `owner_id`をクライアント入力に含めず、認証結果からサーバーが決めることで所有者の偽装を防ぐ
- `pytestmark`はfixtureを先に実行させ、fixtureがcommitしたユーザーは別Sessionから検索できる
- `yield client`はfixtureの値をテストへ渡し、`yield`後は共有clientのAuthorizationヘッダーを削除する
- モックは指定したクラス全体へ影響し得るため、確認したい小さな責務だけを置き換える
- キーワード引数で呼ばれるモック関数は、元の呼び出しと一致する引数名を受け取る必要がある
- REPEATABLE READのSession Bでは、最初のSELECTがスナップショットの基準になるため、準備用検索を別Sessionで行う
- `Queue[str]`はスレッド間で文字列の結果を安全に受け渡し、`sorted()`は業務上の意味ではなく文字列順で結果をそろえる

### 動作確認

- 開発用・テスト用DB：`8972e235fa78 (head)`
- `psql`：`books.owner_id`のinteger、NOT NULL、`fk_books_owner_id_users`を確認
- PATCH：所有者以外は403、書籍タイトルは変更されない
- DELETE：所有者以外は403、書籍は削除されない
- pytest：92ケース収集、学習者の環境で全件成功
- Git：コミット`675f52a`をGitHubへpush済み

### 完了判定

- 完了：パスワードハッシュの作成・検証と秘密情報を返さないユーザー登録
- 完了：JWT発行・検証、Bearer認証、現在ユーザー取得
- 完了：認証の主要な正常系・異常系テスト
- 完了：本当の同時ISBN登録、REPEATABLE READ、versionによる楽観的ロックの基礎
- 完了：書籍所有者の段階的マイグレーション、保存、PATCH・DELETEの所有者認可
- 完了：所有者認可の403と、操作されていないDB状態のテスト
- 経過観察：fixtureの実行順と共有状態を別のfixtureでも自力設計できるか
- 経過観察：モック対象と関数シグネチャを別の例でも自力判断できるか
- 未完了：CORS、秘密情報、主要なWeb API脅威の基礎
- 未完了：所有者ベース以外のロール・権限設計

### 次回開始地点

認証と認可、401と403、クライアントに`owner_id`を指定させない理由を短く復習する。その後、現在の読み取りAPIを誰に公開するかという認可方針を整理し、CORS・秘密情報・主要なWeb API脅威を1項目ずつ扱う。

## 2026-08-14：CORS・秘密情報・主要なWeb API脅威の基礎

### 実施内容

- `CORSMiddleware`を追加し、`http://localhost:3000`、GET・POST・PATCH・DELETE、Authorization・Content-Typeを明示的に許可した
- 許可済みオリジンのプリフライト、未許可オリジンのプリフライト、実際のGETレスポンスの3テストを追加した
- `.env`を`.gitignore`へ追加し、JWT秘密鍵、開発DB、テストDBの安全な見本を`.env.example`へ追加した
- JWT形式とアクセストークンの役割、JWT header、ログインレスポンスの`access_token`・`token_type`を復習した
- BOLA、プロパティ単位の認可不備、リソース消費の制限不足、設定不備、SQLインジェクション、レスポンス・エラーの情報漏えいを現在のコードと対応付けた

### 理解確認できた内容

- CORSミドルウェアがHTTPレスポンスへ許可ヘッダーを追加し、ブラウザがJavaScriptへ内容を渡すか判断する
- 許可されたオリジンからOriginヘッダー付きで要求された場合、実際のGETレスポンスにも`Access-Control-Allow-Origin`が付く
- JWTはアクセストークンそのものの総称ではなく、今回はアクセストークンを表す形式として使っている
- JWT秘密鍵が漏れると、攻撃者がFastAPIの検証を通る署名を作れる危険がある
- `.env.example`は必要な環境変数名を伝える説明書で、本物の秘密情報や環境変数を自動設定するものではない
- `book_id`は対象を特定するだけで、所有者認可には`owner_id`とログインユーザーの比較が必要である
- 所有者をクライアントに決めさせず、サーバーがJWTから設定することで偽装を防ぐ
- SQLAlchemyを使ってもSQLの理解は必要で、SQLと入力値の分離がSQLインジェクション対策になる

### 動作確認

- CORS対象テスト3件：成功
- pytest全件：成功
- `git diff --check`：問題なし
- `.env`：Gitの追跡対象外
- `.env.example`：本物の秘密情報を含まない見本値のみ

### 完了判定

- 完了：CORSの目的、ブラウザ・ミドルウェア・エンドポイント関数の役割分担
- 完了：明示的な許可オリジン設定とプリフライト・実レスポンスの正常系、未許可オリジンの異常系テスト
- 完了：秘密情報をコードとGitから分離し、`.env.example`で必要な設定名だけ共有する基礎
- 完了：主要なWeb API脅威と、現在の認証・認可・入力制限・レスポンス設計との対応付け
- 経過観察：別APIでCORS・公開項目・認可条件を要件から自力設計できるか
- 未完了：レート制限の実装、本番環境の秘密情報管理サービス、秘密情報のローテーション実践

### 次回開始地点

現在のGET・POST・PATCH・DELETEそれぞれの認証・認可条件を確認し、書籍一覧・1件取得を誰へ公開するか要件から決める。その後、決定した読み取り認可方針をテストで示す。

## 2026-08-15：個人用書籍APIの読み取り認可

### 実施内容

- 書籍管理APIを公開カタログではなく、ログイン利用者が自分の書籍だけを管理する個人用サービスと決定した
- `show_books()`へ`Depends(get_current_user)`と所有者条件を追加し、本人の書籍だけを一覧取得するよう変更した
- `show_book()`へ認証依存を追加し、`book_id`と`owner_id`の両方が一致する書籍だけを取得するよう変更した
- 所有者別一覧、非所有者の1件取得、一覧・1件取得のトークンなしをテストした
- 認証追加によって影響したN+1のSQL回数テスト、非所有者PATCH・DELETE後の確認GET、CORSの実レスポンステストを修正した

### 理解確認できた内容

- `book_id`は対象の特定、`owner_id == current_user.user_id`はその対象を読める権限の確認を担当する
- 他人の書籍を1件指定された場合は存在を知らせないため404を返す
- 一覧取得で本人の書籍が0件の場合は、正常な検索結果として200と空リストを返す
- 未ログインのGETはHTTPBearerで401となり、エンドポイント関数やDB検索まで進まない
- `UserDB.user_id`はモデルのカラムであり、ログインユーザーの実際の値には`current_user.user_id`を使う
- 認証を追加するとUserDB検索のSELECTが増えるため、書籍と出版社の一括取得が維持されても全体のSELECTは2回になる
- 非所有者へ切り替えたテストで所有者として確認GETするには、元のAuthorizationを保存・復元する必要がある

### 動作確認

- 所有者別一覧テスト：成功
- 非所有者の1件取得404テスト：成功
- 未ログインの一覧・1件取得401テスト：成功
- 書籍テスト全件：成功
- CORSの実レスポンステスト：成功
- pytest全件：成功

### 完了判定

- 完了：書籍読み取りAPIを公開型・個人用の要件から選択する
- 完了：一覧・1件取得の認証と所有者フィルタ
- 完了：未ログイン401、他人の1件404、本人の0件一覧200の使い分け
- 完了：認可変更が既存のSQL回数、更新・削除、CORSテストへ与える影響の修正
- 経過観察：別のデータ要件で公開範囲と401・403・404を自力設計できるか

### 次回開始地点

pytestが実行時の振る舞いを確認するのに対し、lint・format・型チェックがコードを実行する前に何を確認するか、全体像から学ぶ。各ツールを一度に入れず、役割を確認して1つずつ導入する。

## 2026-08-16：Ruff・mypy strictとSQLAlchemy 2系型付きモデル

### 実施内容

- Ruff 0.16.0を導入し、import順、未使用import、複数`with`文を段階的に修正した
- FastAPIの`Depends()`に対するB008、Alembicの副作用importに対するF401、過去のマイグレーション履歴を`ruff.toml`で適切に扱った
- Ruffの`--select`、`--statistics`、対象を限定した`--fix`、`format --check`を使い分けた
- mypy 2.3.0を導入し、通常検査、`--check-untyped-defs`、`--strict`の順で検査範囲を広げた
- `declarative_base()`を`DeclarativeBase`へ変更し、全SQLAlchemyモデルを`Mapped`・`mapped_column()`と型付きrelationshipへ移行した
- nullableな外部キー、単数・複数relationship、前方参照をPythonの型へ反映した
- `get_db()`のGenerator型、JWT payloadの辞書型、SQLAlchemy更新辞書、エンドポイント関数の戻り値型を追加した
- `mypy.ini`へstrict設定と検査対象を記録し、Ruff・mypy・pytestのキャッシュを`.gitignore`へ追加した

### 理解確認できた内容

- Ruffはコードの書き方、mypyは型の整合性、pytestは正常系・異常系を含む実際の動作を確認する
- Ruffが自動修正可能と示しても、FastAPIやAlembicの意図したコードを機械的に削除してはいけない
- `import models`はAlembicがモデルを`Base.metadata`へ登録するために必要である
- SQLAlchemy 2系をインストールしていても、モデル記法に旧形式が残る場合がある
- `Mapped[str]`はPython側の値、`mapped_column(String, nullable=False)`はDB側の型と制約を示す
- `publisher_id`がNULLなら`book.publisher`はNone、出版社に書籍が0件なら`publisher.books`は空リストになる
- `BookDB.version + 1`は整数値ではなく、PostgreSQLへ送るSQL式である
- `response_model`とエンドポイント関数が実際に返すPythonオブジェクトの型は別である

### 動作確認

- `python -m ruff check .`：成功
- `python -m ruff format --check .`：全対象ファイル整形済み
- `python -m mypy`：strict設定で成功
- `python -m pytest -q`：全件成功
- `alembic check`：`No new upgrade operations detected.`

### 完了判定

- 完了：lint・format・型チェックが解決する問題の区別
- 完了：Ruffの指摘を確認し、修正・限定除外・対象外設定を判断する基礎
- 完了：mypy strictとSQLAlchemy 2系の型付きモデルへの移行
- 完了：静的検査、型チェック、pytest、Alembic差分確認の品質確認フロー
- 経過観察：別の機能でも戻り値型、nullable、relationship、外部ライブラリ境界の型を自力設計できるか

### 次回開始地点

Issue・ブランチ・コミット・Pull Requestが開発工程のどこを担当するか全体像を確認する。その後、現在の未コミット変更を題材に、Issueへ目的・要件・完了条件を整理し、専用ブランチとPull Requestで変更内容・確認方法を説明する。

## 2026-08-17：IssueからPull Request・マージまでの実務フロー

### 実施内容

- READMEと実装の不一致を題材に、GitHub Issue #1へ問題・目的・完了条件を記載した
- Issueの完了条件を調査・変更・確認のタスクへ分解した
- `docs/issue-1-update-readme-quality-checks`ブランチを作成した
- READMEのテスト用DB説明を、インメモリSQLiteからテスト専用PostgreSQLへ修正した
- `TEST_DATABASE_URL`付きpytest、Ruffのlint・format確認、mypyの実行手順をREADMEへ追加した
- 古いSQLite記載の検索、pytest、Ruff、mypy、`git diff --check`、変更ファイルを確認した
- コミット`3c9fb4b`をpushし、PR #2へ変更理由・変更内容・確認結果・`Closes #1`を記載した
- `Files changed`がREADMEだけであることを確認し、PR #2を`main`へマージしてIssue #1が閉じることを確認した
- `git pull --ff-only`でローカル`main`を更新し、ローカル・リモートの作業ブランチを削除した

### 理解確認できた内容

- Issueは作業の問題・目的・完了条件を共有し、誤った方向へ進むことを防ぐ
- ブランチはプロジェクトのコピーではなく、コミットを指す目印である
- pushは作業ブランチをGitHubへ共有する操作で、Pull Requestは変更内容のレビューと`main`への取り込みを提案する仕組みである
- 実務では責任者や担当レビュアーが、要件・テスト・安全性を確認してからマージする
- マージコミット`49974be`は、PR #2を`main`へ統合した履歴である
- ローカルとGitHubのブランチは別に存在し、マージ後はそれぞれを整理する必要がある
- ブランチを削除しても、`main`へマージ済みの変更・コミット・PR・Issueの履歴は残る

### 動作確認

- README記載のテスト専用PostgreSQLを使ったpytest：成功
- Ruffによるlint：成功
- Ruffによるフォーマット確認：成功
- mypyによる型チェック：成功
- `git diff --check`：問題なし
- PR #2の変更ファイル：READMEのみ
- PR #2：Merged
- Issue #1：Closed
- 最終ブランチ一覧：ローカル・リモートともに`main`のみ

### 完了判定

- 完了：Issueへ問題・目的・完了条件を記載する
- 完了：Issueを調査・変更・確認のタスクへ分解する
- 完了：専用ブランチ、コミット、push、Pull Request、マージ、後片付けの基本フロー
- 完了：PRへ変更理由・変更内容・確認結果を記載する
- 経過観察：別Issueで同じ流れをヒントなしに再現する
- 未完了：実際の他者レビュー指摘を理解し、修正・再確認・追加コミット・返信で対応する

### 次回開始地点

Pull Requestのレビューが要件・安全性・保守性をチームで確認する工程であることを復習する。その後、小さなレビュー指摘を題材に、指摘内容の整理、修正、対象確認、追加コミット、レビュー返信を1ステップずつ行う。

## 2026-08-21：Dockerfile・Docker ComposeによるAPIとPostgreSQLの実行環境

### 実施内容

- `python:3.14-slim`を土台に、依存関係とアプリコードをコピーしてUvicornを起動するDockerfileを作成した
- `.dockerignore`で仮想環境、Git、`.env`、キャッシュ、ローカルSQLiteをビルド対象から除外した
- DockerイメージからAPIコンテナを起動し、`8000:8000`のポート転送でSwagger UIを表示した
- `compose.yaml`へAPI・PostgreSQL 17のサービス、環境変数、内部ネットワーク、`postgres_data` volumeを定義した
- `pg_isready`によるhealthcheckと`depends_on`で、PostgreSQLが`healthy`になった後にAPIを起動した
- 一時APIコンテナからAlembicを`head`まで適用し、Composeの`command`へAlembic成功後のUvicorn起動を組み込んだ
- `.env`のPostgreSQL設定からAPI用`DATABASE_URL`を作り、`JWT_SECRET_KEY`をAPIコンテナへ渡した
- API・DBコンテナとネットワークを削除・再作成し、同じvolumeの登録済みユーザーでログインできることを確認した
- ログイン500のログから`KeyError: 'JWT_SECRET_KEY'`を特定し、環境変数の受け渡しを修正した
- `.env.example`とREADMEへ、見本のコピー、ローカル値、秘密鍵生成、起動、状態確認、Swagger UI、停止手順を追加した

### 理解確認できた内容

- Dockerfileはイメージの作り方、イメージはひな型、コンテナは動作中の実体である
- `RUN`はビルド時、`CMD`はコンテナ起動時に実行される
- Composeの`command`はDockerfileの`CMD`を上書きするため、Uvicorn起動も`command`へ含める必要がある
- Composeはプロジェクト名とサービス名・volume名からDocker上の名前を自動生成する
- Composeの内部ネットワークはAPIとDBの内部通信に使い、作成しただけでインターネットへ公開されるわけではない
- PostgreSQLコンテナとvolumeは別の役割で、通常の`docker compose down`ではvolumeとDBデータが残る
- `Up`はプロセス動作中、`healthy`はhealthcheck成功を表し、HTTPとDB接続はSwagger UI・API操作で別に確認する
- Alembicが失敗した状態でUvicornを起動すると、APIコードが期待するテーブル・カラム・制約と実DBが一致せず500の原因になる
- `.env.example`は見本の共有、`.env`は各開発者の実値、`api.environment`はコンテナへ渡す値を担当する

### 動作確認

- Dockerイメージのビルド：成功
- API・PostgreSQLのCompose起動：成功
- PostgreSQL healthcheck：`healthy`
- Alembic `8972e235fa78 (head)`：確認
- Swagger UI：表示成功
- ユーザー登録：201
- コンテナ再作成後のログイン：200、`token_type: bearer`
- pytest：99件成功、7.34秒
- Ruff lint：`All checks passed!`
- Ruff format：25ファイル整形済み
- mypy：8ファイル、問題なし
- `docker compose config --quiet`：成功
- `git diff --check`：問題なし

### 完了判定

- 完了：DockerfileからAPIイメージを作り、コンテナでFastAPIを起動する
- 完了：Docker ComposeでAPI・PostgreSQL・volume・内部ネットワークを管理する
- 完了：PostgreSQLのhealthcheck後にAlembicとUvicornを順番に起動する
- 完了：ローカル用環境変数と秘密情報を`.env`へ分離し、安全な見本だけ共有する
- 完了：ログ、状態表示、HTTPレスポンス、DB操作から障害を段階的に切り分ける基礎
- 経過観察：別要件でDockerfile・Composeを自力設計し、`CMD`上書きやvolume削除の影響を判断する
- 未完了：CI、クラウドへのデプロイ、本番環境の秘密情報管理

### 次回開始地点

手元でpytest・Ruff・mypyを実行するだけでは、実行忘れや環境差を防げない問題を確認する。その後、CIの役割とGitHub上で品質チェックを自動実行する流れを、設定を小さく作りながら学ぶ。
