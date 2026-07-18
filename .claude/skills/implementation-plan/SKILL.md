---
name: implementation-plan
description: Use this skill when the user wants to create an implementation plan for a repository change. This skill assumes that prerequisite investigation results may already exist in files, but it can delegate targeted read-only investigation, strategy design, and quality review to configured custom agents/subagents before producing a concrete implementation plan.
---

# Implementation Plan Skill

## Purpose

Create a grounded implementation plan that another coding agent or developer can execute without repeating the full investigation.

The plan must identify:

* the confirmed change and behavior to preserve
* the files and responsibilities involved
* the smallest sufficient design and ordered implementation steps
* validation matched to the changed areas and risks
* assumptions, open questions, risks, and done criteria

This skill plans the change; it does not implement it. After writing the plan, stop and wait for user approval before implementation.

## Language Policy

Write the final implementation plan in Japanese unless the user explicitly requests another language. Keep code identifiers, paths, commands, symbols, configuration keys, and quoted source text unchanged.

Use English for all main-agent/subagent communication, delegated reports, review notes, and handoff material. Synthesize English delegated results into the Japanese final artifact. Do not expose private chain-of-thought.

## Allowed Scope

Start with read-only investigation. Do not modify source code, configuration, tests, documentation, generated artifacts, or lock files while using this skill.

The only allowed write is creating or explicitly updating an implementation plan under:

```text
docs/agent-reports/plans/
```

Do not run formatters or tests unless a read-only command is necessary for investigation and proportionate to the planning question.

## Planning Principles

### Ground the Plan

* Prefer relevant existing research, investigation reports, and design notes over repeating repository exploration.
* Verify important facts against current repository files.
* Cite files, symbols, configuration, tests, or commands for material claims.
* Separate confirmed facts, assumptions, and open questions. Do not invent missing details.
* Ask the user only when a blocking choice cannot be resolved safely from repository evidence.

### Use the Smallest Sufficient Design

* Plan only what confirmed requirements require.
* Do not add abstractions, extension points, configuration, compatibility layers, or files for hypothetical future needs.
* Prefer existing modules, utilities, and direct control flow.
* Propose a new abstraction only for a distinct responsibility or concrete repeated behavior.
* Split files by cohesive responsibility when extraction improves understanding and reviewability. Do not use numeric size thresholds.
* Preserve required boundary validation, invariants, error handling, security, and compatibility. Simplicity is not a reason to remove necessary safeguards.
* Keep changed files and public surface area as small as practical.

### Make Validation Proportional

For each validation step, record the changed area or risk, the command or check, and why it is sufficient.

Start with the smallest check that directly exercises the change. Expand validation when the plan affects shared APIs, multiple modules, project configuration, build or distribution behavior, security-sensitive code, data migrations, or another identified high-risk boundary.

Do not include repository-wide checks, manual verification, or a separate test phase by default. Include them only when the change or risk justifies them. Do not plan repeated execution of an identical successful check unless relevant files or configuration change afterward.

## Mandatory Delegation Contract

Use the current tool's native separate-agent mechanism when available. Invoke the configured roles by their exact names; do not role-play them in the main context.

Delegate as follows:

* `implementation-plan-context-researcher`: required when planning needs inspection of more than two repository files. It performs focused read-only research, prioritizes existing reports, and returns evidence, relevant validation, constraints, and gaps.
* `implementation-plan-strategy-designer`: required unless the change is clearly small, local, and obvious. It proposes the smallest sufficient design, ordered steps, file responsibilities, proportional validation, and meaningful risks.
* `implementation-plan-quality-reviewer`: required when the plan touches multiple files, public APIs, tests, CI, build, packaging, deployment, or has meaningful risk. It reviews the draft for grounding, unnecessary complexity, validation fit, and missing contracts.

The role definitions in `agent-source/agents/` are the source assets and are distributed to host-specific agent locations. Use the role available in the current environment rather than assuming a host-specific path.

The main agent must:

1. delegate before performing investigation or design that belongs to a required role
2. wait for all required delegated results
3. review and reconcile the results
4. synthesize them into one coherent plan instead of pasting them verbatim

### Main-Agent Limits Before Delegation

Before required delegation, the main agent may only:

* identify the requested change and likely investigation type
* list likely report directories or search report names
* identify candidate source material paths
* read the external plan template
* check the output directory
* inspect a small number of top-level files needed to route the task

Do not trace behavior, inspect many files, design the implementation, or review the draft before assigning the matching role.

### Delegation Fallback

If no usable separate-agent mechanism is available, perform the smallest necessary direct read-only investigation. Record the fallback and its reason in the plan's delegation log; do not claim delegation occurred.

