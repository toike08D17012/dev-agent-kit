# AGENTS.md

## 1. Project Overview

This repository is a Python project. Before making changes, understand the existing implementation, tests, and configuration files.

Follow the existing architecture and coding patterns. Prefer small, focused changes over broad rewrites.

## 2. Source of Truth

The following files are the source of truth for project configuration:

* `pyproject.toml` for Python version, dependencies, Ruff, Mypy, Pytest, and packaging settings
* Existing source files for architecture and implementation patterns
* Existing tests for expected behavior
* README or documentation files for user-facing behavior

If this document conflicts with tool configuration, prefer the tool configuration and report the inconsistency.

## 3. Coding Style

This project follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

### Exceptions

* Line length: up to 120 characters

### General Rules

* Write readable and Pythonic code.
* Use type annotations where practical.
* Use built-in generic types such as `list`, `tuple`, and `dict` when supported by the target Python version defined in `pyproject.toml`.
* Write docstrings in Google style.
* Write comments and docstrings in English.
* Keep public APIs backward compatible unless a breaking change is explicitly requested.
* Avoid unnecessary refactoring, file moves, or formatting-only changes.

## 4. Tools

This project uses:

* Ruff for linting and formatting
* Mypy for static type checking
* Pytest for testing

Do not change lint, type-check, or test settings just to make failures disappear.

## 5. Dependency Management

* Do not add new dependencies unless necessary.
* Prefer the standard library or existing dependencies when practical.
* Do not use `pip install` to add dependencies.
* Use the repository-defined dependency management workflow, such as `uv add`, when adding dependencies.
* When adding a dependency, update the appropriate project configuration and consider license compatibility.

## 6. Development Flow

Use a plan-first workflow for repository changes.

By default, for any task that may modify repository files, the agent should create a plan file before implementation, regardless of task size.

The agent may skip the plan file and implement directly only when the user explicitly instructs it to do so, such as by saying "implement directly", "skip the plan", or "make the change now".

Unless the user gives such an explicit instruction, do not implement changes in the same turn as plan creation.

Before editing:

* Inspect the relevant source files, tests, and configuration.
* Check whether a similar implementation already exists.
* Understand the current behavior before proposing changes.

### Plan Artifact Workflow

For any task that may modify source code, tests, configuration, scripts, CI, documentation, or repository structure, create a plan file before implementation.

Plan files must be created under:

```text
.agents/plans/YYYY-MM-DD-HHMM-<task-slug>.md
```

Examples:

```text
.agents/plans/2026-06-07-0130-add-integrated-gradients-tests.md
.agents/plans/2026-06-07-0145-refactor-docker-entrypoint.md
```

During the planning phase:

* Do not modify production source code, tests, configuration, scripts, CI, or documentation.
* Only create or update the plan file.
* Keep the plan specific enough that the user can review and edit it before implementation.
* Stop after writing the plan file.
* Report the plan file path to the user.
* Do not proceed to implementation until the user explicitly approves the plan or asks to implement it.

A plan file must include:

```markdown
# Plan: <task title>

## Goal

Describe the goal of the change.

## Current Understanding

Summarize the relevant current implementation, configuration, tests, and constraints.

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

* Read the approved plan file before editing.
* Follow the approved plan unless repository investigation reveals a better approach.
* If the implementation meaningfully diverges from the plan, update the plan file with an `Implementation Notes` section.
* Keep the actual changes minimal and focused.
* Do not make unrelated changes.

After editing, run the relevant checks when possible:

```bash
# This script runs `ruff check`, `ruff format`, `mypy`, and `pytest`.
./scripts/pre-commit/checks.sh
```

If these commands cannot be run, explain why and state which commands should be run by the developer.

## 7. Testing Policy

* Add or update tests when changing behavior.
* Prefer focused unit tests for small logic changes.
* Do not delete, skip, or weaken tests just to make the test suite pass.
* Keep test names descriptive.
* Follow the existing test structure and fixture style.

## 8. Security and Secrets

* Do not hard-code API keys, passwords, tokens, private keys, or credentials.
* Do not include secrets in logs, exceptions, comments, tests, or documentation.
* Do not commit generated credentials or local environment files.
* Use environment variables or existing configuration mechanisms for sensitive values.

## 9. Coding Agent Workflow

When using a coding agent:

* Follow this guide strictly.
* Use the Plan Artifact Workflow before implementing repository changes, unless the user explicitly asks to skip planning or implement directly.
* Read the relevant files before generating or editing code.
* Preserve existing design, naming, and public APIs.
* Avoid unrelated changes.
* Keep diffs minimal and focused.
* Use existing utilities, abstractions, and patterns where possible.
* Add tests for changed behavior.
* Use the Plan Artifact Workflow before implementing repository changes.
* Do not skip the plan file for convenience when the task modifies repository files.
* Run relevant checks when possible.
* In the final response, summarize:

  * what was changed
  * which files were changed
  * which checks were run
  * which checks could not be run, if any
  * whether the implementation followed the approved plan or diverged from it

## 10. Skills and Subagents

When repository-provided skills, subagents, or agent workflows are available, use them for tasks that require repeated procedures or structured investigation.

Use skills or subagents for:

* repository structure investigation
* architecture review
* test strategy review
* documentation generation
* large refactoring planning
* migration planning
* codebase-wide impact analysis

General rules:

* Prefer existing skills over ad-hoc workflows when a matching skill exists.
* Keep each subagent task narrow and evidence-based.
* Ask subagents to report findings with relevant file paths.
* Consolidate subagent findings before editing code.
* Do not use skills or subagents to bypass tests, reviews, or project conventions.
* Do not create new skills or subagents unless explicitly requested.
* When a skill or subagent investigation informs implementation, summarize the findings in the plan file before editing.

If a task produces reusable investigation results, save them as markdown only when the user or project workflow asks for persistent output.

## 11. Comments and Docstrings

* Comments and docstrings must be written in English.
* Avoid redundant comments.
* Explain intent, assumptions, constraints, and non-obvious behavior.
* Do not write comments that merely restate the code.

## 12. Language Policy

* Write code comments, docstrings, test names, commit messages, and agent-facing notes in English.
* Write final user-facing explanations in Japanese unless otherwise requested.
* Do not mix Japanese and English in code comments unless necessary.

## 13. Checklist

Before implementing a change, confirm:

* [ ] The relevant existing implementation was inspected.
* [ ] A plan file was created under `.agents/plans/`.
* [ ] The plan includes goal, current understanding, files likely to change, proposed steps, validation plan, risks, and acceptance criteria.
* [ ] The user approved the plan or explicitly asked to implement it.

Before finishing a change, confirm:

* [ ] The approved plan file was read before editing.
* [ ] The change is minimal and focused.
* [ ] Public APIs remain compatible, unless a breaking change was requested.
* [ ] Code follows the Google Python Style Guide.
* [ ] Lines are within 120 characters where practical.
* [ ] Type annotations are used where practical.
* [ ] Comments and docstrings are written in English.
* [ ] Tests were added or updated for behavior changes.
* [ ] Ruff, Mypy, and Pytest were run when possible.
* [ ] Any skipped checks are explained.
* [ ] Any meaningful divergence from the plan was documented in the plan file.
