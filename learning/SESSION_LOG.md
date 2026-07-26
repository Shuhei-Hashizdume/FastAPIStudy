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
