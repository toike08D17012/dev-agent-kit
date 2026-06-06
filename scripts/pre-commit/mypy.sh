#!/usr/bin/env bash

set -euo pipefail

main() {
    local hook_dir

    hook_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
    cd "${hook_dir}/../.."

    if ! command -v docker >/dev/null 2>&1; then
        echo "ERROR: docker is required. Please install/start Docker and retry." >&2
        exit 1
    fi

    exec ./docker/run-docker.sh mypy "$@"
}

main "$@"
