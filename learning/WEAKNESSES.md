# 苦手・要復習の管理

項目はセッション終了時の理解確認に応じて移動する。推測では「克服済み」にしない。

## 現在の苦手・要復習

- HTTPレスポンスオブジェクト、レスポンスボディ、Pydanticモデルの違いを主語付きで説明する
- スレッド、SQLiteの `check_same_thread=False`、`StaticPool` がテストで必要な理由を説明する
- OS、実行中のプロセス、環境変数の関係を説明する
- fixture、Dependency Override、テスト用DBの役割を切り分けて説明する

## 学習中

- ログの目的、ログレベル、例外情報の記録
- ログへ機密情報を書かないための判断
- 制約違反などのDB例外を再現し、ログとテストで確認する
- CRUD全体を別の要件から一貫して自力実装する

## 今後学習

- fixtureの応用、モック、テストデータ管理
- 制約、インデックス、クエリ効率
- PostgreSQLとAlembic
- 認証・認可
- Docker、CI、デプロイ

## 経過観察

- FastAPI、Pydantic、SQLAlchemy、Uvicorn、エンドポイント関数の担当
- `response_model` とレスポンス用Pydanticスキーマ
- `from_attributes`
- Dependency Injectionを使ったSessionの受け渡し
- pytestのfixtureとDependency Overrideの実装
- 正常系だけでなく異常系まで確認する習慣

今後の類似課題で、ヒントなしに設計・実装・説明できるか確認する。

## 克服済み

- 更新APIの対象検索、部分更新、`commit()`、`refresh()`、レスポンスの基本的な流れ
- 削除APIの対象検索、`delete()`、`commit()`、204・404の基本的な流れ
- `commit()` 失敗後に `rollback()` でSessionを正常な状態へ戻す理由
- DBモデルとAPI用Pydanticスキーマの役割の違い
- ファイルの責務分割と `APIRouter` の基本
- pytestでステータスコードとJSONレスポンスを検証する基本
- Ruffによるフォーマットと不要importの整理
