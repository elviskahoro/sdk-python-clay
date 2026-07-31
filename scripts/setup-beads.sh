#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Conductor worktrees must not reuse a parent repository's .beads database.
mkdir -p .beads-local
if [[ ! -f .beads/redirect ]]; then
  printf '%s\n' '.beads-local' > .beads/redirect
fi

bd init \
  --init-if-missing \
  --non-interactive \
  --prefix clay \
  --skip-agents \
  --skip-hooks

remote_url='https://doltremoteapi.dolthub.com/elviskahoro/sdk-python-clay'
if ! bd dolt remote list | awk '$1 == "origin" { found = 1 } END { exit !found }'; then
  bd dolt remote add origin "$remote_url"
fi
