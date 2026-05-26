"""Top-level command-line orchestrator for EasyEDA Monkey."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
from typing import cast

from . import __version__
from .cli_commands import COMMANDS as CLI_COMMANDS
from .cli_commands import register_commands
from .cli_commands.fetch_part import normalize_lcsc_id

__all__ = ["CLI_COMMANDS", "build_parser", "main", "normalize_lcsc_id"]


def build_parser() -> argparse.ArgumentParser:
    """Build the EasyEDA Monkey argument parser."""
    parser = argparse.ArgumentParser(
        prog="easyeda-monkey",
        description="EasyEDA / LCSC parsing utilities.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    register_commands(subparsers)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the EasyEDA Monkey CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help(sys.stderr)
        return 2
    return cast("CommandHandler", handler)(args)


CommandHandler = Callable[[argparse.Namespace], int]


if __name__ == "__main__":
    raise SystemExit(main())
