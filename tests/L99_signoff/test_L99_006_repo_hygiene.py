"""Repository hygiene signoff tests."""

from __future__ import annotations

import subprocess
import tomllib
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
REQUIRED_FILES = (
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "pyproject.toml",
    "uv.lock",
)


def test_required_hygiene_files_exist() -> None:
    """Verify root files required by the public package standard exist."""
    for relative_path in REQUIRED_FILES:
        assert (PACKAGE_ROOT / relative_path).exists(), relative_path


def test_env_file_is_ignored_and_not_tracked() -> None:
    """Verify local secret files are ignored and not tracked."""
    gitignore = (PACKAGE_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore
    result = subprocess.run(
        ["git", "ls-files", ".env"],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_sdist_excludes_temporary_plans_research_and_results() -> None:
    """Verify release artifacts exclude working notes and local results."""
    with (PACKAGE_ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = cast(Mapping[str, object], tomllib.load(handle))
    tool = cast(Mapping[str, object], pyproject["tool"])
    hatch = cast(Mapping[str, object], tool["hatch"])
    build = cast(Mapping[str, object], hatch["build"])
    targets = cast(Mapping[str, object], build["targets"])
    sdist = cast(Mapping[str, object], targets["sdist"])
    exclude = cast(Sequence[str], sdist["exclude"])

    assert "docs/plans/**" in exclude
    assert "docs/research/**" in exclude
    assert "tests/rack_results/**" in exclude


def test_setup_doc_records_tooling_and_binary_distribution_policy() -> None:
    """Verify setup docs mention tooling and future binary artifact layout."""
    setup_doc = (PACKAGE_ROOT / "docs" / "setup.html").read_text(encoding="utf-8")

    assert "uv" in setup_doc
    assert "Rack" in setup_doc
    assert "dist/native/windows-x64/" in setup_doc
    assert "dist/wasm/browser/" in setup_doc
