"""Machine-readable contract signoff tests."""

from __future__ import annotations

import importlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

from easyeda_monkey.cli import CLI_COMMANDS, build_parser


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()


def _load_json_mapping(path: Path) -> Mapping[str, object]:
    """Load a JSON object."""
    return cast(Mapping[str, object], json.loads(path.read_text(encoding="utf-8")))


def _object_sequence(value: object, key: str) -> Sequence[Mapping[str, object]]:
    """Read a JSON list of objects."""
    if not isinstance(value, list):
        raise TypeError(f"expected {key} to be a list")
    items: list[Mapping[str, object]] = []
    for item in cast(list[object], value):
        if not isinstance(item, dict):
            raise TypeError(f"expected {key} entries to be objects")
        items.append(cast(Mapping[str, object], item))
    return items


def test_command_manifest_matches_cli_and_design_docs() -> None:
    """Verify command contracts match the registered CLI and docs."""
    manifest = _load_json_mapping(PACKAGE_ROOT / "docs" / "contracts" / "command_manifest.v0.json")
    commands = _object_sequence(manifest["commands"], "commands")
    registered = {command.name: command for command in CLI_COMMANDS}
    help_text = build_parser().format_help()

    for command in commands:
        name = cast(str, command["name"])
        module_name = cast(str, command["module"])
        design_doc = PACKAGE_ROOT / cast(str, command["design_doc"])
        data_command = cast(str, command["data_command"])

        assert name in registered
        assert name in help_text
        assert design_doc.exists()
        assert f'data-command="{data_command}"' in design_doc.read_text(encoding="utf-8")
        imported = importlib.import_module(module_name)
        assert hasattr(imported, "register")


def test_interface_manifest_matches_exports_and_design_docs() -> None:
    """Verify interface contracts match importable public objects and docs."""
    manifest = _load_json_mapping(
        PACKAGE_ROOT / "docs" / "contracts" / "interface_manifest.v0.json"
    )
    interfaces = _object_sequence(manifest["interfaces"], "interfaces")

    for item in interfaces:
        name = cast(str, item["name"])
        module_name, symbol_name = name.rsplit(".", 1)
        module = importlib.import_module(module_name)
        design_doc = PACKAGE_ROOT / cast(str, item["design_doc"])
        data_interface = cast(str, item["data_interface"])

        assert hasattr(module, symbol_name)
        assert design_doc.exists()
        assert f'data-interface="{data_interface}"' in design_doc.read_text(encoding="utf-8")


def test_standards_exceptions_are_documented() -> None:
    """Verify known standards exceptions are explicit and reviewable."""
    exceptions = _load_json_mapping(PACKAGE_ROOT / "docs" / "contracts" / "exceptions.json")
    entries = _object_sequence(exceptions["exceptions"], "exceptions")
    ids = {cast(str, entry["id"]) for entry in entries}

    assert "EASYEDA-JSON-ANY" in ids
    assert "EASYEDA-COMPLEXITY-RATCHET" in ids
    assert "EASYEDA-LEGACY-SRC-PY" in ids
    assert "EASYEDA-PYRIGHT-STANDARD" in ids
    assert "EASYEDA-PYDOCSTYLE-RATCHET" in ids
