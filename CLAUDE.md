# CLAUDE.md

このファイルは、このリポジトリのコードを操作する際にClaude Code (claude.ai/code)にガイダンスを提供します。

## プロジェクト概要

これは株価情報を通知するDiscordボットプロジェクトです。GitHub ActionsとDiscord Webhookを連携させて、株価監視・通知システムを実装しています。

## 実装済み機能

### 1. Discord Bot (`bot/discord_bot.py`)
- Discord.pyベースのボット実装
- 株価情報の定期通知機能
- GitHub Actions向けの単発実行モード

### 2. 株価API (`api/stock_api.py`)
- yfinanceを使用した株価取得
- 複数の株式銘柄に対応
- エラーハンドリングとフォールバック機能

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
src/
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

### 必要な依存関係
```
discord.py==2.3.2
requests==2.31.0  
python-dotenv==1.0.0
yfinance==0.2.65
schedule==1.2.0
pytz==2024.2
pytest==8.4.1
black==25.1.0
flake8==7.3.0
isort==6.0.1
```

### 開発コマンド

```bash
# コードフォーマット
black .
isort --profile black .

# リント
flake8 . --ignore=E501,F401,F811,E203,W503,W504 --max-line-length=88

# テスト実行
pytest tests -s
python run_tests.py

# メインアプリケーション実行
python main.py
```

### Docker開発環境

```bash
# 開発コンテナを起動
docker-compose -f .devcontainer/development/docker-compose.yml up --build
```

- **ベースイメージ**: Python 3.12
- **非特権ユーザー**: UID/GID 1000
- **仮想環境**: `/src/venv/`（自動作成）

## 環境変数

必要な環境変数:
- `DISCORD_WEBHOOK_URL` - Discord Webhook URL（GitHub Actionsで設定）
- `COMPOSE_PROJECT_NAME=discord-stock-bot`

## GitHub Actions

### `discord-command-handler.yml`
- Discord Webhookからのコマンド処理
- GitHub Issue自動作成
- 無効コマンドの通知
