---
name: targeted-repository-research
description: Use this skill when asked to investigate a specific topic, feature, behavior, symbol, setting, error, test, dependency, or impact area inside a repository. This skill is for narrow and deep repository investigation, not broad repository overview.
---

# Targeted Repository Research Skill

## Purpose

Investigate a user-specified topic inside the repository and produce a grounded answer that explains:

- Where the relevant implementation lives
- How the relevant code, configuration, or behavior works
- What files, symbols, tests, or commands are involved
- What evidence supports the conclusion
- What remains uncertain
- What follow-up actions are recommended

This skill is optimized for narrow, user-directed investigation.

For broad repository onboarding or overall repository mapping, use the `repository-overview` workflow instead.

## Default Behavior

Start with read-only investigation.

Do not modify source code, configuration files, tests, or documentation unless the user explicitly asks for edits.

Do not install dependencies, start services, run migrations, or run expensive commands unless explicitly allowed or clearly safe for the repository context.

When available, read `docs/agent-reports/repository-overview.md` first to understand the repository structure and avoid unnecessary exploration.

By default, answer in the conversation without creating files.

When the user asks for persistent output, or when the investigation result will be useful for future coding agents, create or update a targeted research report under:

- `docs/agent-reports/targeted-research/<topic-slug>.md`

Use a short, lowercase, kebab-case topic slug.

Examples:

- `docs/agent-reports/targeted-research/dataset-loading-flow.md`
- `docs/agent-reports/targeted-research/model-checkpoint-loading.md`
- `docs/agent-reports/targeted-research/precommit-ruff-behavior.md`

If a report for the same topic already exists, read it first, verify whether it is still accurate, and update it in place instead of creating a dated copy.

Use Git history to track previous versions when needed.

## Investigation Principles

Follow these principles:

- Focus on the user-specified topic.
- Avoid turning a targeted investigation into a full repository overview.
- Prefer concrete evidence over assumptions.
- Cite file paths, config keys, commands, and symbols when summarizing.
- Distinguish confirmed facts from inferred hypotheses.
- Trace only as far as needed to answer the user’s question.
- Prefer precise search terms over broad file dumps.
- Identify unknowns instead of guessing.
- Keep the final output actionable for future implementation, debugging, testing, or review.

## Research Question Framing

Before deep investigation, identify the investigation type.

Common types:

- Implementation location: "Where is this feature implemented?"
- Symbol trace: "Where is this function/class/setting defined and used?"
- Behavior flow: "How does this behavior work?"
- Impact scope: "What changes if this code/config/spec changes?"
- Bug context: "What code could explain this error or unexpected behavior?"
- Test target: "Which tests cover this behavior?"
- Config/dependency: "Where is this setting/dependency/tool configured?"

If the user’s request includes multiple topics, split them into separate research questions and investigate each one independently.

Do not ask for clarification when a reasonable interpretation exists. State the assumption and proceed.

## High-Level Workflow

### 1. Understand the Request

Extract:

- Target topic
- Relevant names, symbols, files, commands, errors, or behavior
- Expected answer type
- Constraints from the user
- Whether persistent output is needed

### 2. Establish Repository Context

Check `docs/agent-reports/repository-overview.md` if it exists.

Use it to identify likely source directories, tests, configs, and commands.

Do not rely on the overview report blindly. Verify findings against current files.

### 3. Search for Relevant Evidence

Use targeted searches based on:

- Exact symbol names
- Error messages
- Config keys
- CLI commands
- Function/class names
- File names
- Test names
- Documentation references
- Domain terms from the user request

Prefer commands such as:

```bash
rg "<exact-term>"
rg "<symbol-name>"
rg "<config-key>"
git ls-files | rg "<path-or-topic>"
```

Use repository-appropriate commands. Avoid noisy full-tree dumps.

### 4. Trace the Relevant Context

Depending on the request, trace:

* Definition and usage
* Import/export chain
* Call path
* Runtime entrypoint
* Configuration loading
* Data flow
* Test coverage
* CI or command execution
* Documentation references
* Side effects and external interfaces

Trace only the amount needed to answer the question.

### 5. Delegate Focused Research

When subagents are available, delegate by investigation type:

* `implementation-location-researcher`: locate where a feature or behavior is implemented
* `symbol-trace-researcher`: trace definitions, references, imports, exports, and call sites
* `behavior-flow-researcher`: explain runtime behavior and execution flow
* `impact-scope-researcher`: identify affected files, tests, APIs, and risks for a potential change
* `bug-context-researcher`: investigate errors, failures, suspicious behavior, and likely root causes
* `quality-and-test-researcher`: identify relevant tests, validation commands, and quality signals
* `project-config-researcher`: investigate configuration, dependencies, tool settings, and environment behavior

The parent agent must synthesize all subagent findings into one coherent answer.

Subagents should not make final broad conclusions outside their assigned scope.

### 6. Synthesize the Answer

Produce a concise answer with:

* Direct conclusion
* Relevant files and symbols
* Explanation of behavior or relationships
* Evidence
* Unknowns and assumptions
* Suggested next actions

For implementation or debugging tasks, include concrete next steps such as:

* Files to edit
* Tests to run
* Additional checks to perform
* Risks to watch

## Output Style

Use concise but useful Markdown.

Start with the answer, not the investigation log.

Every important claim should be grounded by at least one of:

* File path
* Config key
* Command result
* Symbol name
* Error message
* Explicit uncertainty note

Use labels:

* `Confirmed:` for facts grounded in files
* `Inferred:` for reasonable conclusions
* `Unknown:` for unresolved items

## Completion Criteria

The investigation is complete when the final output explains:

* What was investigated
* What the conclusion is
* Which files, symbols, configs, tests, or commands are involved
* Why the conclusion is supported
* What remains uncertain
* What should be done next

If creating a persistent report, use the report template in `report-template.md`.
