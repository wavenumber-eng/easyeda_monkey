"""Design documentation signoff tests."""

from __future__ import annotations

from pathlib import Path

from easyeda_monkey.cli import CLI_COMMANDS


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


PACKAGE_ROOT = _project_root()
DESIGN_ROOT = PACKAGE_ROOT / "docs" / "design"


def test_design_entry_points_exist() -> None:
    """Verify that the master design docs entry points exist."""
    assert (DESIGN_ROOT / "index.html").exists()
    assert (DESIGN_ROOT / "styles.css").exists()
    assert (DESIGN_ROOT / "cli" / "index.html").exists()


def test_cli_commands_have_matching_design_docs() -> None:
    """Verify that every registered CLI command has a matching design document."""
    cli_index = (DESIGN_ROOT / "cli" / "index.html").read_text(encoding="utf-8")

    for command in CLI_COMMANDS:
        design_doc = DESIGN_ROOT / command.design_doc
        assert design_doc.exists(), f"Missing design doc for {command.name}: {design_doc}"
        assert f'data-command="{command.name}"' in cli_index
        assert command.design_doc in cli_index

        text = design_doc.read_text(encoding="utf-8")
        assert f'data-command="{command.name}"' in text
        assert '<section id="usage">' in text
        assert '<section id="arguments">' in text
        assert '<section id="output">' in text
        assert '<section id="tests">' in text


def test_cli_commands_have_dedicated_modules() -> None:
    """Verify that public CLI commands do not live in the orchestrator module."""
    orchestrator_text = (PACKAGE_ROOT / "src" / "py" / "easyeda_monkey" / "cli.py").read_text(
        encoding="utf-8"
    )
    assert ".add_parser(" not in orchestrator_text
    assert ".set_defaults(handler=" not in orchestrator_text

    commands_root = PACKAGE_ROOT / "src" / "py" / "easyeda_monkey" / "cli_commands"
    for command in CLI_COMMANDS:
        module_name = command.name.replace("-", "_")
        module_path = commands_root / f"{module_name}.py"
        assert module_path.exists(), f"Missing CLI command module for {command.name}: {module_path}"


def test_cli_config_contracts_are_declared() -> None:
    """Verify that each command doc declares whether it has a config contract."""
    for command in CLI_COMMANDS:
        text = (DESIGN_ROOT / command.design_doc).read_text(encoding="utf-8")
        assert 'data-config-contract="' in text
