#!/usr/bin/env sh
set -eu

SSH_HOST_KEY_PATH="${SSH_HOST_KEY_PATH:-/app/data/ssh_host_key}"
SSH_PORT="${SSH_PORT:-2222}"

mkdir -p "$(dirname "$SSH_HOST_KEY_PATH")"

if [ ! -f "$SSH_HOST_KEY_PATH" ]; then
  ssh-keygen -t ed25519 -N "" -f "$SSH_HOST_KEY_PATH" >/dev/null
fi

chmod 600 "$SSH_HOST_KEY_PATH"

export SSH_HOST="${SSH_HOST:-0.0.0.0}"
export SSH_PORT
export SSH_HOST_KEY_PATH

exec python -m app.server.server
