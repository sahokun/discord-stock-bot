"""
株価API テスト
"""

import unittest
from datetime import datetime
from unittest.mock import Mock, patch

from api.stock_api import StockPrice, StockPriceAPI
from utils.config import Config, StockConfig


class TestStockPriceAPI(unittest.TestCase):
    """株価API テストクラス"""

    def setUp(self):
        """テストセットアップ"""
        self.config = Config()
        self.api = StockPriceAPI(self.config)

    @patch("api.stock_api.yf.Ticker")
    def test_get_stock_price_success(self, mock_ticker):
        """株価取得成功テスト"""
        # モックデータの準備
        mock_ticker_instance = Mock()
        mock_ticker.return_value = mock_ticker_instance

        # 履歴データのモック
        import pandas as pd

        mock_hist = pd.DataFrame(
            {"Close": [100.0, 105.0], "Volume": [1000000, 1100000]}
        )
        mock_ticker_instance.history.return_value = mock_hist
        mock_ticker_instance.info = {"symbol": "TEST"}

        # テスト実行
        result = self.api.get_stock_price("TEST", "Test Stock", "us")

        # 検証
        self.assertIsNotNone(result)
        self.assertEqual(result.symbol, "TEST")
        self.assertEqual(result.name, "Test Stock")
        self.assertEqual(result.price, 105.0)
        self.assertEqual(result.change, 5.0)
        self.assertEqual(result.change_percent, 5.0)

    @patch("api.stock_api.yf.Ticker")
    def test_get_stock_price_failure(self, mock_ticker):
        """株価取得失敗テスト"""
        # モックデータの準備
        mock_ticker_instance = Mock()
        mock_ticker.return_value = mock_ticker_instance

        # 空の履歴データ
        import pandas as pd

        mock_hist = pd.DataFrame()
        mock_ticker_instance.history.return_value = mock_hist

        # テスト実行
        result = self.api.get_stock_price("INVALID", "Invalid Stock", "us")

        # 検証
        self.assertIsNone(result)

    def test_cache_functionality(self):
        """キャッシュ機能テスト"""
        # キャッシュにデータを設定
        test_price = StockPrice(
            symbol="TEST",
            name="Test Stock",
            price=100.0,
            change=5.0,
            change_percent=5.0,
            volume=1000000,
            timestamp=datetime.now(),
            market="us",
        )

        cache_key = "TEST_us"
        self.api.cache[cache_key] = {"data": test_price, "timestamp": datetime.now()}

        # キャッシュが有効であることを確認
        self.assertTrue(self.api._is_cache_valid(cache_key))


if __name__ == "__main__":
    unittest.main()
