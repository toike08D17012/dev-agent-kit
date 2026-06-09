#!/usr/bin/env bash

# Usage:
#   ./scripts/sync.sh <target_directory> [additional_cli_options...]
#
# Examples:
#   ./scripts/sync.sh /path/to/repo
#   ./scripts/sync.sh /path/to/repo --force
#   ./scripts/sync.sh /path/to/repo --disable-codex --force

set -euo pipefail

# Move to repository root directory
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

# Set PYTHONPATH to `src` directory to ensure imports work correctly
PYTHONPATH="$(pwd)/src"
export PYTHONPATH

# arguments check
if [[ "$#" -eq 0 ]]; then
    echo "Usage: $0 <target_directory> [additional_cli_options...]"
    exit 1
fi

target_dir="$1"
shift

# Run the synchronization script with target_dir and pass through extra CLI args.
exec python -m dev_agent_kit.cli --target-dir "${target_dir}" "$@"
