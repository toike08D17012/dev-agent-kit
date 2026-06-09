# Markdown Instructions

## 1. Scope

Apply these instructions when editing:

- Markdown files (`*.md`)
- Agent instruction files
- Skill files such as `SKILL.md`
- README files
- Documentation files
- Plan files under `.agents/plans/`

## 2. General Style

- Write clear, structured Markdown.
- Use concise headings.
- Prefer short sections over long dense blocks.
- Use bullet lists for procedures, requirements, and checklists.
- Use tables only when they make comparison easier.
- Keep code fences language-tagged when possible.
- Avoid vague wording in agent-facing instructions.
- Keep instructions actionable and testable.
- Avoid duplicating the same rule in multiple places unless required for tool compatibility.

## 3. Language Policy

- Write agent-facing instructions in English.
- Write user-facing documentation in the language used by the surrounding documentation.
- When documentation is primarily Japanese, use natural Japanese.
- Do not mix Japanese and English in the same sentence unless technical terms make it necessary.
- Keep code identifiers, command names, file paths, and tool names unchanged.

## 4. Agent-Facing Markdown

For files such as `AGENTS.md`, `.agents/instructions/*.md`, and `SKILL.md`:

- Prefer direct imperative wording.
- Avoid ambiguous words such as "basically", "maybe", "probably", and "as needed" unless the condition is clearly defined.
- Keep always-loaded files concise.
- Move detailed language-specific or task-specific guidance to separate instruction or skill files.
- Do not include secrets, private URLs, or machine-specific local paths.
- Do not include tool-specific syntax in shared instructions unless it is intentionally shared.

## 5. Plan Files

Plan files under `.agents/plans/` must be specific enough for review before implementation.

A plan file should include:

- goal
- current understanding
- files likely to change
- proposed steps
- validation plan
- risks and considerations
- acceptance criteria

Do not use plan files to hide implementation details after the fact. If implementation diverges from the plan, add an `Implementation Notes` section.

## 6. Links and References

- Prefer relative links for repository files.
- Keep external links stable and relevant.
- Do not add raw URLs when a readable Markdown link is clearer.
- Check whether linked files or headings exist when practical.
- Do not invent references.

## 7. Code Blocks

- Use fenced code blocks.
- Add a language tag such as `python`, `bash`, `text`, `toml`, or `markdown` when practical.
- Ensure commands are copy-pasteable when shown as commands.
- Avoid mixing command output and commands in the same code block unless clearly labeled.

## 8. Checklist

Before finishing Markdown changes, confirm:

- [ ] The Markdown structure is clear.
- [ ] Headings and lists are consistent.
- [ ] Code fences have language tags where practical.
- [ ] Links are valid or reasonably checked.
- [ ] Agent-facing instructions are concise and actionable.
- [ ] No secrets or machine-specific local paths were added.
