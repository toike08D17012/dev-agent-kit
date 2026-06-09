---
name: implementation-plan
description: Use this skill when the user wants to create an implementation plan for a repository change. This skill assumes that prerequisite investigation results may already exist in files, but it can delegate targeted read-only investigation and strategy review to subagents before producing a concrete implementation plan.
---

# Implementation Plan Skill

## Purpose

Create a concrete, grounded implementation plan for a requested repository change.

This skill bridges the gap between:

1. existing investigation reports, design notes, or repository research files
2. additional missing information discovered through targeted read-only investigation
3. a practical implementation plan that future coding agents or developers can follow

The output must make it clear:

- what should be changed
- where it should be changed
- in what order the work should be done
- how the change should be tested
- what risks, assumptions, and open questions remain

This skill does not implement the change by default.

## Main Agent Role

The main agent is responsible for orchestration and final synthesis.

The main agent should focus on:

- understanding the user's requested change
- locating likely source investigation reports
- deciding what information is missing
- delegating heavy investigation to subagents
- delegating implementation strategy design to subagents
- reviewing subagent outputs
- creating the final implementation plan file
- reporting the created plan path to the user

The main agent should avoid doing heavy repository investigation directly when a subagent can perform it.

## Subagents

Use the following subagents when available.

### `implementation-plan-context-researcher`

Use this subagent for targeted read-only investigation.

Delegate to this subagent when you need to inspect:

- existing investigation reports
- relevant source files
- relevant tests
- project configuration
- CI or pre-commit settings
- examples or documentation
- similar implementations in the repository

The expected output is a factual context research report.

### `implementation-plan-strategy-designer`

Use this subagent to convert investigation results into an implementation strategy.

Delegate to this subagent when you need:

- proposed implementation approach
- considered options
- phased implementation steps
- file-level change plan
- validation strategy
- risks and mitigations
- rollback plan
- done criteria

The expected output is a strategy report that the main agent can merge into the final plan.

### `implementation-plan-quality-reviewer`

Use this subagent to review the implementation plan draft.

Delegate to this subagent before finalizing the plan when:

- the change touches multiple files
- the change affects public APIs
- the change affects tests, CI, build, packaging, or deployment
- the plan contains assumptions or open questions
- the implementation has non-trivial risk

For very small local changes, this review is optional.

## When to Use This Skill

Use this skill when the user asks for things like:

- "Create an implementation plan"
- "Plan how to implement this feature"
- "Turn the investigation result into an implementation plan"
- "Based on this research file, create a plan"
- "Before editing, summarize the implementation steps"
- "追加調査して実装計画に落とし込んで"
- "実装前にplanファイルを作って"

This skill is especially useful when a previous investigation skill has already produced a markdown report, but the implementation path is not yet clear.

## When Not to Use This Skill

Do not use this skill for:

- broad repository overview
- root-cause investigation without a requested implementation
- directly editing source code
- debugging and fixing in the same step
- writing user-facing documentation without implementation planning

For broad repository understanding, use a repository overview or investigation skill first.

For direct code changes, use the appropriate implementation or coding workflow after this plan is created.

## Default Behavior

Start with read-only investigation.

Do not modify source code, configuration files, tests, or documentation, except for creating or updating the implementation plan file.

Do not implement the requested change unless the user explicitly asks to implement immediately or explicitly asks to skip planning.

The allowed write operation for this skill is creating or updating an implementation plan file under:

```text
docs/agent-reports/plans/
```

## Inputs

Use the following inputs when available:

* the user's requested change
* paths to previous investigation reports
* existing design notes
* issue descriptions
* relevant source files
* relevant tests
* project configuration files
* existing coding conventions
* existing architecture patterns

If the user does not provide an investigation report path, look for likely reports in:

* `docs/agent-reports/investigations/`
* `docs/agent-reports/research/`
* `docs/agent-reports/`
* `docs/`
* `reports/`
* `notes/`
* `.agents/`
* `agents/`

Prefer recently created or recently modified reports that clearly relate to the requested change.

## Core Principles

