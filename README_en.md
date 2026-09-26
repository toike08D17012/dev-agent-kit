---
title: Dev Agent Kit
description: Manage shared instructions, Skills, and Agents for Coding Agents and distribute them to repositories
---

# Dev Agent Kit

[日本語](README.md) | English

A repository for managing shared instructions, Skills, and Agents for Coding Agents. A CLI distributes the files in `agent-source/` to your repositories so GitHub Copilot, Codex, and Claude Code can use common development policies and workflows.

## 1. What this repository manages

| Type | Contents | Source |
| --- | --- | --- |
| Shared instructions | Development principles, plan approval, validation scope, and language policies | [agent-source/instructions/AGENTS.md](agent-source/instructions/AGENTS.md) |
| Language-specific instructions | Editing rules for Python, Markdown, and Shell | [agent-source/instructions/](agent-source/instructions/) |
| Skills | Procedures for repository research, implementation planning, and quality checks | [agent-source/skills/](agent-source/skills/) |
| Agents | Specialists for architecture, implementation location, bugs, change impact, and plan review | [agent-source/agents/](agent-source/agents/) |

Shared content is maintained in the source files. The CLI adapts output paths and Agent definition formats for each tool. Claude Code-specific instructions are maintained in [agent-source/instructions/CLAUDE.md](agent-source/instructions/CLAUDE.md).

## 2. Add assets to a repository

Check out this repository and run the following from its root with `uv` and Python 3.14 or later available:

```bash
uv sync
uv run dev-agent-kit --target-dir /path/to/repository
```

By default, the command generates files for GitHub Copilot, Codex, and Claude Code. If `--target-dir` is omitted, files are distributed to the current directory.

### Output paths

Paths below are relative to the target repository root.

| Target | Output paths |
| --- | --- |
| Always generated | `AGENTS.md`, `.agents/instructions/*.md` |
| GitHub Copilot or Codex enabled | `.agents/skills/` |
| GitHub Copilot | `.github/agents/*.agent.md` |
| Codex | `.codex/agents/*.toml` |
| Claude Code | `.claude/CLAUDE.md`, `.claude/skills/`, `.claude/agents/*.md` |

`.claude/CLAUDE.md` references the root `AGENTS.md`. The command does not generate `.github/copilot-instructions.md` or `.github/skills/`.

### Select target tools

Use `--disable-copilot`, `--disable-codex`, or `--disable-claude-code` to disable output for an individual tool. For example, to generate only Codex assets:

```bash
uv run dev-agent-kit --target-dir /path/to/repository --disable-copilot --disable-claude-code
```

`AGENTS.md` and `.agents/instructions/*.md` are generated even when all tools are disabled. To use a different source directory, pass `--source-dir /path/to/agent-source`. The default source is `./agent-source`.

### Update existing files

Existing files with identical contents are left as they are. Files with different contents cause an error. Review the differences and use `--force` only when you intend to overwrite them.

```bash
uv run dev-agent-kit --target-dir /path/to/repository --force
```

Files are written one at a time, so an error can leave earlier outputs in place. Files removed from the source and existing files for disabled tools are not automatically deleted.

## 3. Maintain instructions, Skills, and Agents

To update shared policies or workflows, edit the relevant files in `agent-source/` and redistribute them to target repositories with the CLI. Supporting files such as Skill templates are distributed as well.

To apply changes to this repository itself, review the differences and run:

```bash
uv run dev-agent-kit --target-dir . --force
```

Edits made directly to generated files in a target repository do not update the source. A later run with `--force` can overwrite those edits, so maintain changes you want to keep sharing in the source files.

### Main Skills

| Skill | Responsibility |
| --- | --- |
| `repository-overview` | Create and update a repository map |
| `targeted-repository-research` | Investigate a specific feature or change impact within the necessary scope |
| `implementation-plan` | Document an implementation approach and validation plan |
| `run-in-docker` | Run project commands through the Docker wrapper |
| `run-ruff-check` / `run-ruff-format` | Verify lint/formatting or apply authorized automatic changes |
| `run-mypy` / `run-pytest` | Run type checks and tests through dedicated wrappers |

The distributed instructions encourage reusing existing research, obtaining human approval of an implementation plan for non-trivial code or configuration changes, and validating the scope justified by the change.

The `run-*` Skills reference `scripts/pre-commit/` and `docker/run-docker.sh` in the target repository. The CLI does not distribute these scripts or the development environment. Provide the scripts or adapt the Skill procedures to the target project's setup.

## 4. Develop and validate this repository

The distribution CLI is implemented in Python, with dependencies managed by `uv`. VS Code Dev Container and Docker configuration are also included.

### Quality checks

Use the dedicated wrappers in `scripts/pre-commit/`, starting with files or tests relevant to the change.

```bash
./scripts/pre-commit/pytest.sh tests/test_agent_distribution.py
./scripts/pre-commit/ruff-check.sh src/dev_agent_kit tests
./scripts/pre-commit/ruff-format.sh --check src/dev_agent_kit tests
./scripts/pre-commit/mypy.sh src/dev_agent_kit
```

Use read-only options for verification. Apply Ruff's `--fix` or a writing formatter only when automatic changes are intended, keeping the target scope focused.

The wrappers use Docker when called from the host and the current environment inside the Dev Container / project container. They do not silently fall back to Python tools installed on the host. Do not wrap the dedicated scripts in another Docker wrapper call.

`pytest.sh` treats exit code `5` (no tests collected) as a successful wrapper exit, but no tests were executed in that case.

### Main directories

| Path | Purpose |
| --- | --- |
| `agent-source/` | Source instructions, Skills, and Agents |
| `src/dev_agent_kit/` | Distribution CLI and tool-specific output logic |
| `tests/` | Tests for distribution and other behavior |
| `.agents/`, `.github/agents/`, `.codex/agents/`, `.claude/` | Distributed assets used in this repository |
| `scripts/pre-commit/` | Quality-check wrappers |
| `.devcontainer/`, `docker/` | Development environment for this repository |
