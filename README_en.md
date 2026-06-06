---
title: Python Workspace Template
description: Modern Python development environment with Dev Container, uv, Ruff, and Mypy
---

## Python Workspace Template

[Japanese Version](README.md) | English

A template repository for Python project development.
Provides a modern development environment using Dev Container, uv, Ruff, and Mypy.

## Initial Customization

When using this template for a new project, update the following items first.

* Project description in `README.md` and `README_en.md`
* Directory name `src/python_workspace_template` (for example, `src/<repository_name>`)
* `image`, `volumes`, and `working_dir` in `docker/docker-compose.yml`
* `name` and `workspaceFolder` in `.devcontainer/devcontainer.json`

## Features

* **Package Management**: High-speed dependency resolution using `uv`
* **Development Environment**: Consistent environment via Dev Container (`.devcontainer`)
* **Static Analysis / Formatting**: High-speed Lint/Format using `ruff`
* **Type Checking**: Static type checking using `mypy`
* **Machine Learning Support**: Pre-configured dynamic installation for PyTorch (CPU/CUDA)

## Usage

### 1. Start Dev Container

Open this repository in VS Code and start the container using the recommended "Dev Containers" extension.
`postCreateCommand` will automatically execute `uv sync` to set up the environment.

### 2. Add Dependencies

Use `uv` to add packages.

```bash
uv add <package_name>
```

### 3. Quality Control Commands

Based on `AGENTS.md`, we recommend running quality checks through the wrapper scripts below.

```bash
# Execute formatting, auto-fix linting, type checking, and tests in one go
./scripts/pre-commit/ruff-format.sh && \
./scripts/pre-commit/ruff-check.sh --fix && \
./scripts/pre-commit/mypy.sh . && \
./scripts/pre-commit/pytest.sh
```

These wrappers run via `./docker/run-docker.sh` internally.
This template enforces Docker-only execution and does not use local fallback.

`pytest` options can be passed through as-is.

```bash
# Example: pass additional pytest options
./scripts/pre-commit/pytest.sh -q -k smoke
```

### 4. Docker Execution (Automatic CPU/GPU Switching)

`docker/docker-compose.yml` is now unified into a single file, and GPU settings are managed with the `gpu` profile.

When you use `docker/run-docker.sh`, it checks `nvidia-smi` and switches automatically.

* If NVIDIA GPU is available: runs `app-gpu` service with `--profile gpu`
* If NVIDIA GPU is unavailable: runs `app` service

```bash
# Start default shell
./docker/run-docker.sh

# Run any command
./docker/run-docker.sh pytest -q
```

For normal use, prefer `./docker/run-docker.sh` instead of direct `docker compose run ...` commands.

## Switching the Docker Base Image

The default base image is the lightweight `ubuntu:24.04`.
For GPU / machine learning workloads, replace the first line of `docker/Dockerfile` as follows:

```dockerfile
# Before (default)
FROM ubuntu:24.04

# After (ML/CUDA)
FROM nvidia/cuda:13.0.2-cudnn-runtime-ubuntu24.04
```

## Directory Structure

* `.devcontainer/`: Dev Container settings (for VS Code)
* `docker/`: docker related files
* `AGENTS.md`: Coding guidelines (Google Style, Ruff settings, etc.)
