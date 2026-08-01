#!/usr/bin/env bash
# Tag a release.
#
# This script does NOT bump the version or write any files. Speakeasy's
# `versioningStrategy: automatic` (see .speakeasy/gen.yaml) picks the version
# bump and writes it into pyproject.toml, src/clay/_version.py, and
# .speakeasy/gen.lock as part of the regen commit, which is reviewed and
# merged to main via PR. By the time you run this script the version already
# exists on origin/main — this script's only job is to tag that commit and
# push the tag, after refusing to do so if something doesn't line up.
#
# Pushing the tag fires .github/workflows/pypi.yml, which re-verifies the tag
# against pyproject.toml and publishes via PyPI Trusted Publishing (OIDC).
#
# Usage: scripts/release.sh [--dry-run] [--yes] [--version <v>]
#
#   --dry-run        Do everything except the confirmation prompt and the
#                     final `git push`. Prints the resolved version/commit.
#   --yes            Skip the interactive confirmation prompt.
#   --version <v>    Explicit opt-in to tag a specific version instead of
#                     whatever origin/main currently carries. Use this only
#                     to re-tag an older, already-merged commit; it does not
#                     search history for you.

set -euo pipefail

trap 'code=$?; if [[ ${code} -eq 141 ]]; then echo "release.sh hit a transient SIGPIPE (exit 141) - this is a known intermittent shell/pipe issue, not a logic bug; just re-run the script." >&2; fi; exit ${code}' EXIT

dry_run=0
assume_yes=0
explicit_version=""

usage() {
  cat <<'EOF'
Usage: scripts/release.sh [--dry-run] [--yes] [--version <v>]

Tags origin/main's current version and pushes the tag, which fires the
Publish to PyPI workflow. Does not write any files or create commits;
Speakeasy already wrote the version during the regen that merged to main.

  --dry-run        Print the resolved version/commit; push nothing.
  --yes            Skip the interactive confirmation prompt.
  --version <v>    Tag this version explicitly instead of reading it from
                    origin/main (opt-in escape hatch, e.g. to re-tag an
                    older commit).
  -h, --help       Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      dry_run=1
      shift
      ;;
    --yes)
      assume_yes=1
      shift
      ;;
    --version)
      if [[ $# -lt 2 ]]; then
        echo "Error: --version requires an argument" >&2
        exit 2
      fi
      explicit_version="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unrecognized argument '$1'" >&2
      usage >&2
      exit 2
      ;;
  esac
done

repo_root="$(git rev-parse --show-toplevel)"
cd "${repo_root}"

echo "Fetching origin/main and tags..."
git fetch origin main --tags

release_commit="origin/main"
commit_sha="$(git rev-parse --short "${release_commit}")"
commit_subject="$(git log -1 --format='%s' "${release_commit}")"
echo "Release commit: ${commit_sha} ${commit_subject}"

pyproject_version="$(
  git show "${release_commit}:pyproject.toml" \
    | python3 -c "import sys, tomllib; print(tomllib.loads(sys.stdin.read())['project']['version'])"
)"

version_py_version="$(
  git show "${release_commit}:src/clay/_version.py" \
    | grep '^__version__: str' \
    | sed -E 's/^__version__: str = "([^"]+)"/\1/'
)"

gen_lock_version="$(
  git show "${release_commit}:.speakeasy/gen.lock" \
    | grep 'releaseVersion:' \
    | sed -E 's/^[[:space:]]*releaseVersion:[[:space:]]*//'
)"

if [[ "${pyproject_version}" != "${version_py_version}" || "${pyproject_version}" != "${gen_lock_version}" ]]; then
  echo "Error: version sources disagree at ${commit_sha}:" >&2
  echo "  pyproject.toml:        ${pyproject_version}" >&2
  echo "  src/clay/_version.py:  ${version_py_version}" >&2
  echo "  .speakeasy/gen.lock:   ${gen_lock_version}" >&2
  echo "This means a Speakeasy regen was partially committed. Do not release." >&2
  exit 1
fi

version="${pyproject_version}"
if [[ -n "${explicit_version}" ]]; then
  echo "Note: --version overrides resolved version ${version} with ${explicit_version}"
  version="${explicit_version}"
fi

if ! [[ ${version} =~ ^[0-9]+\.[0-9]+\.[0-9]+([a-zA-Z0-9.+-]*)?$ ]]; then
  echo "Error: '${version}' does not look like a SemVer (e.g. 0.0.2 or 1.0.0rc1)" >&2
  exit 2
fi

echo "Resolved version: ${version}"

if git rev-parse -q --verify "refs/tags/v${version}" >/dev/null; then
  echo "Error: tag v${version} already exists locally." >&2
  exit 1
fi

if git ls-remote --exit-code --tags origin "refs/tags/v${version}" >/dev/null 2>&1; then
  echo "Error: tag v${version} already exists on origin." >&2
  exit 1
fi

echo "Checking PyPI for an existing gtm-clay ${version} release..."
pypi_json="$(curl -sf https://pypi.org/pypi/gtm-clay/json || true)"
if [[ -z "${pypi_json}" ]]; then
  echo "Warning: could not reach PyPI to check existing releases. Proceeding without this check." >&2
else
  if echo "${pypi_json}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
sys.exit(0 if '${version}' in data.get('releases', {}) else 1)
"; then
    echo "Error: gtm-clay ${version} is already published on PyPI." >&2
    exit 1
  fi
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Warning: working tree is dirty. This does not affect the tag on origin/main," >&2
  echo "but usually means you think you're releasing something you aren't." >&2
fi

local_branch="$(git rev-parse --abbrev-ref HEAD)"
local_sha="$(git rev-parse HEAD)"
main_sha="$(git rev-parse "${release_commit}")"
if [[ "${local_sha}" != "${main_sha}" ]]; then
  echo "Warning: local HEAD (${local_branch} @ $(git rev-parse --short HEAD)) differs from origin/main (${commit_sha})." >&2
  echo "This does not affect the tag on origin/main, but check you meant to release ${commit_sha}." >&2
fi

echo
echo "About to tag v${version} -> ${commit_sha} (${commit_subject}) and push to origin."

if [[ ${dry_run} -eq 1 ]]; then
  echo "Dry run: stopping before confirmation/push."
  exit 0
fi

if [[ ${assume_yes} -ne 1 ]]; then
  read -r -p "Proceed? [y/N] " reply
  if [[ ! ${reply} =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
  fi
fi

git tag "v${version}" "${release_commit}"
git push origin "v${version}"

echo
echo "Pushed v${version}. Watch the publish run:"
echo "  gh run watch \$(gh run list --workflow='Publish to PyPI' --limit 1 --json databaseId -q '.[0].databaseId')"
