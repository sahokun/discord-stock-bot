"""
Discord コマンドパーサー - GitHub Issues経由で株式管理
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class StockCommand:
    """株式管理コマンド"""
    action: str  # add, remove, list, clear
    symbol: str
    name: str
    market: str
    user: str


class DiscordCommandParser:
    """Discord コマンドパーサー"""
    
    def __init__(self):
        self.command_patterns = {
            'add': re.compile(r'^!add[-_]?stock\s+([A-Z0-9\.\^-]+)(?:\s+(.+?))?(?:\s+(jp|us|crypto|eu|asia|ca|au))?$', re.IGNORECASE),
            'remove': re.compile(r'^!remove[-_]?stock\s+([A-Z0-9\.\^-]+)$', re.IGNORECASE),
            'list': re.compile(r'^!list[-_]?stocks?$', re.IGNORECASE),
            'clear': re.compile(r'^!clear[-_]?stocks?$', re.IGNORECASE),
        }
    
    def parse_command(self, message: str, username: str = "Unknown") -> Optional[StockCommand]:
        """
        Discordメッセージからコマンドを解析
        
        対応コマンド:
        - !add-stock AAPL Apple us
        - !add-stock 369A.T エータイ jp
        - !add-stock BTC-USD Bitcoin crypto
        - !add-stock TSLA.L Tesla eu
        - !add-stock 700.HK Tencent asia
        - !add-stock SHOP.TO Shopify ca
        - !add-stock BHP.AX BHP au
        - !remove-stock AAPL
        - !list-stocks
        - !clear-stocks
        
        市場指定なしの場合は日本株 (jp) として処理されます。
        """
        message = message.strip()
        
        # add-stock コマンド
        if match := self.command_patterns['add'].match(message):
            symbol = match.group(1).upper()
            name = match.group(2) if match.group(2) else symbol
            market = match.group(3) if match.group(3) else "jp"  # デフォルトは日本
            
            return StockCommand(
                action="add",
                symbol=symbol,
                name=name,
                market=market,
                user=username
            )
        
        # remove-stock コマンド
        elif match := self.command_patterns['remove'].match(message):
            symbol = match.group(1).upper()
            
            return StockCommand(
                action="remove",
                symbol=symbol,
                name="",
                market="",
                user=username
            )
        
        # list-stocks コマンド
        elif self.command_patterns['list'].match(message):
            return StockCommand(
                action="list",
                symbol="",
                name="",
                market="",
                user=username
            )
        
        # clear-stocks コマンド
        elif self.command_patterns['clear'].match(message):
            return StockCommand(
                action="clear",
                symbol="",
                name="",
                market="",
                user=username
            )
        
        return None
    
    
    def format_github_issue(self, command: StockCommand) -> Dict[str, str]:
        """GitHub Issue用のフォーマット"""
        if command.action == "add":
            title = f"Add Stock: {command.symbol} ({command.name})"
            body = f"""
## 株式追加リクエスト

**シンボル**: {command.symbol}
**名前**: {command.name}
**市場**: {command.market}
**リクエスト者**: {command.user}

### 実行アクション
- [ ] 株式を監視リストに追加
- [ ] 設定ファイルを更新
- [ ] Discord通知を送信

---
*このIssueは自動的に作成されました*
"""
        elif command.action == "remove":
            title = f"Remove Stock: {command.symbol}"
            body = f"""
## 株式削除リクエスト

**シンボル**: {command.symbol}
**リクエスト者**: {command.user}

### 実行アクション
- [ ] 株式を監視リストから削除
- [ ] 設定ファイルを更新
- [ ] Discord通知を送信

---
*このIssueは自動的に作成されました*
"""
        elif command.action == "list":
            title = f"List Current Stocks"
            body = f"""
## 現在の監視銘柄リスト要求

**リクエスト者**: {command.user}

### 実行アクション
- [ ] 現在の監視銘柄リストを取得
- [ ] Discord通知を送信

---
*このIssueは自動的に作成されました*
"""
        elif command.action == "clear":
            title = f"Clear All Stocks"
            body = f"""
## 全監視銘柄削除リクエスト

**リクエスト者**: {command.user}

⚠️ **警告**: この操作は全ての監視銘柄を削除します

### 実行アクション
- [ ] 全監視銘柄を削除
- [ ] 設定ファイルを更新
- [ ] Discord通知を送信

---
*このIssueは自動的に作成されました*
"""
        
        return {
            "title": title,
            "body": body,
            "labels": ["discord-command", f"action-{command.action}"]
        }