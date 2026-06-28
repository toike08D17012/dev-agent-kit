#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

# ==== 設定（必要なら変更）====
export USER_NAME="${USER_NAME:-kujira}"
export GROUP_NAME="${GROUP_NAME:-$USER_NAME}"

CONTEXT=".." # レポジトリルート
REPO_NAME="$(basename "$(cd "${CONTEXT}" && pwd)")"
export REPO_NAME

# bash の組込み $UID をそのまま使う（上書きしない）
USER_UID="${UID}"
USER_GID="$(id -g)"
USER_HOME="/home/${USER_NAME}"

export USER_UID
export USER_GID
export USER_HOME

# ==== 実行 ====
echo "Build args:"
echo "  REPO_NAME=${REPO_NAME}"
echo "  USER_NAME=${USER_NAME}"
echo "  GROUP_NAME=${GROUP_NAME}"
echo "  USER_UID=${USER_UID}"
echo "  USER_GID=${USER_GID}"
echo "  HOME=${USER_HOME}"

docker compose build
