---
title: Python Workspace Template
description: Modern Python development environment with Dev Container, uv, Ruff, and Mypy
---

## Python Workspace Template

[English Versions](README_en.md) | 日本語

Pythonプロジェクト開発用のテンプレートリポジトリです。
Dev Container、uv、Ruff、Mypyを用いたモダンな開発環境を提供します。

## テンプレート利用時の初期設定

このテンプレートを新規プロジェクトとして使う場合は、最初に以下を更新してください。

* `README.md` / `README_en.md` のプロジェクト説明
* `src/python_workspace_template` のディレクトリ名（例: `src/<repository_name>`）
* `docker/docker-compose.yml` の `image` / `volumes` / `working_dir`
* `.devcontainer/devcontainer.json` の `name` / `workspaceFolder`

## 機能・特徴

* **パッケージ管理**: `uv` を使用した高速な依存関係解決
* **開発環境**: Dev Container (`.devcontainer`) による一貫した環境
* **静的解析・フォーマット**: `ruff` による高速なLint/Format
* **型チェック**: `mypy` による静的型チェック
* **機械学習対応**: PyTorch (CPU/CUDA) の動的なインストール設定済み

## 使い方

### 1. Dev Container の起動

VS Code で本リポジトリを開き、推奨される拡張機能「Dev Containers」を使用してコンテナを起動してください。
`postCreateCommand` により、自動的に `uv sync` が実行され、環境がセットアップされます。

### 2. 依存関係の追加

パッケージを追加する場合は `uv` を使用します。

```bash
uv add <package_name>
```

### 3. 品質管理コマンド

本プロジェクトでは `AGENTS.md` に基づき、以下の wrapper スクリプト経由での品質チェックを推奨しています。

```bash
# フォーマット、Lint自動修正、型チェック、テストを一括実行
./scripts/pre-commit/ruff-format.sh && \
./scripts/pre-commit/ruff-check.sh --fix && \
./scripts/pre-commit/mypy.sh . && \
./scripts/pre-commit/pytest.sh
```

各 wrapper は内部で `./docker/run-docker.sh` を使って実行されます。
このテンプレートではローカルフォールバックを行わず、`docker` 実行を必須とします。

pytest は追加オプションもそのまま渡せます。

```bash
# 例: 追加オプションつきで実行
./scripts/pre-commit/pytest.sh -q -k smoke
```

### 4. Docker 実行（CPU/GPU 自動切り替え）

`docker/docker-compose.yml` は 1 ファイルに統合されており、GPU 構成は `profiles`（`gpu`）で管理しています。

`docker/run-docker.sh` を使うと、`nvidia-smi` の実行可否を判定して自動で切り替えます。

* NVIDIA GPU が使える場合: `app-gpu` サービス（`--profile gpu`）で起動
* NVIDIA GPU が使えない場合: `app` サービスで起動

```bash
# デフォルトシェル起動
./docker/run-docker.sh

# 任意コマンド実行
./docker/run-docker.sh pytest -q
```

日常運用では、`docker compose run ...` の直接実行ではなく `./docker/run-docker.sh` の利用を推奨します。

## Docker ベースイメージの切り替え

デフォルトのベースイメージは軽量な `ubuntu:24.04` です。
GPU / 機械学習用途では、`docker/Dockerfile` の先頭を以下のように書き換えてください。

```dockerfile
# 変更前（デフォルト）
FROM ubuntu:24.04

# 変更後（ML/CUDA用）
FROM nvidia/cuda:13.0.2-cudnn-runtime-ubuntu24.04
```

## ディレクトリ構成

* `.devcontainer/`: Dev Container 設定 (VS Code用)
* `docker/`: docker関連ファイル
* `AGENTS.md`: コーディング規約 (Google Style, Ruff設定など)
