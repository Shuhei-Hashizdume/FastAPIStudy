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
- 今後の確認：Sessionとトランザクションの流れ、例外時のrollbackを自分の言葉で説明できるか確認する

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

- 状態：学習中
- 更新済み：PATCHで `BookResponse` を使い、更新後の `target_book` を直接返す
- 更新確認済み：正常系200、存在しないIDの404
- 削除済み：DELETEを204・本文なしへ変更
- 削除確認済み：正常系204、存在しないIDの404
- 未確認：処理全体の自力実装、トランザクションとrollbackの説明、類似課題

## HTTPレスポンスと処理主体

- 状態：基礎理解・要復習
- エンドポイントはHTTPメソッドとパスで表される窓口
- エンドポイント関数は実際の処理を行い、Pythonの値を返す
- FastAPIはエンドポイント関数を呼び出し、HTTPレスポンスを生成する
- Pydanticはモデル定義に基づく検証・変換を担当する
- SQLAlchemyはPythonオブジェクトとDB操作を橋渡しする
- UvicornはHTTP通信を受け取り、HTTPレスポンスをクライアントへ送信する
