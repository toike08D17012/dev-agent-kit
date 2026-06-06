---
name: "docker-runner"
description: "dockerコンテナ実行を run-docker.sh に統一するワークフロー。CPU/GPU自動切替、引数付き実行、品質コマンド実行を一貫化したいときに使う"
argument-hint: "実行したいコマンド。未指定なら対話シェルを起動"
user-invocable: true
disable-model-invocation: false
---

# Docker Runner Workflow

## Outcome

このスキルは、Docker 実行を常に `docker/run-docker.sh` 経由に統一します。

* CPU/GPU 切り替えは `run-docker.sh` に任せる
* `docker compose run ...` の直接実行を避ける
* ローカル実行へのフォールバックを禁止する
* 任意のコマンドとオプションをそのまま渡して実行できる

## Workflow

1. 実行したい内容を決める。
2. 直接 `docker compose run` は使わず、必ず `./docker/run-docker.sh` を使う。
3. 引数をそのまま渡して実行する。
4. 実行結果を確認し、失敗時はコマンド単位で再実行する。

## Decision Points

### 1. 引数の有無

* 引数なし: 対話シェルを起動
* 引数あり: 指定コマンドをそのまま実行

### 2. 実行コマンドの種類

* 品質チェック系: `ruff`, `mypy`, `pytest`
* アプリ実行系: `python`, `uv`, `bash`
* すべて `run-docker.sh` の引数として渡す

## Commands

```bash
./docker/run-docker.sh
```

```bash
./docker/run-docker.sh <command> [args...]
```

### Examples

```bash
# Pythonスクリプトの実行
./docker/run-docker.sh python script.py

# Ruffでのフォーマット
./docker/run-docker.sh ruff format

# 型チェック
./docker/run-docker.sh mypy .

# Pytest の詳細オプション
./docker/run-docker.sh pytest -q -k smoke
```

## Completion Checks

* Docker 実行コマンドが `./docker/run-docker.sh` になっている
* `docker compose run` を直接書いていない
* ローカル実行へのフォールバック処理が入っていない
* 必要な引数・オプションが `run-docker.sh` に透過的に渡されている
* 実行結果の成功/失敗を確認している
