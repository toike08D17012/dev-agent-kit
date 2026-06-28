#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  ./docker/run-docker.sh [COMMAND ...]
  ./docker/run-docker.sh -h | --help

Description:
  Runs the project container with automatic CPU/GPU switching.
  If NVIDIA GPU is available, it runs app-gpu with --profile gpu.
  Otherwise, it runs app.

Examples:
  ./docker/run-docker.sh
  ./docker/run-docker.sh pytest -q
EOF
}

main() {
    cd "$(dirname "$0")" || exit 1

    if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
        usage
        exit 0
    fi

    local -a command=(bash)
    if [[ "$#" -gt 0 ]]; then
        command=("$@")
    fi

    local service_name="app"
    local -a profile_args=()

    if command -v nvidia-smi &>/dev/null && nvidia-smi >/dev/null 2>&1; then
        echo "NVIDIA GPU detected. Running with GPU profile."
        profile_args+=(--profile gpu)
        service_name="app-gpu"
    else
        echo "No NVIDIA GPU detected. Running in CPU mode."
    fi

    # if bash_history does not exist,
    # create an empty file to avoid creating it as directory
    if [[ ! -f .bash_history ]]; then
        touch .bash_history
    fi

    local -a docker_compose_cmd=(docker compose)
    if [[ "${#profile_args[@]}" -gt 0 ]]; then
        docker_compose_cmd+=("${profile_args[@]}")
    fi

    docker_compose_cmd+=(
        run
        --rm
        -e "NEW_UID=$(id -u)"
        -e "NEW_GID=$(id -g)"
        "${service_name}"
        "${command[@]}"
    )

    "${docker_compose_cmd[@]}"
}

main "$@"
