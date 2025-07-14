"""
設定管理モジュール
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class StockConfig:
    """株式設定"""

    symbol: str
    name: str
    market: str  # 'jp' or 'us'
    threshold: float = 5.0  # 変動通知閾値（%）


@dataclass
class NotificationConfig:
    """通知設定"""

    webhook_url: str
    interval: int = 300  # 定時通知間隔（秒）
    timezone: str = "Asia/Tokyo"


class Config:
    """設定クラス"""

    def __init__(self):
        self.notification = NotificationConfig(
            webhook_url=os.getenv("DISCORD_WEBHOOK_URL", ""),
            interval=int(os.getenv("NOTIFICATION_INTERVAL", "300")),
            timezone=os.getenv("TIMEZONE", "Asia/Tokyo"),
        )

        self.price_change_threshold = float(os.getenv("PRICE_CHANGE_THRESHOLD", "5.0"))

        # 監視対象株式の設定
        self.stocks = self._load_stock_config()

        # GitHub設定
        self.github_token = os.getenv("GITHUB_TOKEN", "")

    def _load_stock_config(self) -> List[StockConfig]:
        """株式設定を読み込み"""
        stocks = []

        # 日本株
        jp_stocks = [
            ("7203.T", "トヨタ自動車", "jp"),
            ("6758.T", "ソニーグループ", "jp"),
            ("9984.T", "ソフトバンクグループ", "jp"),
            ("^N225", "日経平均", "jp"),
            ("^TOPX", "TOPIX", "jp"),
        ]

        # 米国株
        us_stocks = [
            ("AAPL", "Apple", "us"),
            ("GOOGL", "Alphabet", "us"),
            ("MSFT", "Microsoft", "us"),
            ("TSLA", "Tesla", "us"),
            ("^GSPC", "S&P 500", "us"),
            ("^DJI", "ダウ平均", "us"),
        ]

        # 暗号通貨
        crypto_stocks = [
            ("BTC-USD", "Bitcoin", "crypto"),
        ]

        # 設定を統合
        for symbol, name, market in jp_stocks + us_stocks + crypto_stocks:
            stocks.append(
                StockConfig(
                    symbol=symbol,
                    name=name,
                    market=market,
                    threshold=self.price_change_threshold,
                )
            )

        return stocks

    def validate(self) -> bool:
        """設定の妥当性チェック"""
        if not self.notification.webhook_url:
            return False

        if not self.stocks:
            return False

        return True
