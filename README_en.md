---
title: Python Workspace Template
description: Python development template with Dev Container, uv, Ruff, and Mypy
---

# Python Workspace Template

[日本語](README.md) | English

A template repository for Python projects. It provides a development environment based on Dev Container and `uv`, wrappers for Ruff, Mypy, and pytest, and shared Coding Agent assets for GitHub Copilot, Codex, and Claude Code.

## 1. Initial customization

When creating a project from this template, update these items first:

- The project description in `README.md` and `README_en.md`
- The directory name `src/python_workspace_template/` (for example, `src/<repository_name>/`)
- `image`, `volumes`, and `working_dir` in `docker/docker-compose.yml`
- `name` and `workspaceFolder` in `.devcontainer/devcontainer.json`

## 2. Features

- **Dependency management:** `uv`
- **Development environment:** VS Code Dev Container
- **Lint / formatting:** Ruff
- **Type checking:** Mypy
- **Testing:** pytest
- **Machine learning:** Dynamic PyTorch installation configuration for CPU / CUDA
- **Coding Agents:** A CLI that distributes shared instructions, Skills, and Agents to host-specific locations

## 3. Getting started

### 3.1 Distribute Coding Agent assets

Expand the shared files in `agent-source/` into a target repository:

```bash
uv run dev-agent-kit --target-dir /path/to/repository
```

By default, the command generates files for GitHub Copilot, Codex, and Claude Code. It fails if an existing destination file has different contents. Use `--force` only when you intend to overwrite those generated files.

```bash
uv run dev-agent-kit --target-dir /path/to/repository --force
```

Use `--disable-copilot`, `--disable-codex`, or `--disable-claude-code` to disable an individual target. `AGENTS.md` and `.agents/instructions/*.md` are always generated. When GitHub Copilot or Codex is enabled, `.agents/skills/` is generated as well. The command does not generate `.github/copilot-instructions.md` or `.github/skills/`.

### 3.2 Start the Dev Container

Open the repository in VS Code and start the container using the Dev Containers extension. `postCreateCommand` runs `uv sync` to set up the development environment.

### 3.3 Add dependencies

```bash
uv add <package_name>
```

## 4. Quality checks

Use the wrappers in `scripts/pre-commit/` for project validation. **Use read-only options when checking status, and apply automatic fixes only when changes are intended.** For a localized change, begin with the affected files or relevant tests; expand the scope only when needed.

### 4.1 Verification only (no automatic source edits)

```bash
./scripts/pre-commit/ruff-check.sh .
./scripts/pre-commit/ruff-format.sh --check .
./scripts/pre-commit/mypy.sh .
./scripts/pre-commit/pytest.sh
```

These are examples of project-wide checks. For routine small changes, pass a specific file, directory, or test node to the relevant wrapper. Once the necessary checks succeed, there is no need to repeat them unless related files or configuration change.

`pytest.sh` treats pytest exit code `5` (no tests collected) as a successful wrapper exit. This does **not** mean the tests passed: no tests were executed.

### 4.2 Explicit automatic fixes and formatting

```bash
# Apply lint fixes to a focused target
./scripts/pre-commit/ruff-check.sh --fix src/package/module.py

# Format a focused target
./scripts/pre-commit/ruff-format.sh src/package/module.py
```

Do not add `--fix` or run a writing formatter for a verification-only request. Use Ruff's `--unsafe-fixes` only with explicit authorization.

The wrappers are designed to use `./docker/run-docker.sh` when called from the host, and the current environment when called inside the Dev Container / project container. **They do not silently fall back to Python tools installed on the host.** Do not wrap the dedicated scripts in another Docker wrapper call.

## 5. Run arbitrary commands in Docker

`docker/docker-compose.yml` is a single Compose file with GPU configuration under the `gpu` profile. `docker/run-docker.sh` checks `nvidia-smi` and selects the `app-gpu` service when an NVIDIA GPU is available, or `app` otherwise. Let the wrapper handle CPU/GPU selection and UID/GID mapping.

```bash
# Start the default shell
./docker/run-docker.sh

# Run a project command
./docker/run-docker.sh python -m package.module
```

For normal use, prefer the wrapper over direct `docker compose run ...` commands. For tests, lint, and type checking, prefer the dedicated wrappers in the preceding section.

## 6. Switch the Docker base image

The default base image is `ubuntu:24.04`. For GPU / ML workloads, replace the first line of `docker/Dockerfile`:

```dockerfile
# Default
FROM ubuntu:24.04

# CUDA-capable example (use instead of the default)
FROM nvidia/cuda:13.0.2-cudnn-runtime-ubuntu24.04
```

## 7. Coding Agent workflow

When the distributed Skills are installed, their responsibilities are separated to avoid duplicate research and excessive verification.

| Skill | Responsibility |
| --- | --- |
| `repository-overview` | Create a repository map and refresh it when relevant changes occur |
| `targeted-repository-research` | Investigate a specific feature or change impact within the necessary scope |
| `implementation-plan` | Document an implementation approach and a minimal validation plan |
| `run-in-docker` | Run arbitrary project commands through the Docker wrapper |
| `run-ruff-check` / `run-ruff-format` | Verify lint/formatting or apply authorized automatic changes |
| `run-mypy` / `run-pytest` | Run type checks and tests through dedicated wrappers |

For code changes, the intended workflow is to reuse existing research, have a human review the plan before implementation, and run the checks justified by that plan. Each Skill should stop after the required scope passes rather than repeating project-wide validation without a reason.

## 8. Main directories

| Path | Purpose |
| --- | --- |
| `agent-source/` | Source of shared Coding Agent assets |
| `AGENTS.md` | Generated shared Coding Agent guidelines |
| `.agents/instructions/` | Generated language-specific and task-specific instructions |
| `.agents/skills/` | Generated Skills when the relevant hosts are enabled |
| `.devcontainer/` | VS Code Dev Container configuration |
| `docker/` | Dockerfile, Compose, and command wrapper |
| `scripts/pre-commit/` | Quality-check wrappers |
| `src/` | Python source code |
| `tests/` | Tests |
