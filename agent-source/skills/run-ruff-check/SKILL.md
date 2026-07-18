---
name: run-ruff-check
description: Use this skill when asked to run Ruff lint checks, fix Ruff lint errors, investigate Ruff errors, or keep Python linting clean. By default, run Ruff check with --fix through the repository wrapper script so fixable lint issues are corrected automatically.
argument-hint: "[ruff check args ...]"
--------------------------------------

# Run Ruff check

Use this skill when the user asks to:

* run Ruff lint checks
* fix Ruff lint errors
* investigate Ruff errors
* keep Python linting clean
* verify lint status after code changes

## Core rule

Do not run `ruff check` directly.

Always run Ruff check through the repository wrapper script:

```bash
./scripts/pre-commit/ruff-check.sh [RUFF_CHECK_ARGS ...]
```

Preserve every target and option supplied by the user. Do not silently replace or broaden the requested scope.

When the user provides no target or options, prefer running Ruff with automatic fixes enabled:

```bash
./scripts/pre-commit/ruff-check.sh --fix .
```

The project should normally be kept in a state where running `ruff check --fix` produces no additional changes.

This wrapper handles both cases:

* when called from the local host environment, it runs Ruff through `./docker/run-docker.sh`
* when called from an environment without Docker, such as a devcontainer or project container, it runs `ruff check` directly inside the current container

## Before running

From the repository root, confirm that the wrapper exists:

```bash
test -f ./scripts/pre-commit/ruff-check.sh
```

If it is not executable, make it executable:

```bash
chmod +x ./scripts/pre-commit/ruff-check.sh
```

## Common commands

Run Ruff check and apply safe fixes:

```bash
./scripts/pre-commit/ruff-check.sh --fix .
```

Run Ruff check and apply safe fixes to a specific directory:

```bash
./scripts/pre-commit/ruff-check.sh --fix src
```

Run Ruff check and apply safe fixes to a specific file:

```bash
./scripts/pre-commit/ruff-check.sh --fix src/package/module.py
```

Run Ruff check without applying fixes only when read-only verification is specifically useful:

```bash
./scripts/pre-commit/ruff-check.sh .
```

Show remaining differences or unfixed issues:

```bash
./scripts/pre-commit/ruff-check.sh --diff .
```

Use unsafe fixes only when the user or repository policy allows them:

```bash
./scripts/pre-commit/ruff-check.sh --fix --unsafe-fixes .
```

## Workflow

When working on Python code:

1. Make the requested code changes.

2. Run Ruff check against the user-specified target. When no scope was specified, use the no-argument behavior defined in the core rule:

   ```bash
   ./scripts/pre-commit/ruff-check.sh --fix .
   ```

3. Review any remaining Ruff errors.

4. Fix remaining issues manually when needed.

5. After a fix, re-run the smallest failing file or directory that can confirm the result.

6. Expand back to the user-requested scope when needed to establish the requested result, or when fixes affect shared imports, configuration, or multiple packages.

7. Stop after a successful check. Do not repeat it unless relevant files or Ruff configuration change afterward.

## Error handling

If Ruff check fails:

1. Report the exact command that was run.
2. Summarize the important remaining Ruff rule violations.
3. Identify whether each issue is likely:

   * automatically fixable but blocked by syntax or context
   * a real code quality issue
   * an import sorting issue
   * an unused variable/import issue
   * a formatting-related issue that should be handled by `ruff format`
4. Prefer the smallest focused fix.
5. Re-run the smallest target that confirms the fix, then restore the user-requested scope when required.

## Do not do this

Do not run these commands directly unless the user explicitly asks for host execution:

```bash
ruff check
python -m ruff check
docker compose run app ruff check
docker compose run app-gpu ruff check
```

Use the wrapper script instead.

## Reporting format

After execution, report:

```text
Command:
./scripts/pre-commit/ruff-check.sh --fix ...

Result:
Passed / Failed

Important output:
...

Next action:
...
```

If Ruff applied fixes, briefly summarize the changed files based on command output or `git diff --stat`.