### 1. Main Agent Orchestrates, Subagents Investigate

The main agent should not manually inspect many files when subagents are available.

Use subagents to gather context, compare options, and review the draft.

The main agent is accountable for the final plan, but not expected to perform all low-level investigation itself.

### 2. Ground the Plan in Existing Facts

The plan must be based on repository facts, not guesses.

When possible, cite or reference:

* files inspected
* functions/classes/modules involved
* tests found
* configuration files found
* previous investigation reports used
* subagent reports used

### 3. Investigate Only What Is Missing

Assume prior investigation may already contain most of the necessary context.

Do not repeat broad repository investigation unless the existing report is clearly insufficient.

Focus follow-up investigation on gaps that affect implementation planning.

### 4. Prefer Small, Safe, Incremental Changes

The implementation plan should be broken into small, reviewable steps.

Avoid broad rewrites unless clearly justified.

Prefer plans that preserve existing architecture and conventions.

### 5. Make Validation Explicit

Every implementation plan must include concrete validation steps.

Examples:

* unit tests to add or update
* integration tests to run
* lint/type-check commands
* manual verification steps
* expected behavior after implementation

### 6. Separate Facts, Assumptions, and Open Questions

The plan should clearly distinguish:

* confirmed facts from repository investigation
* assumptions made to proceed
* unresolved questions that may need user or maintainer confirmation

When a question is not blocking, proceed with a reasonable assumption and document it.

When a question is blocking, mark it clearly.

## Workflow

### Step 1: Understand the Requested Change

Restate the requested change in practical implementation terms.

Clarify internally:

* what behavior should change
* what new capability should exist
* what existing behavior must be preserved
* whether this is a feature, refactor, bug fix, test improvement, or tooling change

Do not ask the user for clarification unless the request is too ambiguous to produce a useful plan.

When reasonable assumptions are possible, proceed and document them.

### Step 2: Locate Existing Investigation Results

Find likely existing investigation reports or design notes.

Prefer files under:

```text
docs/agent-reports/investigations/
```

Also check:

```text
docs/agent-reports/
docs/
reports/
notes/
.agents/
agents/
```

The main agent may do a lightweight search to locate candidate reports.

If candidate reports are found, pass them to `implementation-plan-context-researcher`.

### Step 3: Delegate Context Research

Use `implementation-plan-context-researcher` for targeted read-only investigation.

Provide the subagent with:

* the user's requested change
* candidate investigation report paths
* any known relevant files
* specific missing information questions
* instruction to avoid modifying files

Ask the subagent to return:

* existing reports used
* files inspected
* confirmed current state
* relevant tests and validation commands
* risks and constraints
* missing or unclear information

The main agent should review the subagent result and decide whether enough information exists to plan.

### Step 4: Identify Remaining Missing Information

Use this checklist:

* Goal and expected behavior are clear
* Relevant entry points are known
* Main files/classes/functions to change are known
* Existing architecture pattern is understood
* Public API impact is understood
* Configuration impact is understood
* Data/model/schema impact is understood, if applicable
* Test locations are known
* Validation commands are known
* Backward compatibility risks are known
* Performance/security risks are considered, if relevant
* Migration or rollout needs are considered, if relevant

If important information is still missing, either:

* send a focused follow-up request to `implementation-plan-context-researcher`
* document the unknown as an open question if it is not worth further investigation
* mark it as blocking if the plan cannot safely proceed without it

### Step 5: Delegate Strategy Design

Use `implementation-plan-strategy-designer` after enough context has been gathered.

Provide the subagent with:

* the user's requested change
* context research result
* relevant constraints
* any assumptions already made
* any open questions

Ask the subagent to return:

* recommended approach
* considered options
* phased implementation steps
* file-level change plan
* validation strategy
* risks and mitigations
* rollback plan
* done criteria

The main agent should not blindly copy the strategy result.

The main agent must synthesize it into the final implementation plan and resolve inconsistencies.

### Step 6: Draft the Implementation Plan

Create a draft using:

```text
agents/skills/implementation-plan/templates/implementation-plan.md
```

