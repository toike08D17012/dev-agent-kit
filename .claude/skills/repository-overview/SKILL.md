---
name: repository-overview
description: Use this skill when asked to understand, summarize, map, onboard, audit, or document the overall structure of a repository. This skill is for broad repository-level investigation, not for deep investigation of one specific feature or bug.
---

# Repository Overview Skill

## Purpose

Create a concise, grounded overview of the entire repository so future coding agents and developers can quickly understand:

- What this repository is for
- How the repository is structured
- Where the main implementation lives
- How to set up, run, test, lint, and build the project
- What the main runtime flow is
- What risks, gaps, or unclear areas exist

This skill is optimized for broad repository understanding.  
For narrow investigations such as "where is this function used?" or "what is the impact of changing this setting?", use a targeted repository research workflow instead.

## Default Behavior

Start with read-only investigation.

Do not modify source code, configuration files, tests, or documentation unless the user explicitly asks for edits.

Do not install dependencies, start services, or run expensive commands unless explicitly allowed or clearly safe for the repository context.

The only allowed write during this skill is creating or updating the repository overview report at:

* `docs/agent-reports/repository-overview.md`

This report is the canonical, latest overview of the repository.

If `docs/agent-reports/repository-overview.md` already exists, read it first, verify whether its contents are still accurate, and update stale or missing sections.

When the repository structure, tooling, architecture, or validation workflow changes, update this file in place instead of creating dated copies.

Use Git history to track previous versions when needed.

## Investigation Principles

Follow these principles:

* Prefer concrete evidence over assumptions.
* Cite file paths, config keys, commands, and symbols when summarizing.
* Distinguish confirmed facts from inferred hypotheses.
* Do not read every file exhaustively unless necessary.
* Prioritize source-of-truth files such as README, project config, CI config, package metadata, scripts, and main source directories.
* Identify unknowns instead of guessing.
* Keep the final output useful for future implementation work.

## High-Level Workflow

### 1. Repository Inventory

Identify:

* Top-level files
* Main source directories
* Test directories
* Documentation directories
* Scripts
* CI/CD configuration
* Docker or devcontainer configuration
* Package or build configuration
* Example or demo directories

Prefer commands such as:

```bash
git ls-files
find . -maxdepth 2 -type f
find . -maxdepth 2 -type d
```

Use repository-appropriate commands. Avoid noisy full-tree dumps.

### 2. Project Type and Tooling

Determine:

* Main language or languages
* Dependency manager
* Build system
* Runtime or framework
* Lint command
* Format command
* Type-check command
* Test command
* Packaging or release method

Check files such as:

* `pyproject.toml`
* `package.json`
* `Cargo.toml`
* `go.mod`
* `CMakeLists.txt`
* `Makefile`
* `Taskfile.yml`
* `justfile`
* `.pre-commit-config.yaml`
* `.github/workflows/*`
* `Dockerfile`
* `docker-compose.yml`
* `.devcontainer/*`

### 3. Architecture and Runtime Flow

Identify:

* Main entrypoints
* Main packages or modules
* Core abstractions
* Data flow
* Control flow
* External interfaces
* Configuration loading
* Public API surface, if applicable

Do not deeply trace every function. Focus on the overall shape.

### 4. Testing and Quality

Identify:

* Test framework
* Test directory structure
* Common test utilities
* Fixture patterns
* CI test commands
* Local validation commands
* Missing or weak test areas, if visible from repository structure

### 5. Documentation Consistency

Compare documentation with configuration and source layout.

Check whether:

* Setup instructions match actual files
* Commands in README are still plausible
* Documented paths exist
* Public API examples match exported code
* Development commands are documented

### 6. Synthesis

Produce a final overview that includes:

* Executive summary
* Repository purpose
* Tech stack
* Repository layout
* Main runtime flow
* Important commands
* Testing strategy
* Documentation notes
* Risks and unknowns
* Recommended next actions
* Evidence list

## Subagent Delegation

When subagents are available, delegate as follows:

### `repo-structure-researcher`

Use for:

* Repository map
* Directory roles
* Important top-level files
* Main implementation areas

### `project-config-researcher`

Use for:

* Dependency management
* Build/test/lint/format commands
* Docker/devcontainer
* CI/CD
* Tooling source of truth

### `runtime-architecture-researcher`

Use for:

* Entrypoints
* Main execution flow
* Core modules
* Public APIs
* Data/control flow

### `quality-and-test-researcher`

Use for:

* Test layout
* Test commands
* CI validation
* Coverage gaps visible from structure
* Quality tooling

### `documentation-consistency-researcher`

Use for:

* README and docs consistency
* Setup instruction accuracy
* Missing documentation
* Stale references

The parent agent must synthesize all subagent findings into one coherent report.
Subagents should not make broad final conclusions outside their assigned scope.

## Output Style

Use concise but useful Markdown.

Every important claim should be grounded by at least one of:

* File path
* Config key
* Command result
* Symbol name
* Explicit uncertainty note

Use labels:

* `Confirmed:` for facts grounded in files
* `Inferred:` for reasonable conclusions
* `Unknown:` for unresolved items

## Completion Criteria

The investigation is complete when the final output explains:

* What the repository does
* Where the important code is
* How to run or validate the project
* What the main architecture looks like
* What future coding agents should inspect first
* What remains unclear

If `docs/agent-reports/repository-overview.md` already exists, update it in place and remove stale information rather than appending a new dated report.
