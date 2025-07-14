"""
Discord通知ボット
"""

import asyncio
import json
import logging
import threading
import time
from datetime import datetime
from typing import List

import requests
import schedule

from api.stock_api import StockPrice

logger = logging.getLogger(__name__)


class DiscordStockBot:
    """Discord株価通知ボット"""

    def __init__(self, config, stock_api):
        self.config = config
        self.stock_api = stock_api
        self.last_alert_time = {}
        self.running = False

    def run(self):
        """ボットを実行（従来の継続実行版）"""
        if not self.config.validate():
            logger.error("設定が無効です")
            return

        self.running = True

        # 定期通知のスケジュール設定
        schedule.every(self.config.notification.interval).seconds.do(
            self._send_regular_update
        )

        # 価格アラートのスケジュール設定（より頻繁にチェック）
        schedule.every(30).seconds.do(self._check_price_alerts)

        # 初回実行
        self._send_regular_update()

        # メインループ
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        """ボットを停止"""
        self.running = False

    def _send_regular_update(self):
        """定期的な株価更新を送信"""
        try:
            logger.info("定期株価更新を開始")
            prices = self.stock_api.get_all_prices()

            if not prices:
                logger.warning("株価データが取得できませんでした")
                return

            # 市場別にグループ化
            jp_stocks = [p for p in prices if p.market == "jp"]
            us_stocks = [p for p in prices if p.market == "us"]
            crypto_stocks = [p for p in prices if p.market == "crypto"]

            # Discord埋め込みメッセージを作成
            embed = self._create_regular_embed(jp_stocks, us_stocks, crypto_stocks)

            # Discord Webhookで送信
            self._send_discord_message(embed)

        except Exception as e:
            logger.error(f"定期更新エラー: {e}")

    def _check_price_alerts(self):
        """価格アラートをチェック"""
        try:
            alerts = self.stock_api.check_price_alerts()

            for alert in alerts:
                # 同じ銘柄のアラートが短時間で重複しないようにチェック
                if self._should_send_alert(alert):
                    self._send_price_alert(alert)
                    self.last_alert_time[alert.symbol] = datetime.now()

        except Exception as e:
            logger.error(f"価格アラートチェックエラー: {e}")

    def _should_send_alert(self, alert: StockPrice) -> bool:
        """アラートを送信すべきかチェック"""
        if alert.symbol not in self.last_alert_time:
            return True

        # 30分以内の同じ銘柄のアラートは送信しない
        time_diff = datetime.now() - self.last_alert_time[alert.symbol]
        return time_diff.seconds > 1800  # 30分

    def _send_price_alert(self, alert: StockPrice):
        """価格アラートを送信"""
        try:
            logger.info(f"価格アラート送信: {alert.symbol}")

            # 変動の方向を判定
            direction = "急上昇" if alert.change_percent > 0 else "急落"
            color = 0x00FF00 if alert.change_percent > 0 else 0xFF0000

            embed = {
                "title": f"🚨 {direction}アラート",
                "description": f"**{alert.name} ({alert.symbol})**",
                "color": color,
                "fields": [
                    {
                        "name": "現在価格",
                        "value": self._format_price(alert.price, alert.market),
                        "inline": True,
                    },
                    {"name": "変動額", "value": f"{alert.change:+.2f}", "inline": True},
                    {
                        "name": "変動率",
                        "value": f"{alert.change_percent:+.2f}%",
                        "inline": True,
                    },
                ],
                "timestamp": alert.timestamp.isoformat(),
            }

            self._send_discord_message(embed)

        except Exception as e:
            logger.error(f"価格アラート送信エラー: {e}")

    def _create_regular_embed(
        self,
        jp_stocks: List[StockPrice],
        us_stocks: List[StockPrice],
        crypto_stocks: List[StockPrice],
    ):
        """定期更新用の埋め込みメッセージを作成"""
        embed = {
            "title": "📊 株価定期更新",
            "description": "定期的な株価情報をお知らせします",
            "color": 0x0099FF,
            "fields": [],
            "timestamp": datetime.now().isoformat(),
        }

        # 日本株
        if jp_stocks:
            jp_text = self._format_stock_list(jp_stocks)
            embed["fields"].append(
                {
                    "name": "🇯🇵 日本株・日本株インデックス",
                    "value": jp_text,
                    "inline": False,
                }
            )

        # 米国株
        if us_stocks:
            us_text = self._format_stock_list(us_stocks)
            embed["fields"].append(
                {
                    "name": "🇺🇸 米国株・米国株インデックス",
                    "value": us_text,
                    "inline": False,
                }
            )

        # 暗号通貨
        if crypto_stocks:
            crypto_text = self._format_stock_list(crypto_stocks)
            embed["fields"].append(
                {"name": "₿ 暗号通貨", "value": crypto_text, "inline": False}
            )

        return embed

    def _format_stock_list(self, stocks: List[StockPrice]) -> str:
        """株価リストをフォーマット"""
        lines = []
        for stock in stocks:
            change_icon = (
                "📈"
                if stock.change_percent > 0
                else "📉" if stock.change_percent < 0 else "➡️"
            )
            price_str = self._format_price(stock.price, stock.market)
            lines.append(
                f"{change_icon} **{stock.name}**: {price_str} ({stock.change_percent:+.2f}%)"
            )
        return "\n".join(lines)

    def _format_price(self, price: float, market: str) -> str:
        """価格をフォーマット"""
        if market == "jp":
            return f"¥{price:,.0f}"
        elif market == "crypto":
            return f"${price:,.0f}"
        else:
            return f"${price:.2f}"

    def _send_discord_message(self, embed):
        """Discord Webhookでメッセージを送信"""
        try:
            webhook_url = self.config.notification.webhook_url

            payload = {"embeds": [embed]}

            response = requests.post(
                webhook_url, json=payload, headers={"Content-Type": "application/json"}
            )

            if response.status_code == 204:
                logger.info("Discord通知送信成功")
            else:
                logger.error(f"Discord通知送信失敗: {response.status_code}")

        except Exception as e:
            logger.error(f"Discord通知送信エラー: {e}")
