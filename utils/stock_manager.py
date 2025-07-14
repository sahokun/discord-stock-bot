"""
株式管理ユーティリティ - 動的な株式リスト管理
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class StockEntry:
    """株式エントリ"""
    symbol: str
    name: str
    market: str


class StockManager:
    """株式管理クラス"""
    
    def __init__(self, data_file: str = "data/stocks.json"):
        self.data_file = Path(data_file)
        self.ensure_data_file()
    
    def ensure_data_file(self):
        """データファイルが存在することを確認"""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            self.save_stocks([])
    
    def load_stocks(self) -> List[StockEntry]:
        """株式リストを読み込み"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [StockEntry(**stock) for stock in data.get('stocks', [])]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_stocks(self, stocks: List[StockEntry]):
        """株式リストを保存"""
        data = {
            'stocks': [asdict(stock) for stock in stocks]
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_stock(self, symbol: str, name: str, market: str) -> bool:
        """株式を追加"""
        stocks = self.load_stocks()
        
        # 既に存在するかチェック
        if any(stock.symbol == symbol for stock in stocks):
            return False
        
        # 新しい株式を追加
        new_stock = StockEntry(symbol=symbol, name=name, market=market)
        stocks.append(new_stock)
        
        # 市場順、シンボル順でソート
        stocks.sort(key=lambda x: (x.market, x.symbol))
        
        self.save_stocks(stocks)
        return True
    
    def remove_stock(self, symbol: str) -> bool:
        """株式を削除"""
        stocks = self.load_stocks()
        
        # 削除対象を見つける
        original_count = len(stocks)
        stocks = [stock for stock in stocks if stock.symbol != symbol]
        
        if len(stocks) < original_count:
            self.save_stocks(stocks)
            return True
        
        return False
    
    def clear_stocks(self) -> int:
        """全ての株式を削除"""
        stocks = self.load_stocks()
        count = len(stocks)
        self.save_stocks([])
        return count
    
    def get_stock_by_symbol(self, symbol: str) -> Optional[StockEntry]:
        """シンボルで株式を検索"""
        stocks = self.load_stocks()
        return next((stock for stock in stocks if stock.symbol == symbol), None)
    
    def get_stocks_by_market(self, market: str) -> List[StockEntry]:
        """市場別に株式を取得"""
        stocks = self.load_stocks()
        return [stock for stock in stocks if stock.market == market]
    
    def get_all_stocks(self) -> List[StockEntry]:
        """全ての株式を取得"""
        return self.load_stocks()
    
    def stock_exists(self, symbol: str) -> bool:
        """株式が存在するかチェック"""
        return self.get_stock_by_symbol(symbol) is not None
    
    def get_stock_count(self) -> int:
        """株式の総数を取得"""
        return len(self.load_stocks())
    
    def get_market_summary(self) -> Dict[str, int]:
        """市場別サマリーを取得"""
        stocks = self.load_stocks()
        summary = {}
        
        for stock in stocks:
            summary[stock.market] = summary.get(stock.market, 0) + 1
        
        return summary