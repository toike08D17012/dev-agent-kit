#!/usr/bin/env bash

set -euo pipefail

main() {
    local generated_file=".devcontainer/docker-compose.generated.yml"

    echo "Checking for NVIDIA GPU..."

    if command -v nvidia-smi &>/dev/null && nvidia-smi >/dev/null 2>&1; then
        echo "NVIDIA GPU detected. Generating GPU override."
        cat >"${generated_file}" <<'YAML'
services:
    app:
        deploy:
            resources:
                reservations:
                    devices:
                        - driver: nvidia
                          count: all
                          capabilities: [gpu]
YAML
        echo "Created ${generated_file} with GPU settings."
    else
        echo "No NVIDIA GPU detected. Generating empty override configuration."
        echo "services: {}" >"${generated_file}"
        echo "Created empty ${generated_file}."
    fi
}

main "$@"
