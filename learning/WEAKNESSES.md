# 苦手・要復習の管理

項目はセッション終了時の理解確認に応じて移動する。推測では「克服済み」にしない。

## 現在の苦手・要復習

- `commit()`、`refresh()`、`rollback()` の役割と処理順を自分の言葉で説明する
- FastAPI、Pydantic、SQLAlchemy、Uvicorn、エンドポイント関数の担当を、主語を明確にして説明する
- コード上の不要な空白やimportを整理する

## 学習中

- 更新API全体の処理とトランザクション
- 削除API全体の処理とトランザクション
- 正常系だけでなく異常系まで確認する習慣

更新・削除のレスポンス改善とSwagger UIでの動作確認は完了。類似課題での自力実装と、例外時のrollbackを含む処理説明を次回確認する。

## 今後学習

- ファイル分割と `APIRouter`
- pytestによるテスト
- PostgreSQLとAlembic
- 認証・認可
- Docker、CI、デプロイ

## 経過観察

- `response_model` とレスポンス用Pydanticスキーマ
- `from_attributes`
- 1件と複数件で異なるレスポンス型を選ぶ
- APIレスポンスの一貫性
- IDと `.first()` を使った1件取得
- `HTTPException` を使った404処理
- Dependency Injectionを使ったSession受け渡し

今後の類似課題で、ヒントなしに設計・実装・説明できるか確認する。

## 克服済み

- `response_model` の基本目的、実装、Swagger UIでの確認
- レスポンス用Pydanticスキーマの基本設計
- DBモデルとAPIレスポンスモデルの役割の違い
- SQLAlchemyオブジェクトの属性から値を読む `from_attributes=True` の基本
