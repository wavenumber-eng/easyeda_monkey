"""Rack-owned source quality tool checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()


def _run_module(module: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Run a Python module from the repository root and capture output."""
    return subprocess.run(
        [sys.executable, "-m", module, *args],
        cwd=PACKAGE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_ruff_check_passes() -> None:
    """Verify that linting is part of the Rack signoff gate."""
    completed = _run_module("ruff", "check", ".")

    assert completed.returncode == 0, completed.stderr + completed.stdout


def test_pyright_check_passes() -> None:
    """Verify that type checking is part of the Rack signoff gate."""
    completed = _run_module("pyright", "src/py", "tests")

    assert completed.returncode == 0, completed.stderr + completed.stdout
