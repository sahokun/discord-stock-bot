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
        """株式設定を読み込み（動的株式リスト対応）"""
        from utils.stock_manager import StockManager
        
        try:
            # 動的株式リストから読み込み
            stock_manager = StockManager()
            stock_entries = stock_manager.load_stocks()
            
            stocks = []
            for entry in stock_entries:
                stocks.append(StockConfig(
                    symbol=entry.symbol,
                    name=entry.name,
                    market=entry.market,
                    threshold=self.price_change_threshold,
                ))
            
            return stocks
            
        except Exception:
            # フォールバック: 静的な設定
            stocks = []
            fallback_stocks = [
                ("^N225", "日経平均", "jp"),
                ("369A.T", "(株)エータイ", "jp"),
                ("8136.T", "(株)サンリオ", "jp"),
                ("GSPC", "S&P 500", "us"),
                ("BTC-USD", "Bitcoin", "crypto"),
            ]
            
            for symbol, name, market in fallback_stocks:
                stocks.append(StockConfig(
                    symbol=symbol,
                    name=name,
                    market=market,
                    threshold=self.price_change_threshold,
                ))
            
            return stocks

    def validate(self) -> bool:
        """設定の妥当性チェック"""
        if not self.notification.webhook_url:
            return False

        if not self.stocks:
            return False

        return True
