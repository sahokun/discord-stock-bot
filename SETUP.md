# Discord Stock Bot セットアップガイド

このガイドでは、Discord Stock Botをセットアップして実行する方法を説明します。

## 前提条件

- GitHub アカウント
- Discord サーバーの管理者権限

## 1. GitHubリポジトリのセットアップ

### 1.1 リポジトリの作成

1. GitHubで新しいリポジトリを作成します
2. このプロジェクトのファイルをリポジトリにプッシュします

```bash
git init
git add .
git commit -m "Initial commit: Discord Stock Bot"
git remote add origin https://github.com/your-username/discord-stock-bot.git
git push -u origin main
```

### 1.2 GitHub Secrets の設定

リポジトリの Settings > Secrets and variables > Actions で以下のSecretを設定します：

- `DISCORD_WEBHOOK_URL`: Discord WebhookのURL（下記で取得）

### 1.3 GitHub Variables の設定

リポジトリの Settings > Secrets and variables > Actions で以下のVariablesを設定します：

- `NOTIFICATION_INTERVAL`: 通知間隔（秒）、デフォルト: 300
- `PRICE_CHANGE_THRESHOLD`: 価格変動アラート閾値（%）、デフォルト: 5.0
- `TIMEZONE`: タイムゾーン、デフォルト: Asia/Tokyo

## 2. Discord Webhook の設定

### 2.1 Discord Webhookの作成

1. 通知を送信したいDiscordサーバーを開きます
2. 通知を送信したいチャンネルを右クリック → "チャンネルの編集"
3. "連携サービス" → "ウェブフック"
4. "新しいウェブフック" をクリック
5. ウェブフックの名前を設定（例: "Stock Bot"）
6. "ウェブフックURLをコピー" をクリック

### 2.2 WebhookURLの設定

コピーしたWebhookURLを GitHub Secrets の `DISCORD_WEBHOOK_URL` に設定します。

## 3. 動作確認

### 3.1 手動実行

1. GitHubリポジトリの "Actions" タブを開きます
2. "Discord Stock Bot" ワークフローを選択
3. "Run workflow" をクリックして手動実行

### 3.2 スケジュール実行

ワークフローは以下のスケジュールで自動実行されます：

- **平日 9:00 JST**: 市場開始前通知
- **平日 15:30 JST**: 日本市場終了後通知  
- **平日 23:00 JST**: 米国市場終了後通知

## 4. ローカル開発環境（オプション）

### 4.1 開発環境のセットアップ

```bash
# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 4.2 環境変数の設定

`.env` ファイルを作成し、以下の内容を設定します：

```bash
DISCORD_WEBHOOK_URL=your_webhook_url_here
NOTIFICATION_INTERVAL=300
PRICE_CHANGE_THRESHOLD=5.0
TIMEZONE=Asia/Tokyo
```

### 4.3 ローカル実行

```bash
# テストの実行
python run_tests.py

# ボットの実行
python main.py
```

## 5. 監視対象の銘柄設定

デフォルトで以下の銘柄が監視されます：

### 日本株・日本株インデックス
- 7203.T: トヨタ自動車
- 6758.T: ソニーグループ
- 9984.T: ソフトバンクグループ
- ^N225: 日経平均
- ^TOPX: TOPIX

### 米国株・米国株インデックス
- AAPL: Apple
- GOOGL: Alphabet
- MSFT: Microsoft
- TSLA: Tesla
- ^GSPC: S&P 500
- ^DJI: ダウ平均

### 暗号通貨
- BTC-USD: Bitcoin

銘柄を変更する場合は、`utils/config.py` の `_load_stock_config` メソッドを編集してください。

## 6. Webhook トリガー（外部連携）

**注意: 現在外部システムとの連携は未実装のため、webhook-trigger.ymlは未使用です。**

外部システムからのWebhookトリガーを設定する場合：

1. GitHub Personal Access Token を作成
2. GitHub Secrets に `GITHUB_TOKEN` を設定
3. 以下のエンドポイントにPOSTリクエストを送信：

```
POST https://api.github.com/repos/your-username/discord-stock-bot/dispatches
Authorization: token YOUR_GITHUB_TOKEN
Content-Type: application/json

{
  "event_type": "stock-update"
}
```

## 7. トラブルシューティング

### よくある問題

1. **Discord通知が来ない**
   - Webhook URLが正しく設定されているか確認
   - Discord チャンネルの権限設定を確認

2. **株価データが取得できない**
   - インターネット接続を確認
   - Yahoo Finance APIの利用制限に注意

3. **GitHub Actions が実行されない**
   - リポジトリの Actions が有効になっているか確認
   - Secrets と Variables が正しく設定されているか確認

### ログの確認

GitHub Actions の実行ログは Actions タブから確認できます。エラーが発生した場合は、ログを確認してください。

## 8. カスタマイズ

### 通知メッセージのカスタマイズ

`bot/discord_bot.py` の以下のメソッドを編集：
- `_create_regular_embed()`: 定期通知メッセージ
- `_send_price_alert()`: 価格アラートメッセージ

### 監視銘柄の追加

`utils/config.py` の `_load_stock_config()` メソッドに新しい銘柄を追加してください。

Yahoo Finance の銘柄コードを使用します：
- 日本株: 銘柄コード + ".T" (例: 7203.T)
- 米国株: 銘柄コード (例: AAPL)
- 暗号通貨: 銘柄コード + "-USD" (例: BTC-USD)

## サポート

問題が発生した場合は、GitHub Issues で報告してください。