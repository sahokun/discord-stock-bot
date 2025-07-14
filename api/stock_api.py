"""
株価データAPI
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests
import yfinance as yf

logger = logging.getLogger(__name__)


@dataclass
class StockPrice:
    """株価データ"""

    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    volume: int
    timestamp: datetime
    market: str


class StockPriceAPI:
    """株価データAPI"""

    def __init__(self, config):
        self.config = config
        self.cache = {}
        self.cache_timeout = 60  # キャッシュタイムアウト（秒）

    def get_stock_price(
        self, symbol: str, name: str, market: str
    ) -> Optional[StockPrice]:
        """株価データを取得"""
        try:
            # キャッシュチェック
            cache_key = f"{symbol}_{market}"
            if self._is_cache_valid(cache_key):
                logger.debug(f"キャッシュから株価データを取得: {symbol}")
                return self.cache[cache_key]["data"]

            # yfinanceで株価取得（リトライ機能付き）
            stock_price = self._fetch_with_retry(symbol, name, market)

            if stock_price:
                # キャッシュに保存
                self.cache[cache_key] = {
                    "data": stock_price,
                    "timestamp": datetime.now(),
                }
                logger.debug(f"株価データを取得してキャッシュに保存: {symbol}")

            return stock_price

        except Exception as e:
            logger.error(f"株価取得エラー {symbol}: {e}")
            return None

    def get_all_prices(self) -> List[StockPrice]:
        """全銘柄の株価を取得"""
        prices = []

        for stock_config in self.config.stocks:
            price = self.get_stock_price(
                stock_config.symbol, stock_config.name, stock_config.market
            )
            if price:
                prices.append(price)

        return prices

    def check_price_alerts(self) -> List[StockPrice]:
        """価格アラート対象の銘柄をチェック"""
        alerts = []

        for stock_config in self.config.stocks:
            price = self.get_stock_price(
                stock_config.symbol, stock_config.name, stock_config.market
            )

            if price and abs(price.change_percent) >= stock_config.threshold:
                alerts.append(price)

        return alerts

    def _is_cache_valid(self, cache_key: str) -> bool:
        """キャッシュの有効性をチェック"""
        if cache_key not in self.cache:
            return False

        cache_time = self.cache[cache_key]["timestamp"]
        return (datetime.now() - cache_time).seconds < self.cache_timeout

    def _fetch_with_retry(
        self, symbol: str, name: str, market: str, max_retries: int = 3
    ) -> Optional[StockPrice]:
        """リトライ機能付きで株価データを取得"""
        for attempt in range(max_retries):
            try:
                # 各試行前に少し待機（レート制限対策）
                if attempt > 0:
                    wait_time = 2**attempt  # 指数バックオフ
                    logger.info(
                        f"リトライ {attempt + 1}/{max_retries} for {symbol}, {wait_time}秒待機中..."
                    )
                    time.sleep(wait_time)

                # yfinanceで株価取得（セッション設定でUser-Agent追加）
                ticker = yf.Ticker(symbol)

                # セッション設定を改善
                session = requests.Session()
                session.headers.update(
                    {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                    }
                )
                ticker.session = session

                hist = ticker.history(period="2d")

                if hist.empty:
                    logger.warning(
                        f"株価データが空です: {symbol} (試行 {attempt + 1}/{max_retries})"
                    )
                    if attempt == max_retries - 1:
                        logger.error(
                            f"最終試行でも株価データが取得できませんでした: {symbol}"
                        )
                        return None
                    continue

                # 最新の株価データ
                latest = hist.iloc[-1]
                previous = hist.iloc[-2] if len(hist) > 1 else latest

                current_price = latest["Close"]
                previous_price = previous["Close"]

                change = current_price - previous_price
                change_percent = (
                    (change / previous_price) * 100 if previous_price > 0 else 0
                )

                stock_price = StockPrice(
                    symbol=symbol,
                    name=name,
                    price=current_price,
                    change=change,
                    change_percent=change_percent,
                    volume=int(latest["Volume"]),
                    timestamp=datetime.now(),
                    market=market,
                )

                logger.info(f"株価データ取得成功: {symbol} = ${current_price:.2f}")
                return stock_price

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    logger.warning(
                        f"レート制限エラー {symbol}: {e} (試行 {attempt + 1}/{max_retries})"
                    )
                    if attempt == max_retries - 1:
                        logger.error(f"レート制限により株価取得に失敗: {symbol}")
                        return None
                    continue
                else:
                    logger.error(f"HTTPエラー {symbol}: {e}")
                    return None

            except Exception as e:
                logger.error(
                    f"株価取得エラー {symbol}: {e} (試行 {attempt + 1}/{max_retries})"
                )
                if attempt == max_retries - 1:
                    return None
                continue

        return None
