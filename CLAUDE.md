# CLAUDE.md

このファイルは、このリポジトリのコードを操作する際にClaude Code (claude.ai/code)にガイダンスを提供します。

## プロジェクト概要

これはDiscordボットプロジェクトです。現在のコードベースは、包括的なDockerとVS Code設定を持つ開発環境のスケルトンですが、実際のPythonソースコードは実装する必要があります。

## 開発環境

### コンテナ設定

- **ベースイメージ**: Python 3.12.6-bookworm
- **ユーザー**: 非特権ユーザー（UID/GID 1000）
- **言語**: 日本語ロケール（ja_JP.UTF-8）
- **仮想環境**: `/src/venv/`（初回実行時に自動作成）

### 開発開始

```bash
# 開発コンテナをビルドして起動
docker-compose -f .devcontainer/development/docker-compose.yml up --build

# またはVS Code Dev Containers拡張機能を使用
# VS Codeで開き、「コンテナで再開」を選択
```

### Python環境

```bash
# 仮想環境は初回コンテナ実行時に自動作成されます
# 必要に応じて手動でアクティベート:
source venv/bin/activate

# 依存関係をインストール（requirements.txtが存在する場合）:
pip install -r requirements.txt

# pipをアップグレード:
pip install --upgrade pip
```

## 一般的なコマンド

### 開発

```bash
# Blackでコードをフォーマット
black .

# Flake8でリント
flake8 . --ignore=E501,F401,F811,E203,W503,W504 --max-line-length=88

# インポートをソート
isort --profile black .

# テストを実行
pytest tests -s
```


## コードスタイル設定

### Pythonフォーマット

- **フォーマッター**: Black（行の長さ: 88）
- **インポートソート**: isort with black profile
- **リンティング**: Black互換性のための特定の無視設定を持つFlake8

### VS Code設定

- 保存時フォーマットが有効
- 自動インポート整理
- テスト用のPytest
- Pylance言語サーバー

## アーキテクチャ概要

### 現在の状態

プロジェクトには完全な開発環境が含まれていますが、ソースコードはありません。実装時は以下を考慮してください:

1. **メインアプリケーション**: Discordボットの実装
2. **データ処理**: 必要に応じたデータ処理モジュール
3. **外部API統合**: 各種APIとの統合
4. **ユーティリティ**: 共通機能の実装

### 期待される構造

```text
src/
├── bot/              # Discord bot実装
├── data/            # データ処理モジュール
├── api/             # 外部API統合
├── utils/           # ユーティリティ関数
├── tests/           # テストファイル
├── requirements.txt # Python依存関係
└── main.py         # メインアプリケーションエントリーポイント
```

## 環境変数

プロジェクトは`.env`で設定された環境変数を使用します:

- `COMPOSE_PROJECT_NAME=discord-stock-bot`

以下の追加環境変数が必要になる可能性があります:

- Discordボットトークン
- 外部API用のAPIキー
- データベース設定

## テスト

- **フレームワーク**: pytest
- **テスト発見**: `tests/`ディレクトリ
- **実行コマンド**: `pytest tests -s`
- **VS Code統合**: ワークスペースルートをPythonパスとしてpytest用に設定

## コンテナ環境変数

Dockerコンテナは以下を設定します:

- `PYTHONUNBUFFERED=1` - 即座にstdout/stderrを出力
- `PYTHONDONTWRITEBYTECODE=1` - .pycファイルを防止
- `PYTHONDEVMODE=1` - 開発モードを有効化
- `CHOKIDAR_USEPOLLING=true` - 開発用のファイル監視
- `HOME=/home/user` - ユーザーホームディレクトリ
- `TZ=Asia/Tokyo` - タイムゾーン設定
