#!/usr/bin/env python3
"""Clay SDK update pipeline, powered by Dagger.

Commands:
    fetch-openapi              Refresh openapi/openapi.json from Clay
    generate [--force]         Refresh the spec and regenerate the SDK
    test                       Type-check the generated SDK in a container
    build                      Build wheel and source distribution in a container
    publish                    Build and publish artifacts to PyPI
    ci [--force] [--publish]   Refresh, generate, check, build, and optionally publish

Run through the Dagger CLI so the module's isolated steps use the same
environment locally and in CI::

    dagger run uv run python ci/pipeline.py generate
    dagger run uv run python ci/pipeline.py ci

``SPEAKEASY_API_KEY`` is used as a Dagger secret when set.  Otherwise the
pipeline uses an authenticated local Speakeasy CLI session.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Annotated
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import dagger  # type: ignore[import-untyped]
from dagger import Directory, Doc, dag, function  # type: ignore[import-untyped]

_OPENAPI_URL = "https://developers.clay.com/openapi.json"
_OPENAPI_PATH = Path("openapi/openapi.json")
_PYPI_PUBLISHER_MODULE = "github.com/elviskahoro/sdk-python-publish-to-pypi@main"


def fetch_latest_spec() -> Path:
    """Fetch Clay's public OpenAPI document and write a normalized JSON file."""
    request = Request(_OPENAPI_URL, headers={"Accept": "application/json"})
    print(f"Fetching latest OpenAPI spec from {_OPENAPI_URL}...", file=sys.stderr)
    try:
        with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed HTTPS URL
            spec_data = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not fetch a valid Clay OpenAPI spec: {error}") from error

    if not isinstance(spec_data, dict) or not isinstance(spec_data.get("paths"), dict):
        raise RuntimeError("Clay OpenAPI response does not contain a top-level paths object")

    _OPENAPI_PATH.parent.mkdir(parents=True, exist_ok=True)
    _OPENAPI_PATH.write_text(json.dumps(spec_data, indent=2) + "\n")
    print(f"Saved latest OpenAPI spec to {_OPENAPI_PATH}", file=sys.stderr)
    return _OPENAPI_PATH


