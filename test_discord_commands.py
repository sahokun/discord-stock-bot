#!/usr/bin/env python3
"""
Discord Commands Test
"""

from utils.discord_commands import DiscordCommandParser
from utils.stock_manager import StockManager


def test_discord_commands():
    """Discord コマンドをテスト"""
    print("=== Discord Command Parser Test ===")
    
    # コマンドパーサーのテスト
    parser = DiscordCommandParser()
    
    # テストコマンド
    test_commands = [
        "!add-stock AAPL Apple us",
        "!add-stock 369A.T エータイ jp",
        "!add-stock 369A.T エータイ",         # 市場指定なし → jp
        "!add-stock BTC-USD Bitcoin crypto",
        "!add-stock TSLA.L Tesla eu",
        "!add-stock 700.HK Tencent asia",
        "!add-stock SHOP.TO Shopify ca",
        "!add-stock BHP.AX BHP au",
        "!remove-stock AAPL",
        "!list-stocks",
        "!clear-stocks",
        "invalid command"
    ]
    
    for cmd in test_commands:
        result = parser.parse_command(cmd, "test_user")
        if result:
            print(f"✓ {cmd:40} -> {result.action}: {result.symbol:12} ({result.name:15}) [{result.market}]")
        else:
            print(f"✗ {cmd:40} -> No match")
    
    print("\n=== Stock Manager Test ===")
    # Stock Managerのテスト
    manager = StockManager()
    print(f"Initial stock count: {manager.get_stock_count()}")
    
    # 株式追加テスト
    success = manager.add_stock("TEST", "Test Stock", "us")
    print(f"Add TEST stock: {success}")
    
    # 重複追加テスト
    success = manager.add_stock("TEST", "Test Stock", "us")
    print(f"Add duplicate TEST stock: {success}")
    
    # 株式削除テスト
    success = manager.remove_stock("TEST")
    print(f"Remove TEST stock: {success}")
    
    # 存在しない株式削除テスト
    success = manager.remove_stock("NONEXISTENT")
    print(f"Remove nonexistent stock: {success}")
    
    print(f"Final stock count: {manager.get_stock_count()}")
    
    # 設定テスト
    print("\n=== Config Integration Test ===")
    from utils.config import Config
    config = Config()
    print(f"Config loaded {len(config.stocks)} stocks")
    for stock in config.stocks[:3]:  # 最初の3つだけ表示
        print(f"  - {stock.symbol}: {stock.name} ({stock.market})")


if __name__ == "__main__":
    test_discord_commands()