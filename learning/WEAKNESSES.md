# 苦手・要復習の管理

項目はセッション終了時の理解確認に応じて移動する。推測では「克服済み」にしない。

## 現在の苦手・要復習

- HTTPレスポンスオブジェクト、レスポンスボディ、Pydanticモデルの違いを主語付きで説明する
- スレッド、SQLiteの`check_same_thread=False`、`StaticPool`がテストで必要な理由を説明する
- OS、実行中のプロセス、環境変数の関係を説明する
- `nullable=True`とNOT NULL無効、`nullable=False`とNOT NULL有効の対応を混同せず説明する
- Alembicのベースライン、`stamp`、マイグレーションファイル、DB内の`alembic_version`の関係を説明する
- HTTPレスポンスオブジェクトと、`status_code`・JSONボディを区別する
- PATCHのISBN重複確認で更新対象自身を除外する理由を説明する
- `commit()`内の`flush()`でIDが取得される流れと、`refresh()`でDBの最新値を読み直す役割を区別する
- 関数定義による関数オブジェクト生成、コールバック登録、SQLAlchemyによる呼び出しを主語付きで説明する
- SQLAlchemyイベントが渡す値は検索結果ではなく、SQL実行直前の接続・SQL文・パラメータなどであることを説明する
- fixtureの`yield`前後、`pytestmark.usefixtures()`、テスト関数の引数でfixtureの値を受け取る場合の違いを説明する
- 位置引数とキーワード引数の違い、およびモック関数が元の関数と同じ呼び出し方を受け取る必要性を説明する
- 認証失敗の401と、認証済みだが権限がない403の違いを処理順付きで説明する
- Dockerfileの`CMD`とComposeの`command`の上書き関係を、別の起動構成でも自力で判断する
- `.env.example`、Composeが読む`.env`、APIコンテナへ渡された環境変数を区別する

## 学習中

- EC2停止時のコンテナ、Docker Volume、EBS、パブリックIPv4の状態変化を処理順で説明する
- Docker Volumeによる同一EC2内の永続化と、EBSスナップショット等のバックアップを区別する
- HTTPとHTTPS、Security Groupによる通信元制限と通信内容の暗号化を区別する
- IAMのユーザー、グループ、直接付与ポリシー、最小権限の関係を説明する

- 主キーとUNIQUE制約の共通点・役割の違い
- CRUD全体を別の要件から一貫して自力実装する
- `IntegrityError`、`error.orig`、`UniqueViolation`の関係
- 所有者ベース認可を別のデータ要件へ応用する
- レート制限の実装と、本番環境でのSecrets Managerなどを使った秘密情報管理

## 今後学習

- デプロイ、本番環境の秘密情報管理

## 経過観察

- レビュー指摘の意図を修正前に整理し、別のPRでも同じブランチへの追加コミット・確認・返信を自力で行う
- 公式ドキュメント調査で、公式ドメインだけでなく使用中のバージョンと`dev`・`latest`・固定版を照合する
- 翻訳で概要をつかみ、クラス名・引数名・型・デフォルト値・戻り値を原文と照合する
- Issueの問題・目的・完了条件を、別の変更でも自力で具体化する
- Issueを調査・変更・確認の小さなタスクへヒントなしで分解する
- ブランチ、コミット、push、Pull Request、mergeの役割を別の作業でも区別して説明する
- PR本文へ変更理由・変更内容・確認結果を書き、マージ後のローカル・リモートブランチを自力で整理する
- Dockerfileからイメージを作り、ComposeでAPI・PostgreSQL・volume・ネットワークを別要件でも構成する
- `Up`、`healthy`、ログ、HTTPレスポンス、DB操作を使い、コンテナ障害を段階的に切り分ける
- Ruffの指摘を機械的に直さず、一般的なルールとFastAPI・Alembic固有の例外を区別する
- Ruff、mypy、pytestの担当を、書き方・型・実行結果として区別する
- `Mapped`・`mapped_column()`・型付き`relationship()`を別モデルでも自力で設計する
- `nullable=True`と`Mapped[T | None]`を対応させ、単数relationshipの`None`と複数relationshipの空リストを区別する
- `response_model`とエンドポイント関数が実際に返すPythonオブジェクトの型を区別する
- `Generator[Session, None, None]`で`yield`する値、外部から送る値、終了時のreturn値を説明する
- `Any`をアプリ全体へ広げず、外部ライブラリとの狭い境界だけで使う判断

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
- DBインデックスの検索面の利点と、書き込み・容量面のコスト
- PostgreSQLの接続、`psql`、シーケンス、永続化
- 外部キー、`relationship()`、`back_populates`、JOIN
- `@property`とPydanticの`from_attributes=True`による出版社名のレスポンス変換
- N+1問題と`joinedload()`、イベントリスナーによるSELECT回数の検証
- fixtureは行初期化、AlembicはDB構造の再現を担当する役割分担
- API側の事前検索とPostgreSQLのUNIQUE制約を併用する理由
- SQLiteとPostgreSQLの違いと、テスト専用PostgreSQLを使う範囲
- `TRUNCATE`と`RESTART IDENTITY`によるテストデータ初期化
- 本当の2スレッド同時実行、`Barrier`、`Queue`による結果収集
- READ COMMITTED・REPEATABLE READとスナップショット
- version条件付きUPDATEによる楽観的ロックと409
- Argon2によるパスワードハッシュ、JWTの発行・検証、Bearer認証
- `Depends(get_current_user)`による現在ユーザー取得
- `owner_id`と`current_user.user_id`の比較によるPATCH・DELETE認可
- Responseオブジェクト、JSONボディ、Headersオブジェクトの区別
- CORSのプリフライト、実際のレスポンス、`Access-Control-Allow-Origin`、ブラウザの判断主体
- `.env`、`.env.example`、実行中プロセスの環境変数の役割分担
- BOLA、プロパティ単位の認可不備、リソース消費、SQLインジェクションと現在の対策
- 一覧取得の所有者フィルタ、他人の1件取得を404にする情報隠蔽、未ログイン401の読み取り認可
- 認証追加によりSQL回数や既存テストの前提が変わる影響範囲の確認

今後の類似課題で、ヒントなしに設計・実装・説明できるか確認する。

## 克服済み

- 更新APIの対象検索、部分更新、`commit()`、`refresh()`、レスポンスの基本的な流れ
- 削除APIの対象検索、`delete()`、`commit()`、204・404の基本的な流れ
- `commit()`失敗後に`rollback()`でSessionを正常な状態へ戻す理由
- DBモデルとAPI用Pydanticスキーマの役割の違い
- ファイルの責務分割と`APIRouter`の基本
- pytestでステータスコードとJSONレスポンスを検証する基本
- Ruffによるlint・formatと、mypy strictによる型チェックの基本
- レビュー指摘を理解し、同じ作業ブランチで修正・確認・追加コミット・push・返信・マージする基本
- 公式ドキュメントから対象クラスと設定を探し、対応バージョンと現在のコードへの適用可否を確認する基本
- CIのtrigger、runner、service container、stepsを区別し、Ruff・mypy・Alembic・pytestをGitHub Actionsで自動実行する基本
- 意図的なmypyエラーでCI失敗とRulesetのマージ禁止を確認し、復元後に再成功させる基本
- DB例外をモックで再現し、開発者向けログと安全な500レスポンスを分ける基本
- NOT NULL制約をSQLiteで実際に発生させ、`pytest.raises`で検証する基本
