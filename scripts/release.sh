#!/usr/bin/env bash
# Cut a new release: bump version in pyproject.toml + src/clay/_version.py,
# commit, tag, and push. The Publish to PyPI workflow fires on the tag push
# and publishes via PyPI Trusted Publishing (OIDC) — no token required.
#
# Usage: scripts/release.sh 0.0.2

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>  e.g. $0 0.0.2" >&2
  exit 2
fi

version="$1"

if ! [[ ${version} =~ ^[0-9]+\.[0-9]+\.[0-9]+([a-zA-Z0-9.+-]*)?$ ]]; then
  echo "Error: '${version}' does not look like a SemVer (e.g. 0.0.2 or 1.0.0rc1)" >&2
  exit 2
fi

repo_root="$(git rev-parse --show-toplevel)"
cd "${repo_root}"

status_output="$(git status --porcelain)"
if [[ -n ${status_output} ]]; then
  echo "Error: working tree is dirty. Commit or stash changes first." >&2
  git status --short >&2
  exit 1
fi

branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ ${branch} != "main" ]]; then
  echo "Error: not on main (current: ${branch}). Release from main." >&2
  exit 1
fi

if git rev-parse -q --verify "refs/tags/v${version}" >/dev/null; then
  echo "Error: tag v${version} already exists locally." >&2
  exit 1
fi

if git ls-remote --exit-code --tags origin "refs/tags/v${version}" >/dev/null 2>&1; then
  echo "Error: tag v${version} already exists on origin." >&2
  exit 1
fi

git pull --ff-only origin main

current_version="$(uv run --no-project python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")"

python3 - "$current_version" "$version" <<'EOF'
import sys
from pathlib import Path

current, new = sys.argv[1], sys.argv[2]

pyproject = Path("pyproject.toml")
pyproject.write_text(
    pyproject.read_text().replace(f'version = "{current}"', f'version = "{new}"', 1)
)

version_file = Path("src/clay/_version.py")
version_file.write_text(version_file.read_text().replace(current, new))
EOF

# Sanity check: confirm both files agree with the requested version.
grep -q "version = \"${version}\"" pyproject.toml
grep -q "\"${version}\"" src/clay/_version.py

uv lock

git add pyproject.toml src/clay/_version.py uv.lock
git commit -m "chore: bump version to ${version}"
git tag "v${version}"
git push origin main "v${version}"

echo
echo "Pushed v${version}. Watch the publish run:"
echo "  gh run watch \$(gh run list --workflow='Publish to PyPI' --limit 1 --json databaseId -q '.[0].databaseId')"
