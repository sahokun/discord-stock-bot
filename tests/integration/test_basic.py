#!/usr/bin/env python3
"""
基本機能テスト
"""

import logging

from api.stock_api import StockPriceAPI
from utils.config import Config

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def test_basic_functionality():
    """基本機能をテスト"""
    print("=== 基本機能テスト ===")

    # 設定テスト
    config = Config()
    print("設定読み込み: OK")
    print(f"監視銘柄数: {len(config.stocks)}")

    # Stock API テスト
    stock_api = StockPriceAPI(config)

    # 単一銘柄テスト（複数銘柄で順次テスト）
    print("\n=== 単一銘柄テスト ===")
    test_stocks = [
        ("369A.T", "(株)エータイ", "jp"),
        ("^N225", "日経平均", "jp"),
        ("^GSPC", "S&P 500", "us"),
        ("USDJPY=X", "USD/JPY", "forex"),
    ]

    success_count = 0
    for symbol, name, market in test_stocks:
        try:
            price = stock_api.get_stock_price(symbol, name, market)
            if price:
                if market == "jp":
                    currency = "¥"
                elif market == "forex":
                    currency = ""  # 為替レートには通貨記号を付けない
                else:
                    currency = "$"

                if market == "forex":
                    print(
                        f"✓ {price.name}: {price.price:.2f} ({price.change_percent:+.2f}%)"
                    )
                else:
                    print(
                        f"✓ {price.name}: {currency}{price.price:.2f} ({price.change_percent:+.2f}%)"
                    )
                success_count += 1
            else:
                print(f"✗ {symbol} ({name}): データなし")
        except Exception as e:
            print(f"✗ {symbol} ({name}) エラー: {e}")

    print(f"\n結果: {success_count}/{len(test_stocks)} 銘柄で取得成功")

    print("\n=== 設定検証 ===")
    print(f"✓ 通知設定: {'有効' if config.notification.webhook_url else '無効'}")
    print(f"✓ 価格変動閾値: {config.price_change_threshold}%")
    print(f"✓ 通知間隔: {config.notification.interval}秒")

    print("\n=== 監視銘柄一覧 ===")
    for stock in config.stocks[:5]:  # 最初の5銘柄のみ表示
        print(f"  {stock.symbol}: {stock.name} ({stock.market})")
    if len(config.stocks) > 5:
        print(f"  ... 他{len(config.stocks) - 5}銘柄")


if __name__ == "__main__":
    test_basic_functionality()
