# FastAPIStudy

Pythonバックエンドエンジニアとしての就職と、ジュニアエンジニアとして実務へ参加できる状態を目指す学習リポジトリです。現在はPython、FastAPI、SQLAlchemy、SQLiteを使った書籍管理APIで学習しています。

## 現在地

- 現在のフェーズ：CRUD APIの設計整理と理解確認
- 前回の終了地点：`response_model`、`from_attributes`、CRUDレスポンス改善の実装と動作確認
- 次回：更新・削除APIの処理、トランザクション、例外処理の理解確認

最新の学習状況は [learning/PROGRESS.md](learning/PROGRESS.md) を参照してください。

## 学習記録

- [ロードマップ](learning/ROADMAP.md)
- [現在の進捗](learning/PROGRESS.md)
- [セッション履歴](learning/SESSION_LOG.md)
- [苦手・要復習](learning/WEAKNESSES.md)
- [理解済み知識](learning/KNOWLEDGE.md)
- [就職・実務到達度](learning/JOB_READINESS.md)
- [ポートフォリオ計画](learning/PORTFOLIO.md)

## 現在のアプリ

`main.py` に書籍の登録、取得、更新、削除のコードがあります。ただし、コードが存在することと学習完了は分けて扱います。更新・削除などは、実装理由の説明、正常系・異常系の確認、応用課題を通過するまで完了扱いにしません。

## 初期移行の方針と結果

- 既存の書籍管理APIと、従来の指導・レビュー方針は残す
- コードが存在する項目と、学習完了条件を通過した項目を区別する
- IDによる1件取得、`.first()`、404処理までを完了済みとして引き継ぐ
- 初期移行時点では、`response_model` を基本説明まで進んだ「学習中」とした
- 初期移行時点では、レスポンス用スキーマ、`from_attributes`、更新・削除の理解確認などを推測で完了にしなかった
- 正確な日付が不明な履歴は `SESSION_LOG.md` に「移行時初期記録」として残す
- `ROADMAP.md` と `PROGRESS.md` の現在地を「PydanticスキーマとAPIレスポンス設計」に統一する

この初期移行では学習管理システムの構築だけを行い、`response_model` の講義や完成コードの追加は行っていません。

## 運用ルール

講義とレビューの進め方は [AGENTS.md](AGENTS.md) に定義しています。学習記録を更新する際は、各項目の完了条件を確認し、不明な履歴を推測で完了にしません。
