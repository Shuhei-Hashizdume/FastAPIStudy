# 苦手・要復習の管理

項目はセッション終了時の理解確認に応じて移動する。推測では「克服済み」にしない。

## 現在の苦手・要復習

- `commit()`、`refresh()`、`rollback()` の役割と処理順を自分の言葉で説明する
- 正常系だけでなく異常系まで確認する習慣
- コードが動くことと、APIの入出力設計が適切であることを分けて考える

## 学習中

- `response_model`

`response_model` は基本目的の説明を受けた段階。実装、理解確認、Swagger UI確認、応用課題は未完了。

## 今後学習

- レスポンス用Pydanticスキーマ（次回学習予定）
- DBモデルとAPIレスポンスを分離する考え方（次回以降）
- `from_attributes`
- 更新APIと削除APIの設計・動作確認
- APIレスポンスの統一
- ファイル分割と `APIRouter`
- pytestによるテスト
- PostgreSQLとAlembic
- 認証・認可
- Docker、CI、デプロイ

## 経過観察

- IDと `.first()` を使った1件取得
- `HTTPException` を使った404処理
- Dependency Injectionを使ったSession受け渡し

一度コードで使用しているが、今後の類似課題で自力実装と説明ができるか確認する。

## 克服済み

現時点では、苦手から移動したことを示す理解確認記録なし。
