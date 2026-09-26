---
title: Dev Agent Kit
description: Coding Agent 向けの共通指示・Skills・Agents を一元管理し、各リポジトリへ配布するツール
---

# Dev Agent Kit

日本語 | [English](README_en.md)

Coding Agent 向けの指示・Skills・Agents を一元管理するリポジトリです。GitHub Copilot、Codex、Claude Code で共通の開発方針や作業手順を使えるよう、`agent-source/` にまとめたファイルを CLI で各リポジトリへ配布します。

## 1. 管理するもの

| 種類 | 内容 | 配布元 |
| --- | --- | --- |
| 共通指示 | 開発原則、計画の確認、検証範囲、言語方針など | [agent-source/instructions/AGENTS.md](agent-source/instructions/AGENTS.md) |
| 言語別の指示 | Python、Markdown、Shell の編集ルール | [agent-source/instructions/](agent-source/instructions/) |
| Skills | リポジトリ調査、実装計画、品質チェックなどの作業手順 | [agent-source/skills/](agent-source/skills/) |
| Agents | 構成・実装箇所・不具合・変更影響の調査、計画レビューなどを担う専門エージェント | [agent-source/agents/](agent-source/agents/) |

共通の内容は配布元で管理し、CLI がツールごとの配置先や Agent 定義の形式に合わせて出力します。Claude Code 固有の指示は [agent-source/instructions/CLAUDE.md](agent-source/instructions/CLAUDE.md) で管理します。

## 2. 対象リポジトリへ導入する

このリポジトリを取得し、`uv` と Python 3.14 以上を利用できる環境で、リポジトリのルートから実行します。

```bash
uv sync
uv run dev-agent-kit --target-dir /path/to/repository
```

既定では GitHub Copilot、Codex、Claude Code のすべてに向けてファイルを生成します。`--target-dir` を省略すると、現在のディレクトリに配布します。

### 出力先

以下は対象リポジトリのルートからの相対パスです。

| 対象 | 出力先 |
| --- | --- |
| 常に生成 | `AGENTS.md`、`.agents/instructions/*.md` |
| GitHub Copilot または Codex が有効 | `.agents/skills/` |
| GitHub Copilot | `.github/agents/*.agent.md` |
| Codex | `.codex/agents/*.toml` |
| Claude Code | `.claude/CLAUDE.md`、`.claude/skills/`、`.claude/agents/*.md` |

`.claude/CLAUDE.md` はルートの `AGENTS.md` を参照します。`.github/copilot-instructions.md` と `.github/skills/` は生成しません。

### 配布対象を選ぶ

`--disable-copilot`、`--disable-codex`、`--disable-claude-code` で各ツール向けの出力を無効にできます。たとえば、Codex 向けだけを生成する場合は次のように実行します。

```bash
uv run dev-agent-kit --target-dir /path/to/repository --disable-copilot --disable-claude-code
```

すべてのツールを無効にしても、`AGENTS.md` と `.agents/instructions/*.md` は生成されます。配布元を変更する場合は `--source-dir /path/to/agent-source` を指定します。既定の配布元は `./agent-source` です。

### 既存ファイルを更新する

出力先に同じ内容のファイルがあれば、そのまま扱います。異なる内容のファイルがある場合はエラーになります。差分を確認し、上書きする場合だけ `--force` を指定してください。

```bash
uv run dev-agent-kit --target-dir /path/to/repository --force
```

配布はファイル単位で進むため、途中でエラーになった場合も、それ以前に出力されたファイルは残ります。配布元から削除したファイルや、無効にしたツールの既存ファイルは自動削除されません。

## 3. 指示・Skills・Agents を更新する

共通の指示や作業手順を変更する際は、`agent-source/` 内の該当ファイルを編集し、CLI で対象リポジトリへ再配布します。Skills に付属するテンプレートなども配布されます。

このリポジトリ自身に反映する場合は、差分を確認したうえで次を実行します。

```bash
uv run dev-agent-kit --target-dir . --force
```

配布先で生成ファイルを直接編集した場合、その変更は配布元には反映されません。次回の `--force` による上書き対象になるため、継続して共有したい変更は配布元で管理してください。

### 主な Skills

| Skill | 役割 |
| --- | --- |
| `repository-overview` | リポジトリ全体の地図を作成・更新する |
| `targeted-repository-research` | 特定機能や変更影響を必要な範囲で調査する |
| `implementation-plan` | 実装方針と検証計画を文書化する |
| `run-in-docker` | Docker ラッパー経由でプロジェクトコマンドを実行する |
| `run-ruff-check` / `run-ruff-format` | lint・整形の確認、または許可された自動修正を行う |
| `run-mypy` / `run-pytest` | 専用ラッパー経由で型チェック・テストを実行する |

配布する指示は、既存の調査結果を再利用し、非自明なコード・設定変更では実装計画を人間が承認してから進め、変更に必要な範囲を検証する運用を想定しています。

`run-*` Skills は、配布先の `scripts/pre-commit/` や `docker/run-docker.sh` を参照します。CLI はこれらのスクリプトや開発環境を配布しないため、利用先の構成に合わせてスクリプトを用意するか、Skills の手順を調整してください。

## 4. このリポジトリの開発・検証

配布 CLI は Python で実装し、依存関係は `uv` で管理しています。VS Code Dev Container と Docker の設定も含まれています。

### 品質チェック

`scripts/pre-commit/` の専用ラッパーを使用します。変更に関係するファイルやテストから確認してください。

```bash
./scripts/pre-commit/pytest.sh tests/test_agent_distribution.py
./scripts/pre-commit/ruff-check.sh src/dev_agent_kit tests
./scripts/pre-commit/ruff-format.sh --check src/dev_agent_kit tests
./scripts/pre-commit/mypy.sh src/dev_agent_kit
```

確認のみの場合は読み取り専用のオプションを使います。自動修正が必要な場合に限り、対象を絞って Ruff の `--fix` や書き込みを伴うフォーマットを実行してください。

ラッパーはホストでは Docker 経由、Dev Container / プロジェクトコンテナ内ではその環境で実行します。ホストの Python ツールへの暗黙のフォールバックは行いません。専用ラッパーをさらに Docker ラッパーで包む必要はありません。

`pytest.sh` は終了コード `5`（テスト未収集）を成功として扱いますが、その場合はテストが実行されていません。

### 主なディレクトリ

| パス | 用途 |
| --- | --- |
| `agent-source/` | 指示・Skills・Agents の配布元 |
| `src/dev_agent_kit/` | 配布 CLI とツール別の出力処理 |
| `tests/` | 配布処理などのテスト |
| `.agents/`、`.github/agents/`、`.codex/agents/`、`.claude/` | このリポジトリで使用する配布済みファイル |
| `scripts/pre-commit/` | 品質チェック用ラッパー |
| `.devcontainer/`、`docker/` | このリポジトリの開発環境 |
