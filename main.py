#!/usr/bin/env python3
"""
Discord Stock Bot - Main Entry Point
株価通知Discordボット
"""

import logging
import os
import sys

from dotenv import load_dotenv

from api.stock_api import StockPriceAPI
from bot.discord_bot import DiscordStockBot
from utils.config import Config

# 環境変数を読み込み
load_dotenv()

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def main():
    """メイン関数 - GitHub Actions用単発実行"""
    try:
        # 設定を読み込み
        config = Config()

        # Stock API初期化
        stock_api = StockPriceAPI(config)

        # Discord Bot初期化
        bot = DiscordStockBot(config, stock_api)

        # 定期通知のみ実行（単発）
        logger.info("定期株価通知を送信します...")
        bot._send_regular_update()
        logger.info("通知送信が完了しました")

    except Exception as e:
        logger.error(f"アプリケーション実行中にエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
