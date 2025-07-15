#!/usr/bin/env python3
"""
テスト実行スクリプト
"""

import os
import subprocess
import sys


def run_tests():
    """テストを実行"""
    try:
        # テストディレクトリが存在することを確認
        if not os.path.exists("tests"):
            print("テストディレクトリが見つかりません")
            return False

        # pytestでテストを実行
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-v", "--tb=short"],
            capture_output=True,
            text=True,
        )

        print("=== テスト実行結果 ===")
        print(result.stdout)

        if result.stderr:
            print("=== エラー出力 ===")
            print(result.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"テスト実行エラー: {e}")
        return False


if __name__ == "__main__":
    print("Discord Stock Bot - テスト実行")
    print("=" * 40)

    # 依存関係のインストール確認
    try:
        import pytest
        import requests
        import yfinance

        print("必要なパッケージが利用可能です")
    except ImportError as e:
        print(f"パッケージが不足しています: {e}")
        print("pip install -r requirements.txt を実行してください")
        sys.exit(1)

    # テスト実行
    test_success = run_tests()

    print("\n=== 結果 ===")
    print(f"テスト: {'成功' if test_success else '失敗'}")

    if test_success:
        print("すべてのテストが成功しました！")
        sys.exit(0)
    else:
        print("テストが失敗しました")
        sys.exit(1)
