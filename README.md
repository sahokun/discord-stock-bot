# Discord 株価通知Bot

**完全サーバー不要**で株価の監視と通知を行うシステムです。

## 🚀 特徴

✅ **完全サーバー不要** - GitHub Actionsのみで動作  
✅ **無料運用** - 全て無料サービスで構築  
✅ **簡単操作** - WebブラウザだけでOK  
✅ **株式管理** - 動的な監視銘柄の追加・削除  
✅ **多市場対応** - 日本株、米国株、暗号通貨、欧州株など  
✅ **Discord通知** - 株価更新と管理操作の通知  

## 📋 主な機能

### 1. 株式管理

- **株式追加**: `!add-stock AAPL Apple us`
- **株式削除**: `!remove-stock AAPL`
- **銘柄一覧**: `!list-stocks`
- **全削除**: `!clear-stocks`

### 2. 株価通知

- **定期通知**: 指定時間に株価を自動通知
- **価格アラート**: 急激な価格変動を検知
- **市場別表示**: 日本株、米国株、暗号通貨を分類

### 3. 利用方法

- **GitHub Actions手動実行**: WebブラウザからGitHub上で実行
- **GitHub Issues作成**: Issue経由でコマンド実行
- **Discord Webhook**: 結果をDiscordに自動通知

## 🌍 対応市場

- **jp**: 日本株（デフォルト）
- **us**: 米国株
- **crypto**: 暗号通貨
- **eu**: 欧州株
- **asia**: アジア株
- **ca**: カナダ株
- **au**: オーストラリア株

## 📁 ファイル構成

```
./
├── .github/workflows/          # GitHub Actions設定
│   ├── ci.yml
│   ├── discord-command-handler.yml
│   ├── issue-processor.yml
│   ├── webhook-trigger.yml
│   └── stock-bot.yml
├── api/                       # 外部API連携
│   └── stock_api.py
├── bot/                       # Discord Bot機能
│   └── discord_bot.py
├── data/                      # データファイル
│   └── stocks.json
├── utils/                     # ユーティリティ
│   ├── config.py
│   ├── discord_commands.py
│   └── stock_manager.py
└── requirements.txt          # 依存関係
```

## 🔧 セットアップ

### 1. Discord Webhook設定

1. Discord サーバーでWebhookを作成
2. GitHub SecretsにWebhook URLを設定

### 2. GitHub Actions設定

1. リポジトリをフォーク
2. GitHub Actionsを有効化
3. 必要に応じてcron設定を調整

### 3. 使用開始

1. GitHub Actionsページで手動実行
2. または GitHub Issuesで直接管理

## 🏗️ アーキテクチャ：GitHub Issueをメッセージキューとして使う設計

このプロジェクトはGitHub Issueを**コマンドの中継地点（メッセージキュー）**として活用しています。

### コマンド処理の流れ

```
Discord (ユーザーがコマンド入力)
    ↓ !add-stock AAPL Apple us
discord-command-handler.yml (workflow_dispatch でトリガー)
    ↓ コマンドを解析してGitHub Issueを自動作成
    例) タイトル: "Add Stock: AAPL (Apple)"
         ラベル: "discord-command"
issue-processor.yml (issues: opened, edited でトリガー)
    ↓ discord-command ラベル付きIssueを検知
    ↓ IssueのタイトルとBODYからコマンドを再解析
stocks.json を更新 → Discord に結果を通知
```

### 関連ファイル

- [`.github/workflows/discord-command-handler.yml`](.github/workflows/discord-command-handler.yml) - Discordコマンドを受け取りIssueを作成
- [`.github/workflows/issue-processor.yml`](.github/workflows/issue-processor.yml) - Issueを検知して実際の処理を実行
- [`utils/discord_commands.py`](utils/discord_commands.py) - コマンド解析とIssueフォーマット生成

---

## 📈 使用例

```bash
# 株式追加
!add-stock AAPL Apple us

# 日本株追加（市場指定なし）
!add-stock 369A.T エータイ

# 暗号通貨追加  
!add-stock BTC-USD Bitcoin crypto

# 銘柄一覧表示
!list-stocks
```