Every plan must include this log:

| 役割 | 委任 | 結果を使用 | メモ |
| --- | --- | --- | --- |
| `implementation-plan-context-researcher` | はい / いいえ | はい / いいえ | ... |
| `implementation-plan-strategy-designer` | はい / いいえ | はい / いいえ | ... |
| `implementation-plan-quality-reviewer` | はい / いいえ | はい / いいえ | ... |

If a role was unnecessary for a small, local, low-risk change, say so. If delegation support was unavailable, identify the fallback explicitly.

## Workflow

### 1. Understand the Request

Identify the behavior to change, behavior to preserve, likely change type, user constraints, and whether any choice is blocking. Use a reasonable documented assumption when it does not materially change scope or risk.

### 2. Locate Existing Source Material

Look for relevant reports before new investigation, especially under:

```text
docs/agent-reports/investigations/
docs/agent-reports/research/
docs/agent-reports/
docs/
reports/
notes/
.agents/
agents/
```

Prefer the most directly relevant current report, not merely the newest file. Pass candidate paths and focused missing-information questions to the context researcher when delegation is required.

### 3. Gather Only Missing Context

Establish only facts that affect the plan, such as:

* entry points, relevant symbols, and current behavior
* existing architecture and ownership boundaries
* public API, configuration, schema, compatibility, or deployment impact
* related tests and the smallest relevant validation commands
* conditions that require broader validation
* risks, constraints, and unresolved information

If delegated research leaves a focused gap, send a focused follow-up. Otherwise document a non-blocking unknown or ask the user about a genuinely blocking choice.

### 4. Design the Strategy

Provide the strategy designer with the request, confirmed context, constraints, assumptions, and open questions when delegation is required.

Evaluate its result against the planning principles. Remove speculative layers, unjustified new files, fixed phases, and validation that does not map to an identified change or risk.

### 5. Draft from the External Template

Resolve `templates/implementation-plan.md` relative to this `SKILL.md`. This works both in the source tree and in distributed skill locations.

Use the external template as the source of truth. Keep the plan concise and omit optional sections that do not clarify a real decision. Do not force fixed phases, manual verification, detailed rollback steps, or full-suite checks onto a small change.

If the template is unavailable, include at least:

* summary and user request
* source material and delegation log
* confirmed current state
* requirements, assumptions, and open questions
* proposed approach and complexity guard
* ordered implementation steps and file-level changes
* proportional validation plan
* risks, rollback guidance, and done criteria

Write steps in dependency order. Tie each step to concrete files, responsibilities, behavior, and tests when applicable. The plan must be executable without dictating unnecessary implementation detail.

### 6. Review the Draft

Use `implementation-plan-quality-reviewer` when required. Give it the original request, confirmed context, strategy result, constraints, and draft.

Apply required fixes. Apply optional suggestions only when they improve correctness or clarity without adding unsupported scope or boilerplate.

### 7. Write the Plan File

Create the plan under `docs/agent-reports/plans/` with:

```text
YYYY-MM-DD-<short-topic>-implementation-plan.md
```

Use the current local date and a short lowercase kebab-case topic. Do not overwrite an existing plan unless the user explicitly asks to update it. If a similar plan exists without update permission, choose a more specific filename.

The final file must be Japanese unless the user requested another language. Ensure it contains the completed delegation log and clearly marks blocking questions.

### 8. Stop for Approval

Do not implement the planned repository change in the same workflow. Report the plan and wait for explicit user approval before implementation.

## Handling Insufficient Information

If information remains insufficient after focused investigation:

* do not invent details
* document non-blocking unknowns and the assumption used
* mark blocking questions clearly
* provide the safest useful partial plan when possible
* recommend the narrowest next investigation when planning cannot proceed

## Completion Check

Before finishing, confirm that the plan:

* is grounded in current repository evidence and uses existing reports when relevant
* records required delegation, skipped roles, or fallback accurately
* is written in Japanese unless the user requested another language
* proposes the simplest design that satisfies confirmed requirements
* identifies concrete files and cohesive responsibilities
* avoids speculative abstractions, fixed phases, and unrelated work
* maps validation to changed areas and risks, with justified expansion only
* separates facts, assumptions, and open questions
* covers compatibility, necessary safeguards, risks, rollback, and done criteria in proportion to the change
* does not implement the change

## Final Response

After creating the plan, respond in Japanese unless the user requested another language. Include only:

* the created plan path
* a short summary of the approach
* blocking open questions, if any
* the recommendation to review and approve the plan before implementation

Do not paste the entire plan unless the user asks.
