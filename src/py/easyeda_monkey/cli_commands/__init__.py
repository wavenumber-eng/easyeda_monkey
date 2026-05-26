"""CLI subcommand registry."""

from __future__ import annotations

import argparse

from ..cli_command_types import CliCommandSpec
from . import fetch_part

COMMANDS: tuple[CliCommandSpec, ...] = (
    fetch_part.COMMAND,
)


def register_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register all public CLI subcommands with an argparse parser."""
    fetch_part.register(subparsers)
