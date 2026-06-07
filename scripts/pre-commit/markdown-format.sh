#!/usr/bin/env bash

set -euo pipefail

run_markdown_check() {
    if ! command -v prettier >/dev/null 2>&1; then
        echo "Error: prettier is not installed." >&2
        exit 1
    fi

    if ! command -v markdownlint-cli2 >/dev/null 2>&1; then
        echo "Error: markdownlint-cli2 is not installed." >&2
        exit 1
    fi

    if [ "$#" -gt 0 ]; then
        prettier --write "$@"
        markdownlint-cli2 --fix "$@"
        prettier --write "$@"
    else
        prettier --write "**/*.md"
        markdownlint-cli2 --fix "**/*.md"
        prettier --write "**/*.md"
    fi
}

main() {
    local hook_dir

    hook_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
    # Move to the project root directory.
    cd "${hook_dir}/../.."

    if ! command -v docker >/dev/null 2>&1; then
        run_markdown_check "$@"
        return
    fi

    exec ./docker/run-docker.sh run_markdown_check "$@"
}

main "$@"
