"""Implementation of the fetch-part CLI subcommand."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import cast

from ..cli_command_types import CliCommandSpec
from ..easyeda_api import EasyEdaApiClient

JsonScalar = str | int | float | bool | None
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject = dict[str, JsonValue]

COMMAND = CliCommandSpec(
    name="fetch-part",
    design_doc="cli/fetch-part.html",
    help="Fetch an EasyEDA / LCSC component by C-number.",
)


def register(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register the fetch-part parser."""
    parser = subparsers.add_parser(
        COMMAND.name,
        help=COMMAND.help,
        description="Fetch an EasyEDA / LCSC component by C-number.",
    )
    parser.add_argument("lcsc_id", help="LCSC part number, such as C21190 or 21190.")
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Optional directory for cached API JSON responses.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output JSON file. Defaults to stdout.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Emit the raw EasyEDA API response instead of the compact summary.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="HTTP timeout in seconds when a network fetch is needed.",
    )
    parser.add_argument(
        "--rate-limit-seconds",
        type=float,
        default=0.5,
        help="Minimum delay between live API requests for this process.",
    )
    parser.set_defaults(handler=run)


def normalize_lcsc_id(value: str) -> str:
    """Normalize a user supplied LCSC C-number."""
    lcsc_id = value.strip().upper()
    if not lcsc_id:
        raise ValueError("LCSC id cannot be empty")
    if not lcsc_id.startswith("C"):
        lcsc_id = f"C{lcsc_id}"
    return lcsc_id


def summarize_component(component_data: Mapping[str, JsonValue], lcsc_id: str) -> JsonObject:
    """Build a compact summary for an EasyEDA component API response."""
    result = component_data.get("result")
    if not isinstance(result, dict):
        return {
            "lcsc_id": lcsc_id,
            "found": False,
            "title": "",
            "symbol": {"shape_count": 0},
            "footprint": {"shape_count": 0},
        }

    data_str = _dict_or_empty(result.get("dataStr"))
    symbol_shapes = _list_or_empty(data_str.get("shape"))

    package_detail = _dict_or_empty(result.get("packageDetail"))
    footprint_data = _dict_or_empty(package_detail.get("dataStr"))
    footprint_shapes = _list_or_empty(footprint_data.get("shape"))

    return {
        "lcsc_id": _lcsc_id_from_result(result, default=lcsc_id),
        "found": True,
        "title": _str_or_empty(result.get("title")),
        "uuid": _str_or_empty(result.get("uuid")),
        "symbol": {
            "shape_count": len(symbol_shapes),
            "has_data": bool(symbol_shapes),
        },
        "footprint": {
            "shape_count": len(footprint_shapes),
            "has_data": bool(footprint_shapes),
        },
    }


def run(args: argparse.Namespace) -> int:
    """Run the fetch-part subcommand."""
    try:
        lcsc_id = normalize_lcsc_id(args.lcsc_id)
    except ValueError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2

    client = EasyEdaApiClient(
        cache_dir=args.cache_dir,
        timeout=args.timeout,
        rate_limit_seconds=args.rate_limit_seconds,
    )
    component_data = cast(JsonObject, client.fetch_component(lcsc_id))
    if not component_data:
        sys.stderr.write(f"error: no EasyEDA component data found for {lcsc_id}\n")
        return 1

    payload = component_data if args.raw else summarize_component(component_data, lcsc_id)
    _emit_json(payload, args.output)
    return 0


def _dict_or_empty(value: JsonValue | object) -> Mapping[str, JsonValue]:
    """Return a JSON object view when value is a dictionary."""
    if isinstance(value, dict):
        return cast(Mapping[str, JsonValue], value)
    return {}


def _list_or_empty(value: JsonValue | object) -> list[JsonValue]:
    """Return a JSON list when value is a list."""
    if isinstance(value, list):
        return cast(list[JsonValue], value)
    return []


def _str_or_empty(value: JsonValue | object) -> str:
    """Return a string value or an empty string."""
    return value if isinstance(value, str) else ""


def _lcsc_id_from_result(result: Mapping[str, JsonValue], *, default: str) -> str:
    """Extract the LCSC C-number from a result object."""
    lcsc = _dict_or_empty(result.get("lcsc"))
    szlcsc = _dict_or_empty(result.get("szlcsc"))
    return _str_or_empty(lcsc.get("number")) or _str_or_empty(szlcsc.get("number")) or default


def _emit_json(payload: JsonObject, output: Path | None) -> None:
    """Write JSON to stdout or an output file."""
    text = json.dumps(payload, indent=2, sort_keys=True)
    if output is None:
        sys.stdout.write(text)
        sys.stdout.write("\n")
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text + "\n", encoding="utf-8")
