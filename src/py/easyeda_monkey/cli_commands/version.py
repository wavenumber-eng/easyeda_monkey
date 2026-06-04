"""Implementation of the version command."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from importlib import metadata
from typing import Literal, cast

from easyeda_monkey import __version__
from easyeda_monkey.cli_command_types import CliCommandSpec

COMMAND = CliCommandSpec(
    name="version",
    design_doc="cli/version.html",
    help="Print version information.",
)


def register(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register the command with the root parser."""
    parser = subparsers.add_parser(
        COMMAND.name,
        help=COMMAND.help,
        description="Print easyeda-monkey and major dependency versions.",
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    parser.set_defaults(handler=run)


def run(args: argparse.Namespace) -> int:
    """Run the command."""
    output_format = _output_format(args)
    if output_format == "json":
        print(json.dumps(version_report(), indent=2, sort_keys=True))
        return 0
    return run_text()


def run_text() -> int:
    """Print the default text version report."""
    report = version_report()
    print(f"easyeda-monkey {report['easyeda-monkey']}")
    print(f"python {report['python']}")
    print(f"requests {report['requests']}")
    return 0


def version_report() -> dict[str, str]:
    """Return version data for the package and major runtime dependencies."""
    return {
        "easyeda-monkey": __version__,
        "python": f"{platform.python_implementation()} {sys.version.split()[0]}",
        "requests": _package_version("requests"),
    }


def _package_version(distribution: str) -> str:
    """Return the installed package version for a distribution."""
    try:
        return metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return "not installed"


def _output_format(args: argparse.Namespace) -> Literal["text", "json"]:
    """Return the normalized output format."""
    value = cast(str, args.output_format)
    if value in ("text", "json"):
        return value
    raise TypeError("expected output_format to be text or json")
