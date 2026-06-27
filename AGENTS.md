# AGENTS.md

## 1. Project Overview

This repository is primarily a Python project with Markdown documentation and shell scripts.

Before changing files, inspect the relevant implementation, tests, scripts, documentation, and configuration. Follow existing architecture and prefer small, focused changes.

## 2. Source of Truth

Use repository files as the source of truth:

- `pyproject.toml` for Python dependencies, tooling, and packaging
- existing source files and tests for implementation and behavior
- existing scripts, CI, pre-commit, README, and docs for workflows and user-facing behavior

If this document conflicts with tool configuration, prefer the tool configuration and report the inconsistency.

## 3. Language-Specific Instructions

Language-specific instructions are stored under `.agents/instructions`.

Before editing matching files, read only the relevant instruction file:

- Python / `pyproject.toml` / tests: `.agents/instructions/python.md`
- Markdown: `.agents/instructions/markdown.md`
- Shell scripts: `.agents/instructions/shell.md`

Do not edit instruction files unless explicitly requested.

## 4. General Development Principles

- Inspect relevant files before editing.
- Prefer existing patterns, utilities, naming, and architecture.
- Keep changes minimal and focused.
- Preserve public APIs unless a breaking change is explicitly requested.
- Do not make unrelated refactors, file moves, or formatting-only changes.
- Do not weaken lint, type-check, test, CI, or test coverage to make checks pass.

## 5. Dependency and Tooling Policy

- Do not add dependencies, tools, formatters, linters, frameworks, or package managers unless necessary and justified.
- Prefer the standard library, existing dependencies, and repository-defined workflows.
- When dependencies change, update the appropriate project configuration.

## 6. Plan-First Workflow

Use the `implementation-plan` skill for non-trivial repository changes that may affect source code, tests, configuration, scripts, CI, dependencies, packaging, public APIs, runtime behavior, or validation behavior.

After creating an implementation plan, stop and wait for user approval before implementation.

Markdown-only changes do not require a separate implementation plan.

If a task includes both Markdown changes and non-Markdown repository changes, apply the plan-first workflow to the non-Markdown change. The Markdown updates may be included in that plan.

## 7. Validation

After editing, run relevant checks when possible.
Use narrower checks for Markdown-only or otherwise scoped changes when appropriate.

Default validation command:

```bash
./scripts/pre-commit/checks.sh
```

If checks cannot be run, explain why. In the final response, state which checks were run or skipped.

## 8. Security and Secrets

- Do not hard-code or expose secrets, credentials, tokens, private keys, local environment files, or machine-specific configuration.
- Use environment variables or existing configuration mechanisms for sensitive values.
- Be careful when printing logs, environment variables, command output, or configuration values.

## 9. Language Policy

- Use Japanese for user-facing communication, including progress updates and final responses, unless otherwise requested.
- Write final plan, research, and repository-overview artifacts in Japanese unless the user explicitly requests another language. This includes files under `docs/agent-reports/plans/`, files under `docs/agent-reports/research/`, and `docs/agent-reports/repository-overview.md`.
- Use English for repository-facing and agent-facing text that is not a final artifact, including code comments, docstrings, test names, commit messages, agent instructions, skill instructions, subagent prompts and responses, investigation notes, TODO lists, checklists, and handoff notes.
- Use English for all main-agent/subagent communication, including delegated prompts, intermediate reports, review notes, and handoff material.
- Follow the existing language style of user-facing documentation.
- Keep agent-facing notes concise and avoid repeating instructions already defined in this file or in language-specific instruction files.
- Prefer English for private reasoning where possible. Do not expose private chain-of-thought. When explaining decisions, provide a concise Japanese summary of the rationale, evidence, changes made, and validation results.
