# CLAUDE.md

## プロジェクト概要

これは株価情報を通知するDiscordボットプロジェクトです。GitHub ActionsとDiscord Webhookを連携させて、株価監視・通知システムを実装しています。

## 実装済み機能

### 1. Discord Bot (`bot/discord_bot.py`)
- Discord.pyベースのボット実装
- 株価情報の定期通知機能

### 2. 株価API (`api/stock_api.py`)
- yfinanceを使用した株価取得
- 複数の株式銘柄に対応

### 3. コマンド処理 (`utils/discord_commands.py`)
- Discordメッセージからコマンドを解析
- GitHub Issue作成用のフォーマット機能
- サポートコマンド: add-stock, remove-stock, list-stocks, clear-stocks

### 4. GitHub Actions統合
- Discord Webhookからのコマンド受信
- 自動的なGitHub Issue作成
- 株価通知の定期実行

## アーキテクチャ

```text
./
├── bot/
│   └── discord_bot.py      # Discord Bot実装
├── api/
│   └── stock_api.py        # 株価API
├── data/
│   └── stocks.json         # 監視銘柄データ
├── utils/
│   ├── config.py           # 設定管理
│   ├── discord_commands.py # コマンド解析
│   └── stock_manager.py    # 株式管理
├── tests/                  # テストファイル
├── main.py                 # エントリーポイント
└── requirements.txt        # 依存関係
```

## 開発環境

### 開発コマンド

```bash
# uvのインストール（初回のみ）
curl -LsSf https://astral.sh/uv/install.sh | sh

# Python 3.12 のインストール＋venv作成＋依存関係インストール
uv python install 3.12
uv venv
uv pip install -r requirements.txt

# コードフォーマット
uv run black .
uv run isort --profile black .

# リント
uv run flake8 . --ignore=E501,F401,F541,F811,E203,W503,W504 --max-line-length=88

# テスト実行
uv run pytest tests -s
uv run python run_tests.py

# メインアプリケーション実行
uv run python main.py
```

### GitHub CLI (gh)

```bash
# PR一覧
gh pr list

# PR詳細確認
gh pr view <番号>

# PRをクローズ
gh pr close <番号>

# PR作成
gh pr create --title "タイトル" --body "説明"
```

### Docker開発環境

Dockerコンテナ開発環境は廃止しました。uvを使ってWSLローカル環境で直接開発してください。

## 環境変数

必要な環境変数:
- `DISCORD_WEBHOOK_URL` - Discord Webhook URL（GitHub Actionsで設定）

## GitHub Actions

### `discord-command-handler.yml`
- Discord Webhookからのコマンド処理
- GitHub Issue自動作成
- 無効コマンドの通知

## Git ワークフロー

- featureブランチは `feature/<name>` の形式で **mainから** 作成する
- mainへの直接push・force pushは禁止
- Claudeの作業範囲はfeatureブランチへのpushまで

### PRフロー（人間が担当）
- PR作成・マージは人間が行う
- Copilotの自動レビューでコメントが付いた場合、Claudeが修正して同じfeatureブランチにpushする
- スレッドのResolveと最終マージは人間が行う
