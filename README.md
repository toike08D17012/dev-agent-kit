---
title: Python Workspace Template
description: Dev Container、uv、Ruff、Mypy を備えた Python 開発環境テンプレート
---

# Python Workspace Template

日本語 | [English](README_en.md)

Python プロジェクト向けのテンプレートリポジトリです。Dev Container と `uv` による開発環境に加え、Ruff・Mypy・pytest の実行ラッパーと、GitHub Copilot / Codex / Claude Code 向けの共通 Coding Agent 設定を提供します。

## 1. 新規プロジェクトでの初期設定

このテンプレートからプロジェクトを作成したら、まず以下を変更してください。

- `README.md` / `README_en.md` のプロジェクト説明
- `src/python_workspace_template/` のディレクトリ名（例: `src/<repository_name>/`）
- `docker/docker-compose.yml` の `image`、`volumes`、`working_dir`
- `.devcontainer/devcontainer.json` の `name`、`workspaceFolder`

## 2. 主な機能

- **依存関係管理:** `uv`
- **開発環境:** VS Code Dev Container
- **Lint / フォーマット:** Ruff
- **型チェック:** Mypy
- **テスト:** pytest
- **機械学習:** CPU / CUDA 用 PyTorch の動的インストール設定
- **Coding Agent:** 共通の指示・Skills・Agents をホスト別の配置先に配布する CLI

## 3. 使い始める

### 3.1 Coding Agent 用ファイルの配布

`agent-source/` に置いた共通ファイルを、対象リポジトリに展開します。

```bash
uv run dev-agent-kit --target-dir /path/to/repository
```

既定では GitHub Copilot、Codex、Claude Code 向けのファイルを生成します。既存の出力先に異なる内容のファイルがある場合は失敗するため、上書きが必要な場合だけ `--force` を指定してください。

```bash
uv run dev-agent-kit --target-dir /path/to/repository --force
```

`--disable-copilot`、`--disable-codex`、`--disable-claude-code` で各出力先を無効にできます。`AGENTS.md` と `.agents/instructions/*.md` は常に生成され、GitHub Copilot または Codex が有効な場合は `.agents/skills/` も生成されます。`.github/copilot-instructions.md` と `.github/skills/` は生成しません。

### 3.2 Dev Container の起動

VS Code でリポジトリを開き、Dev Containers 拡張機能からコンテナを起動します。`postCreateCommand` が `uv sync` を実行して開発環境をセットアップします。

### 3.3 依存関係の追加

```bash
uv add <package_name>
```

## 4. 品質チェック

プロジェクトの検証には `scripts/pre-commit/` 配下のラッパーを使用します。**確認だけの場合は読み取り専用のオプションを使い、自動修正は必要なときだけ実行します。** 変更箇所が明らかな場合は、対象ファイルや関連テストに絞ってから必要に応じて範囲を広げてください。

### 4.1 確認のみ（ソースを自動修正しない）

```bash
./scripts/pre-commit/ruff-check.sh .
./scripts/pre-commit/ruff-format.sh --check .
./scripts/pre-commit/mypy.sh .
./scripts/pre-commit/pytest.sh
```

上記は全体確認の例です。日常の小さな変更では、各ラッパーに対象ファイル・ディレクトリ・テストノードを指定できます。コマンドの成功を確認したら、関連ファイルや設定を変更しない限り同じチェックを繰り返す必要はありません。

`pytest.sh` は pytest の終了コード `5`（テスト未収集）を成功として扱います。ただし、この場合は**テストが通過したのではなく、テストが実行されなかった**ことに注意してください。

### 4.2 明示的に自動修正・整形する場合

```bash
# 対象に絞って lint の自動修正
./scripts/pre-commit/ruff-check.sh --fix src/package/module.py

# 対象に絞ってフォーマット
./scripts/pre-commit/ruff-format.sh src/package/module.py
```

確認だけの依頼では `--fix` や書き込みを伴うフォーマットを実行しません。Ruff の `--unsafe-fixes` は明示的に許可された場合のみ使用します。

ラッパーはホストからは `./docker/run-docker.sh` 経由で実行し、Dev Container / プロジェクトコンテナ内ではその環境で実行する設計です。**ホストにインストールした Python ツールへ暗黙にフォールバックしません。** 各ラッパーをさらに Docker ラッパーで包む必要はありません。

## 5. Docker で任意のコマンドを実行する

`docker/docker-compose.yml` は単一ファイル構成で、GPU 設定は `gpu` profile にまとめています。`docker/run-docker.sh` は `nvidia-smi` を確認し、NVIDIA GPU が利用可能なら `app-gpu`、そうでなければ `app` サービスを選択します。CPU/GPU と UID/GID の扱いはラッパーに任せてください。

```bash
# デフォルトのシェル
./docker/run-docker.sh

# 任意のプロジェクトコマンド
./docker/run-docker.sh python -m package.module
```

通常は `docker compose run ...` を直接使わず、ラッパーを経由してください。テスト・lint・型チェックには、前節の専用ラッパーを優先します。

## 6. Docker ベースイメージの切り替え

既定のベースイメージは `ubuntu:24.04` です。GPU / ML 用に切り替える場合は、`docker/Dockerfile` の先頭を変更します。

```dockerfile
# 既定
FROM ubuntu:24.04

# CUDA 対応例（置き換えて使用）
FROM nvidia/cuda:13.0.2-cudnn-runtime-ubuntu24.04
```

## 7. Coding Agent の作業フロー

配布した Skills を使用する場合、役割を次のように分けることで重複調査や過剰検証を抑えられます。

| Skill | 役割 |
| --- | --- |
| `repository-overview` | リポジトリ全体の地図を作成し、必要に応じて差分更新する |
| `targeted-repository-research` | 特定機能や変更影響を必要な範囲だけ調査する |
| `implementation-plan` | 実装方針と最小限の検証計画を文書化する |
| `run-in-docker` | 任意のプロジェクトコマンドを Docker ラッパー経由で実行する |
| `run-ruff-check` / `run-ruff-format` | lint・整形の確認、または許可された自動修正を行う |
| `run-mypy` / `run-pytest` | 型チェック・テストを専用ラッパー経由で実行する |

コード変更時は、必要な調査を再利用し、実装前の Plan を人間が確認してから作業を進める運用を想定しています。各 Skill は、指定範囲のチェックが十分に成功した時点で停止し、理由なく全体検証を繰り返しません。

## 8. 主なディレクトリ

| パス | 用途 |
| --- | --- |
| `agent-source/` | 配布元となる共通の Coding Agent 設定 |
| `AGENTS.md` | 生成される共通の Coding Agent 向けガイドライン |
| `.agents/instructions/` | 生成される言語別・用途別の指示 |
| `.agents/skills/` | 対象ホスト有効時に生成される Skills |
| `.devcontainer/` | VS Code Dev Container 設定 |
| `docker/` | Dockerfile、Compose、実行ラッパー |
| `scripts/pre-commit/` | 品質チェック用ラッパー |
| `src/` | Python ソースコード |
| `tests/` | テストコード |