If the template does not exist, use the template structure defined in this skill.

Fill every section.

If a section is not applicable, write `Not applicable`.

The plan must include:

* source material used
* confirmed current state
* requirements
* assumptions
* open questions
* proposed approach
* considered options, when useful
* implementation steps
* file-level change plan
* validation plan
* risks and mitigations
* rollback plan
* done criteria

### Step 7: Delegate Quality Review

For medium or large plans, or any plan with meaningful risk, use `implementation-plan-quality-reviewer`.

Provide the subagent with:

* the draft implementation plan
* the original user request
* context research result
* strategy result

Ask the reviewer to identify:

* required fixes
* missing information
* risk gaps
* validation gaps
* unclear implementation steps

Apply required fixes before writing the final plan file.

If suggested improvements are useful but not essential, apply them when they improve clarity without overcomplicating the plan.

### Step 8: Create the Implementation Plan File

Create a markdown file under:

```text
docs/agent-reports/plans/
```

Use the filename format:

```text
YYYY-MM-DD-<short-topic>-implementation-plan.md
```

Examples:

```text
docs/agent-reports/plans/2026-06-10-add-retry-handler-implementation-plan.md
docs/agent-reports/plans/2026-06-10-refactor-dataloader-implementation-plan.md
docs/agent-reports/plans/2026-06-10-update-pre-commit-hooks-implementation-plan.md
```

Filename rules:

* Use the current local date.
* Use lowercase kebab-case for `<short-topic>`.
* Keep the topic short but specific.
* Do not overwrite an existing plan unless the user explicitly asks to update it.
* If a similar plan already exists, either update it with permission or create a new file with a more specific topic name.

Before writing the plan, ensure the output directory exists:

```bash
mkdir -p docs/agent-reports/plans
```

The implementation plan is the primary output of this skill.

Do not implement the change unless the user explicitly asks to proceed with implementation.

### Step 9: Final Response to the User

After creating the plan file, respond with only:

* the created plan file path
* a short summary of the proposed approach
* blocking open questions, if any
* recommended next step

Do not paste the entire plan unless the user asks for it.

## Implementation Plan Template

Use the external template when available:

```text
agents/skills/implementation-plan/templates/implementation-plan.md
```

If the template file does not exist, use this structure:

````markdown
# Implementation Plan: <Title>

## 1. Summary

<Briefly describe what will be implemented and why.>

## 2. User Request

<Restate the user's request in implementation-oriented terms.>

## 3. Source Material

<Reference investigation reports, design notes, issues, source files, tests, subagent reports, and configuration files used to create this plan.>

## 4. Confirmed Current State

<List repository facts confirmed by investigation.>

## 5. Requirements

### Functional Requirements

- [ ] ...

### Non-Functional Requirements

- [ ] ...

### Compatibility Requirements

- [ ] ...

## 6. Assumptions

- ...

## 7. Open Questions

### Blocking

- None

### Non-Blocking

- None

## 8. Proposed Approach

<Describe the selected implementation approach.>

## 9. Considered Options

### Option A: <Name>

Pros:

- ...

Cons:

- ...

Decision:

- Selected / Rejected because ...

## 10. Implementation Steps

### Phase 1: Preparation

- [ ] ...

### Phase 2: Core Implementation

- [ ] ...

### Phase 3: Tests

- [ ] ...

### Phase 4: Documentation and Cleanup

- [ ] ...

## 11. File-Level Change Plan

| File | Planned Change |
| --- | --- |
| `path/to/file` | ... |

## 12. Validation Plan

### Automated Checks

