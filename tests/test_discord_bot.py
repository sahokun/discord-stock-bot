"""
Discord Bot テスト
"""

import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

from api.stock_api import StockPrice
from bot.discord_bot import DiscordStockBot
from utils.config import Config


class TestDiscordStockBot(unittest.TestCase):
    """Discord Bot テストクラス"""

    def setUp(self):
        """テストセットアップ"""
        self.config = Config()
        self.config.notification.webhook_url = "https://discord.com/api/webhooks/test"

        self.stock_api = Mock()
        self.bot = DiscordStockBot(self.config, self.stock_api)

    def test_format_price_jp(self):
        """日本円価格フォーマットテスト"""
        result = self.bot._format_price(1000.0, "jp")
        self.assertEqual(result, "¥1,000")

    def test_format_price_us(self):
        """米ドル価格フォーマットテスト"""
        result = self.bot._format_price(100.50, "us")
        self.assertEqual(result, "$100.50")

    def test_format_price_crypto(self):
        """暗号通貨価格フォーマットテスト"""
        result = self.bot._format_price(50000.0, "crypto")
        self.assertEqual(result, "$50,000")

    def test_format_price_forex(self):
        """為替レート価格フォーマットテスト"""
        result = self.bot._format_price(148.85, "forex")
        self.assertEqual(result, "148.85")

    def test_should_send_alert_first_time(self):
        """初回アラート送信判定テスト"""
        alert = StockPrice(
            symbol="TEST",
            name="Test Stock",
            price=100.0,
            change=10.0,
            change_percent=10.0,
            volume=1000000,
            timestamp=datetime.now(),
            market="us",
        )

        result = self.bot._should_send_alert(alert)
        self.assertTrue(result)

    def test_should_send_alert_duplicate(self):
        """重複アラート送信判定テスト"""
        alert = StockPrice(
            symbol="TEST",
            name="Test Stock",
            price=100.0,
            change=10.0,
            change_percent=10.0,
            volume=1000000,
            timestamp=datetime.now(),
            market="us",
        )

        # 直前にアラートを送信したことをシミュレート
        self.bot.last_alert_time["TEST"] = datetime.now()

        result = self.bot._should_send_alert(alert)
        self.assertFalse(result)

    @patch("bot.discord_bot.requests.post")
    def test_send_discord_message(self, mock_post):
        """Discord メッセージ送信テスト"""
        # レスポンスのモック
        mock_post.return_value.status_code = 204

        embed = {
            "title": "Test Message",
            "description": "Test Description",
            "color": 0x0099FF,
        }

        self.bot._send_discord_message(embed)

        # 呼び出しが行われたことを確認
        mock_post.assert_called_once()

        # 呼び出し引数を確認
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], self.config.notification.webhook_url)
        self.assertEqual(kwargs["json"]["embeds"][0], embed)

    def test_format_stock_list(self):
        """株価リストフォーマットテスト"""
        stocks = [
            StockPrice(
                symbol="TEST1",
                name="Test Stock 1",
                price=100.0,
                change=5.0,
                change_percent=5.0,
                volume=1000000,
                timestamp=datetime.now(),
                market="us",
            ),
            StockPrice(
                symbol="TEST2",
                name="Test Stock 2",
                price=200.0,
                change=-10.0,
                change_percent=-5.0,
                volume=2000000,
                timestamp=datetime.now(),
                market="us",
            ),
            StockPrice(
                symbol="USDJPY=X",
                name="USD/JPY",
                price=148.85,
                change=1.56,
                change_percent=1.06,
                volume=0,
                timestamp=datetime.now(),
                market="forex",
            ),
        ]

        result = self.bot._format_stock_list(stocks)

        self.assertIn("📈 **Test Stock 1**: $100.00 (+5.00%)", result)
        self.assertIn("📉 **Test Stock 2**: $200.00 (-5.00%)", result)
        self.assertIn("📈 **USD/JPY**: 148.85 (+1.06%)", result)


if __name__ == "__main__":
    unittest.main()
