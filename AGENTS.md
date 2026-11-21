# Discord 株価通知ボット

<!-- このファイルは AI エージェント（Claude Code・Codex など）と人の両方に向けた、このリポジトリの作業規則。
     「プロジェクト固有」の節はプロジェクトごとに書き換え、「共通の規則」の節は sahokun の全リポジトリで共通に保つ。 -->

## プロジェクト固有

### 概要

株価を監視して Discord に通知するボット。サーバーを持たず、GitHub Actions と Discord Webhook だけで動く。監視する銘柄は、Discord のコマンドから GitHub の Issue を経由して追加・削除する。

### 技術スタックと構成

- Python 3.12。株価の取得に yfinance、通知に Discord Webhook を使う。
  - `bot/discord_bot.py`: ボットの本体（定期通知・価格アラート）。
  - `api/stock_api.py`: yfinance による株価の取得。複数の銘柄に対応する。
  - `utils/discord_commands.py`: Discord のメッセージからコマンド（add-stock・remove-stock・list-stocks・clear-stocks）を解析し、Issue 用に整形する。
  - `utils/stock_manager.py`・`utils/config.py`: 監視銘柄（`data/stocks.json`）の管理と設定。
  - `main.py`: エントリーポイント。
- ワークフロー（`.github/workflows/`）:
  - `discord-command-handler.yml`: Discord のコマンドを受けて Issue を作り、無効なコマンドを通知する。
  - `issue-processor.yml`: `discord-command` ラベルの Issue を処理し、`data/stocks.json` を更新してコミットする。
  - `stock-bot.yml`: 定期の株価通知（現在は無効にしてある）。
  - `webhook-trigger.yml`: 価格アラートを確かめ、`stock-update` の repository dispatch を送る。
- 必要な secret: `DISCORD_WEBHOOK_URL`（GitHub Actions に設定する）。

### 確認の手順

```bash
uv python install 3.12
uv venv
uv pip install -r requirements.txt
uv run black .
uv run isort --profile black .
uv run flake8 . --ignore=E501,F401,F541,F811,E203,W503,W504 --max-line-length=88
uv run pytest tests -s
```

## 共通の規則

### ブランチと PR

<!-- branch-model:begin -->
- 既定のブランチは `main`。作業はブランチを切り、`main` への PR にする。
- PR は squash merge で取り込む。main の履歴には PR のタイトルだけが 1 コミットとして残る。
<!-- branch-model:end -->
- PR のタイトルは Conventional Commits（`feat: ...`・`fix: ...` など）で、変更の内容が 1 行で分かるように書く。
- PR がマージされたら、作業ブランチは自動で削除される。

### 履歴と公開物に書かないもの

- メールアドレス・トークン・パスワード・個人の環境の情報・AI エージェントのセッションへのリンクを、コミット・PR・Issue・コメントに書かない。
  - 作業ブランチのコミットと PR は、マージ後も GitHub に残り続け、所有者でも消せない。main の履歴も書き換えには強制 push とサポートへの依頼が要る。PR の本文だけは後から編集で直せる。
- コミットの作成者のメールアドレスは、GitHub の noreply アドレス（`<ID>+<ユーザー名>@users.noreply.github.com`）を使う。
- `.env`・鍵ファイル・ローカル設定（`.claude/settings.local.json` など）はコミットしない。

### 依存関係

- 追加・更新する依存は、公開から 7 日以上たったバージョンに限る。公開直後に乗っ取り・差し替えが見つかる事例が多いため。
  - Dependabot のバージョン更新は `cooldown` で 7 日待つ。npm は `.npmrc` の `min-release-age=7` で手作業の更新にも同じ制限を掛ける。
- GitHub Actions のアクションは、フル SHA（40 桁）で固定し、行末にバージョンをコメントで残す（例: `actions/checkout@<SHA> # v7.0.1`）。タグは差し替えられるため。
- Dependabot の PR は、更新を知らせる合図として扱う。CI が通ることと、メジャー更新では変更点を確かめてから取り込む。
