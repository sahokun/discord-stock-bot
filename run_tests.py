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


def run_linting():
    """コードリンティングを実行"""
    try:
        print("=== Black フォーマットチェック ===")
        result = subprocess.run(
            [sys.executable, "-m", "black", "--check", ".", "--exclude", "venv"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("フォーマットの問題が見つかりました:")
            print(result.stdout)
            print(result.stderr)
        else:
            print("フォーマットOK")

        print("\n=== Flake8 リンティング ===")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "flake8",
                ".",
                "--ignore=E501,F401,F811,E203,W503,W504",
                "--max-line-length=88",
                "--exclude=venv",
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("リンティングの問題が見つかりました:")
            print(result.stdout)
            print(result.stderr)
        else:
            print("リンティングOK")

        return result.returncode == 0

    except Exception as e:
        print(f"リンティング実行エラー: {e}")
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
    lint_success = run_linting()

    print("\n=== 結果 ===")
    print(f"テスト: {'成功' if test_success else '失敗'}")
    print(f"リンティング: {'成功' if lint_success else '失敗'}")

    if test_success and lint_success:
        print("すべてのチェックが成功しました！")
        sys.exit(0)
    else:
        print("いくつかのチェックが失敗しました")
        sys.exit(1)
