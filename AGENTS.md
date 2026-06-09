# AGENTS.md

## 1. Project Overview

This repository is primarily a Python project, with Markdown documentation and shell scripts.

Before making changes, understand the existing implementation, tests, scripts, documentation, and configuration files.

Follow the existing architecture and coding patterns. Prefer small, focused changes over broad rewrites.

## 2. Source of Truth

The following files are the source of truth for project configuration and behavior:

- `pyproject.toml` for Python version, dependencies, Ruff, Mypy, Pytest, and packaging settings
- Existing source files for architecture and implementation patterns
- Existing tests for expected behavior
- Existing shell scripts for operational workflows
- README and documentation files for user-facing behavior
- CI and pre-commit configuration for validation rules

If this document conflicts with tool configuration, prefer the tool configuration and report the inconsistency.

## 3. Language-Specific Instructions

Language-specific instructions are stored under `.agents/instructions`.

Before editing matching files, read and follow the relevant instruction file:

| File type | Instruction file |
| --- | --- |
| Python files (`*.py`, `pyproject.toml`, test files) | `.agents/instructions/python.md` |
| Markdown files (`*.md`) | `.agents/instructions/markdown.md` |
| Shell scripts (`*.sh`, `*.bash`, scripts with Bash shebangs) | `.agents/instructions/shell.md` |

General rules:

- Apply language-specific instructions only when they are relevant to the files being changed.
- Do not import all language-specific instruction files into this file.
- Do not edit instruction files unless explicitly requested.
- If language-specific instructions conflict with tool configuration, prefer the tool configuration and report the inconsistency.

## 4. General Development Principles

- Inspect relevant files before editing.
- Check whether similar code, documentation, or scripts already exist.
- Understand the current behavior before proposing changes.
- Preserve existing design, naming, and public APIs unless a breaking change is explicitly requested.
- Keep diffs minimal and focused.
- Avoid unrelated refactoring, file moves, or formatting-only changes.
- Do not weaken lint, type-check, test, or CI settings just to make checks pass.
- Do not delete, skip, or weaken tests to hide failures.
- Prefer existing utilities, abstractions, and project patterns.

## 5. Dependency and Tooling Policy

- Do not add new dependencies unless necessary.
- Prefer the standard library or existing dependencies when practical.
- Use the repository-defined dependency management workflow.
- When adding or updating dependencies, update the appropriate project configuration.
- Consider license compatibility when adding dependencies.
- Do not introduce new tools, formatters, linters, frameworks, or package managers without explicit justification.

## 6. Plan-First Development Flow

Use a plan-first workflow for repository changes.

By default, for any task that may modify repository files, create a plan file before implementation, regardless of task size.

The agent may skip the plan file and implement directly only when the user explicitly instructs it to do so, such as by saying:

- "implement directly"
- "skip the plan"
- "make the change now"
- "apply the change now"

Unless the user gives such an explicit instruction, do not implement changes in the same turn as plan creation.

### Plan Artifact Workflow

For any task that may modify source code, tests, configuration, scripts, CI, documentation, instructions, skills, or repository structure, create a plan file before implementation.

Plan files must be created under:

```text
.agents/plans/YYYY-MM-DD-HHMM-<task-slug>.md
```

Use the local timezone of the development environment for the timestamp.

Examples:

```text
.agents/plans/2026-06-07-0130-add-integrated-gradients-tests.md
.agents/plans/2026-06-07-0145-refactor-docker-entrypoint.md
```

During the planning phase:

- Do not modify production source code, tests, configuration, scripts, CI, documentation, or repository structure.
- Only create or update the plan file.
- Keep the plan specific enough that the user can review and edit it before implementation.
- Stop after writing the plan file.
- Report the plan file path to the user.
- Do not proceed to implementation until the user explicitly approves the plan or asks to implement it.

A plan file must include:

```markdown
# Plan: <task title>

## Goal

Describe the goal of the change.

## Current Understanding

Summarize the relevant current implementation, configuration, tests, scripts, documentation, and constraints.

## Files Likely to Change

List the files that are expected to be changed.

## Proposed Steps

Describe the implementation steps in order.

## Validation Plan

List the commands that should be run after implementation.

## Risks and Considerations

Describe risks, assumptions, compatibility concerns, and possible edge cases.

## Acceptance Criteria

List the conditions that must be true for the task to be considered complete.
```

During implementation:

- Read the approved plan file before editing.
- Follow the approved plan unless repository investigation reveals a better approach.
- If the implementation meaningfully diverges from the plan, update the plan file with an `Implementation Notes` section.
- Keep the actual changes minimal and focused.
- Do not make unrelated changes.

## 7. Validation

After editing, run the relevant checks when possible.

Default validation command:

```bash
# This script runs repository-defined formatting, linting, type checking, and tests.
./scripts/pre-commit/checks.sh
```

If this command cannot be run, explain why and state which commands should be run by the developer.

When only a subset of files changed, it is acceptable to run narrower checks first, but the final response must clearly state which checks were run.

## 8. Security and Secrets

- Do not hard-code API keys, passwords, tokens, private keys, credentials, or other secrets.
- Do not include secrets in logs, exceptions, comments, tests, documentation, examples, or plan files.
- Do not commit generated credentials, local environment files, or machine-specific configuration.
- Use environment variables or existing configuration mechanisms for sensitive values.
- Be careful when printing command output, environment variables, or configuration values.

## 9. Skills and Subagents

Repository-provided skills are stored under `.agents/skills`.

When a task matches an available skill, prefer using that skill instead of inventing a new workflow.

Use skills or subagents for:

- repository structure investigation
- architecture review
- test strategy review
- documentation generation
- large refactoring planning
- migration planning
- codebase-wide impact analysis

General rules:

- Prefer existing skills over ad-hoc workflows when a matching skill exists.
- Keep each subagent task narrow and evidence-based.
- Ask subagents to report findings with relevant file paths.
- Consolidate subagent findings before editing code.
- Do not use skills or subagents to bypass tests, reviews, or project conventions.
- Do not create, modify, or delete skills or subagents unless explicitly requested.
- When a skill or subagent investigation informs implementation, summarize the findings in the plan file before editing.

If a task produces reusable investigation results, save them as Markdown only when the user or project workflow asks for persistent output.

## 10. Language Policy

- Write code comments, docstrings, test names, commit messages, and agent-facing notes in English.
- Write final user-facing explanations in Japanese unless otherwise requested.
- Do not mix Japanese and English in code comments unless necessary.
- Follow the existing language style of user-facing documentation.

## 11. Final Response Requirements

In the final response, summarize:

- what was changed
- which files were changed
- which checks were run
- which checks could not be run, if any
- whether the implementation followed the approved plan or diverged from it

If no implementation was performed and only a plan was created, report only the plan file path and a brief summary.

## 12. Checklist

Before implementing a change, confirm:

- [ ] The relevant existing implementation was inspected.
- [ ] The relevant language-specific instruction file was read.
- [ ] A plan file was created under `.agents/plans/`.
- [ ] The plan includes goal, current understanding, files likely to change, proposed steps, validation plan, risks, and acceptance criteria.
- [ ] The user approved the plan or explicitly asked to implement it.

Before finishing a change, confirm:

- [ ] The approved plan file was read before editing.
- [ ] The change is minimal and focused.
- [ ] Public APIs remain compatible, unless a breaking change was requested.
- [ ] Relevant tests were added or updated for behavior changes.
- [ ] Relevant checks were run when possible.
- [ ] Any skipped checks are explained.
- [ ] Any meaningful divergence from the plan was documented in the plan file.
