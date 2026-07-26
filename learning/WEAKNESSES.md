# 苦手・要復習の管理

項目はセッション終了時の理解確認に応じて移動する。推測では「克服済み」にしない。

## 現在の苦手・要復習

- HTTPレスポンスオブジェクト、レスポンスボディ、Pydanticモデルの違いを主語付きで説明する
- スレッド、SQLiteの`check_same_thread=False`、`StaticPool`がテストで必要な理由を説明する
- OS、実行中のプロセス、環境変数の関係を説明する
- fixture、Dependency Override、テスト用DBの役割を切り分けて説明する
- `nullable=True`とNOT NULL無効、`nullable=False`とNOT NULL有効の対応を混同せず説明する
- Alembicのベースライン、`stamp`、マイグレーションファイル、DB内の`alembic_version`の関係を説明する
- HTTPレスポンスオブジェクトと、`status_code`・JSONボディを区別する
- PATCHのISBN重複確認で更新対象自身を除外する理由を説明する

## 学習中

- 主キーとUNIQUE制約の共通点・役割の違い
- API側の重複確認とDBのUNIQUE制約を併用する理由
- CRUD全体を別の要件から一貫して自力実装する

## 今後学習

- インデックス、外部キー、JOIN
- PostgreSQL
- 認証・認可
- Docker、CI、デプロイ

## 経過観察

- FastAPI、Pydantic、SQLAlchemy、Uvicorn、エンドポイント関数の担当
- `response_model`とレスポンス用Pydanticスキーマ
- `from_attributes`
- Dependency Injectionを使ったSessionの受け渡し
- pytestのfixture、Dependency Override、モック、`caplog`
- `logger.exception()`とスタックトレースによる原因調査
- `IntegrityError`と`SQLAlchemyError`の使い分け
- ページネーションの`offset`、`limit`、並び順
- Alembicの`revision`、`upgrade`、`downgrade`
- 正常系だけでなく異常系と全件テストまで確認する習慣
- `Field`による文字数制約と、空文字列・`null`・必須項目不足の422検証
- `ConfigDict(str_strip_whitespace=True)`による前後空白の除去
- PATCHで項目未指定・`null`・不正な空文字列を区別する設計
- ISBNの入力検証、409、DBのUNIQUE・NOT NULL制約
- nullableなカラム追加からNOT NULL化へ進める段階的マイグレーション

今後の類似課題で、ヒントなしに設計・実装・説明できるか確認する。

## 克服済み

- 更新APIの対象検索、部分更新、`commit()`、`refresh()`、レスポンスの基本的な流れ
- 削除APIの対象検索、`delete()`、`commit()`、204・404の基本的な流れ
- `commit()`失敗後に`rollback()`でSessionを正常な状態へ戻す理由
- DBモデルとAPI用Pydanticスキーマの役割の違い
- ファイルの責務分割と`APIRouter`の基本
- pytestでステータスコードとJSONレスポンスを検証する基本
- Ruffによるフォーマットと不要importの整理
- DB例外をモックで再現し、開発者向けログと安全な500レスポンスを分ける基本
- NOT NULL制約をSQLiteで実際に発生させ、`pytest.raises`で検証する基本