```bash
<commands>
````

Expected result:

* ...

### Manual Verification

* ...

## 13. Risks and Mitigations

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| ...  | ...    | ...        |

## 14. Rollback Plan

<Describe how to revert or disable the change if needed.>

## 15. Done Criteria

The implementation is complete when:

* [ ] Required behavior is implemented.
* [ ] Relevant tests are added or updated.
* [ ] Existing tests pass.
* [ ] Lint and formatting checks pass.
* [ ] Type checks pass, if applicable.
* [ ] Documentation is updated, if applicable.
* [ ] No unrelated changes are included.

````

## Plan Creation Rules

When creating an implementation plan:

1. Read or locate existing investigation reports first.
2. Delegate targeted read-only investigation to `implementation-plan-context-researcher` when available.
3. Delegate implementation strategy design to `implementation-plan-strategy-designer` when available.
4. Delegate quality review to `implementation-plan-quality-reviewer` for non-trivial plans.
5. Create a plan file under `docs/agent-reports/plans/`.
6. Use `agents/skills/implementation-plan/templates/implementation-plan.md` as the base template when available.
7. Fill every section of the template.
8. If a section is not applicable, write `Not applicable` instead of deleting it.
9. Do not modify source code during this skill.
10. Do not run formatters or tests unless they are needed for investigation and do not modify files.
11. In the final response, report only:
    - the created plan file path
    - a short summary
    - blocking open questions, if any
    - recommended next step

## Subagent Delegation Prompts

### Context Research Prompt

Use a prompt like:

```markdown
You are the `implementation-plan-context-researcher` subagent.

User request:

<user request>

Candidate source material:

- <paths>

Please perform targeted read-only investigation for implementation planning.

Focus on:
- relevant existing reports
- relevant source files
- relevant tests
- project configuration
- existing behavior
- risks and constraints
- missing information

Do not modify files.
Do not implement the change.
Return the result using your required output format.
````

### Strategy Design Prompt

Use a prompt like:

```markdown
You are the `implementation-plan-strategy-designer` subagent.

User request:

<user request>

Context research result:

<context research result>

Please create an implementation strategy.

Include:
- recommended approach
- considered options
- implementation phases
- file-level change plan
- validation strategy
- risks and mitigations
- rollback plan
- done criteria

Do not modify files.
Return the result using your required output format.
```

### Quality Review Prompt

Use a prompt like:

```markdown
You are the `implementation-plan-quality-reviewer` subagent.

User request:

<user request>

Context research result:

<context research result>

Strategy result:

<strategy result>

Draft implementation plan:

<draft plan>

Please review the draft for completeness, grounding, testability, risks, and clarity.

Do not modify files.
Return required fixes and suggested improvements using your required output format.
```

## Quality Checklist

Before finishing, verify that the plan:

* is based on actual repository investigation
* uses subagent results when available
* references the source material used
* identifies concrete files to change
* breaks work into clear phases
* includes tests and validation commands
* separates facts from assumptions
* identifies risks and mitigations
* avoids unnecessary refactoring
* does not implement the change
* is detailed enough for another coding agent to execute

## Planning Depth Guidelines

### Small Change

For small, localized changes:

* context researcher may be enough
* strategy designer is optional if the implementation path is obvious
* quality reviewer is optional
* keep the plan concise
* identify exact file/function targets
* include minimal but sufficient tests
* avoid over-design

### Medium Change

For changes touching multiple files:

* use context researcher
* use strategy designer
* use quality reviewer when risk or ambiguity exists
* include phased implementation
* identify dependencies between steps
* include regression tests
* document compatibility concerns

### Large Change

For architecture-level changes:

* use all three subagents
* include design alternatives
* include migration or rollout strategy
* include risk analysis
* include incremental delivery milestones
* consider feature flags or compatibility layers if useful

## Handling Insufficient Information

If the existing investigation report is missing important details, delegate targeted read-only investigation to `implementation-plan-context-researcher`.

If information is still insufficient after reasonable investigation:

* do not invent details
* document the unknowns
* mark blocking questions clearly
* provide the best safe partial plan
* recommend the next investigation step

## Example Final Response

```markdown
Created the implementation plan here:

- `docs/agent-reports/plans/2026-06-10-add-xxx-implementation-plan.md`

Summary:

- The plan proposes a small incremental change centered on `src/...`, with tests added under `tests/...`.

Blocking open questions:

- Whether the new behavior should be enabled by default or behind an option.

Recommended next step:

- Confirm the blocking question, then implement Phase 1 and Phase 2 from the plan.
```
