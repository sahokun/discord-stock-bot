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
src/
├── .github/workflows/          # GitHub Actions設定
│   ├── discord-command-handler.yml
│   ├── issue-processor.yml
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
├── DISCORD_SETUP.md          # 利用ガイド
├── DISCORD_COMMANDS.md       # コマンドリファレンス
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

## 💰 コスト

- **GitHub Actions**: 月2,000分無料
- **GitHub Issues**: 無制限無料  
- **Discord Webhook**: 完全無料
- **株価API**: Yahoo Finance（無料）

**完全無料で運用可能！**

## 📚 ドキュメント

- [利用ガイド](DISCORD_SETUP.md) - 詳細な設定・使用方法
- [コマンドリファレンス](DISCORD_COMMANDS.md) - 全コマンドの詳細
- [開発者向け情報](CLAUDE.md) - プロジェクト構成とコード規約

## 🔒 セキュリティ

- GitHubの高セキュリティ環境で動作
- APIキーはGitHub Secretsで管理
- 全ての操作がGitHubに記録

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

## 🤝 貢献

1. リポジトリをフォーク
2. 機能ブランチを作成
3. 変更をコミット
4. プルリクエストを送信

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**完全サーバー不要で株価管理！GitHub Actionsの力を活用した現代的なソリューションです。**