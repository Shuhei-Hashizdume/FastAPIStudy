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
