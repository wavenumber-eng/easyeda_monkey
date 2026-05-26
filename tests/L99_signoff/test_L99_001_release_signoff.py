"""Release signoff tests for the public package."""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path

import easyeda_monkey


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
EXPECTED_VERSION = "2026.5.26.2"
EXPECTED_RELEASE_DATE = date(2026, 5, 26)


def test_version_contract_matches_date_based_release() -> None:
    """Verify that package version metadata follows the date release contract."""
    pyproject = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["version"] == EXPECTED_VERSION
    assert easyeda_monkey.__version__ == EXPECTED_VERSION
    assert EXPECTED_RELEASE_DATE <= date.today()


def test_changelog_mentions_package_version() -> None:
    """Verify that release notes mention the current package version."""
    changelog = (PACKAGE_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert f"## {EXPECTED_VERSION}" in changelog


def test_developer_working_docs_are_excluded_from_release_artifacts() -> None:
    """Verify that developer-only plan and research docs are not packaged."""
    pyproject = tomllib.loads((PACKAGE_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    sdist = pyproject["tool"]["hatch"]["build"]["targets"]["sdist"]

    assert "docs/**" in sdist["include"]
    assert "docs/plans/**" in sdist["exclude"]
    assert "docs/research/**" in sdist["exclude"]


def test_python_signoff_does_not_regress() -> None:
    """Verify that the Python source signoff has no findings."""
    baseline = PACKAGE_ROOT / "tests" / "support_scripts" / "py_signoff_baseline.json"
    script = PACKAGE_ROOT / "tests" / "support_scripts" / "py_signoff.py"

    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--root",
            str(PACKAGE_ROOT),
            "--baseline",
            str(baseline),
            "--format",
            "json",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    payload = json.loads(completed.stdout)
    assert payload["finding_count"] == 0