def _has_local_speakeasy_auth() -> bool:
    """Return whether the installed Speakeasy CLI has an authenticated session."""
    result = subprocess.run(
        ["speakeasy", "auth", "status"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


async def _run_local_speakeasy(*, force: bool) -> None:
    """Generate using the authenticated host CLI session."""
    command = ["speakeasy", "run", "--auto-yes", "--output", "console", "--skip-upload-spec"]
    if force:
        command.append("--force")
    await asyncio.to_thread(subprocess.run, command, check=True)


def _host_source_dir() -> Directory:
    """Create a source snapshot without host-specific runtime state."""
    return dag.host().directory(
        ".",
        exclude=[
            ".git",
            ".venv",
            ".beads",
            ".env",
            ".env.*",
            "dist",
            ".mypy_cache",
            ".pytest_cache",
            "**/__pycache__",
        ],
    )


def _replace_dist_directory() -> None:
    """Clear old build artifacts before exporting the fresh Dagger build."""
    dist_dir = Path("dist")
    if dist_dir.is_symlink() or dist_dir.is_file():
        dist_dir.unlink()
    elif dist_dir.is_dir():
        shutil.rmtree(dist_dir)


def _load_pypi_token() -> None:
    """Load PYPI_TOKEN from the environment or the untracked .env.local file.

    The token is only placed in this process environment. The publisher accepts
    it through Dagger's ``env:PYPI_TOKEN`` secret mechanism, so it is neither
    printed nor copied into the generated SDK or build artifacts.
    """
    if os.environ.get("PYPI_TOKEN"):
        return

    env_file = Path(".env.local")
    if env_file.is_file():
        for raw_line in env_file.read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line.removeprefix("export ").lstrip()
            key, separator, value = line.partition("=")
            if key.strip() != "PYPI_TOKEN" or not separator:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            if value:
                os.environ["PYPI_TOKEN"] = value
                return

    raise RuntimeError("PYPI_TOKEN is not set and was not found in .env.local")


def _publish_artifacts() -> None:
    """Publish the freshly built artifacts through the shared Dagger module."""
    if not Path("dist").is_dir():
        raise RuntimeError("dist/ does not exist; run the build command before publishing")
    # ``dagger run`` injects connection variables for its current session. The
    # publisher is a separate Dagger module, so it must start its own session
    # rather than attempting to nest a client inside the parent session.
    publisher_environment = {
        key: value for key, value in os.environ.items() if not key.startswith("DAGGER_")
    }
    subprocess.run(
        [
            "dagger",
            "-m",
            _PYPI_PUBLISHER_MODULE,
            "call",
            "publish-artifacts",
            "--artifacts",
            "./dist",
            "--pypi-token",
            "env:PYPI_TOKEN",
        ],
        check=True,
        env=publisher_environment,
    )


class ClaySDKPipeline:
    """Dagger functions for Clay SDK generation and verification."""

    def __init__(self, source: Directory) -> None:
        self.source = source

    @function
    def builder_env(self) -> dagger.Container:
        """Return a cached Python/uv build environment."""
        return (
            dag.container()
            .from_("python:3.13-slim")
            .with_mounted_cache("/root/.cache/pip", dag.cache_volume("clay-pip-cache"))
            .with_exec(["pip", "install", "uv"])
            .with_mounted_directory("/repo", self.source)
            .with_workdir("/repo")
        )

    @function
    def dependencies_installed(self, container: dagger.Container) -> dagger.Container:
        """Install the locked project dependencies."""
        return container.with_exec(["uv", "sync", "--locked"])

    @function
    async def test(self) -> str:
        """Compile and type-check the generated SDK."""
        environment = self.dependencies_installed(self.builder_env())
        checked = environment.with_exec(["uv", "run", "python", "-m", "compileall", "-q", "src"])
        return await checked.with_exec(["uv", "run", "mypy", "src"]).stdout()

    @function
    def build(self) -> dagger.Container:
        """Build wheel and source-distribution artifacts."""
        return self.builder_env().with_exec(["uv", "build", "--out-dir", "/dist"])

    @function
    def speakeasy_env(self, api_key: dagger.Secret) -> dagger.Container:
        """Return the isolated Speakeasy generator environment."""
        return (
            dag.container()
            .from_("ghcr.io/speakeasy-api/speakeasy:latest")
            .with_mounted_cache("/var/cache/apt/archives", dag.cache_volume("clay-apt-cache"))
            .with_exec(["/bin/sh", "-c", "sudo apt-get update && sudo apt-get install -y ca-certificates"])
            .with_secret_variable("SPEAKEASY_API_KEY", api_key)
            .with_mounted_directory("/repo", self.source)
            .with_workdir("/repo")
        )

    @function
    async def generate(
        self,
        api_key: Annotated[dagger.Secret, Doc("Speakeasy API key")],
        *,
        force: Annotated[bool, Doc("Force regeneration")] = False,
    ) -> dagger.Directory:
        """Regenerate the SDK and return the complete generated checkout."""
        command = ["/bin/sh", "-c", "sudo chown -R speakeasy:speakeasy /repo && mkdir -p .speakeasy/temp"]
        prepared = self.speakeasy_env(api_key).with_exec(command)
        run_args = ["speakeasy", "run"]
        if force:
            run_args.append("--force")
        generated = prepared.with_exec(run_args)
        await generated.sync()
        return generated.directory("/repo")


async def cmd_fetch_openapi() -> None:
    fetch_latest_spec()


async def cmd_generate(*, force: bool) -> None:
    """Refresh the spec, generate the SDK, and export results to this checkout."""
    fetch_latest_spec()
    api_key_value = os.environ.get("SPEAKEASY_API_KEY")
    if not api_key_value:
        if not _has_local_speakeasy_auth():
            raise RuntimeError("SPEAKEASY_API_KEY is not set and the local Speakeasy CLI is not authenticated")
        await _run_local_speakeasy(force=force)
        return

    async with dagger.connection(dagger.Config(log_output=sys.stderr)):
        pipeline = ClaySDKPipeline(source=_host_source_dir())
        generated = await pipeline.generate(api_key=dag.set_secret("SPEAKEASY_API_KEY", api_key_value), force=force)
        await generated.export(".")


async def cmd_test() -> None:
    async with dagger.connection(dagger.Config(log_output=sys.stderr)):
        result = await ClaySDKPipeline(source=_host_source_dir()).test()
        print(result)


async def cmd_build() -> None:
    async with dagger.connection(dagger.Config(log_output=sys.stderr)):
        built = ClaySDKPipeline(source=_host_source_dir()).build()
        _replace_dist_directory()
        await built.directory("/dist").export("./dist")
        print("Build completed successfully (artifacts in ./dist)", file=sys.stderr)


async def cmd_publish() -> None:
    """Build the SDK once and publish its artifacts to PyPI."""
    _load_pypi_token()
    await cmd_build()
    _publish_artifacts()


async def cmd_ci(*, force: bool, publish: bool) -> None:
    await cmd_generate(force=force)
    await cmd_test()
    await cmd_build()
    if publish:
        _load_pypi_token()
        _publish_artifacts()


def main() -> None:
    parser = argparse.ArgumentParser(description="Clay SDK Dagger pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("fetch-openapi", help="Refresh openapi/openapi.json from Clay")
    subparsers.add_parser("test", help="Compile and type-check the SDK in Dagger")
    subparsers.add_parser("build", help="Build distribution artifacts in Dagger")
    subparsers.add_parser("publish", help="Build and publish artifacts to PyPI")
    generate = subparsers.add_parser("generate", help="Refresh the spec and regenerate the SDK")
    generate.add_argument("--force", action="store_true", help="Force Speakeasy regeneration")
    ci = subparsers.add_parser("ci", help="Refresh, generate, check, build, and optionally publish")
    ci.add_argument("--force", action="store_true", help="Force Speakeasy regeneration")
    ci.add_argument("--publish", action="store_true", help="Publish freshly built artifacts to PyPI")
    args = parser.parse_args()

    if args.command == "fetch-openapi":
        asyncio.run(cmd_fetch_openapi())
    elif args.command == "generate":
        asyncio.run(cmd_generate(force=args.force))
    elif args.command == "test":
        asyncio.run(cmd_test())
    elif args.command == "build":
        asyncio.run(cmd_build())
    elif args.command == "publish":
        asyncio.run(cmd_publish())
    elif args.command == "ci":
        asyncio.run(cmd_ci(force=args.force, publish=args.publish))


if __name__ == "__main__":
    main()
