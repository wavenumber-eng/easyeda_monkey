"""Implementation of the download-part CLI subcommand."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from ..cli_command_types import CliCommandSpec
from ..easyeda_3d_model import EasyEda3DModel, extract_3d_models_from_api_response
from ..easyeda_api import EasyEdaApiClient
from .fetch_part import JsonObject, JsonValue, normalize_lcsc_id, summarize_component

COMMAND = CliCommandSpec(
    name="download-part",
    design_doc="cli/download-part.html",
    help="Download an EasyEDA / LCSC component bundle by C-number.",
)

MODEL_FORMATS = ("step", "obj", "both", "none")


def register(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    """Register the download-part parser."""
    parser = subparsers.add_parser(
        COMMAND.name,
        help=COMMAND.help,
        description=(
            "Fetch an EasyEDA / LCSC component and write raw JSON, summary JSON, "
            "3D model metadata, and requested 3D model files."
        ),
    )
    parser.add_argument("lcsc_id", help="LCSC part number, such as C21190 or 21190.")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Output root directory. The command writes into <output-dir>/<LCSC_ID>/.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=None,
        help="Optional directory for cached API JSON responses.",
    )
    parser.add_argument(
        "--model-format",
        choices=MODEL_FORMATS,
        default="both",
        help="3D model format to download. Defaults to both STEP and OBJ.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP timeout in seconds for live API and model requests.",
    )
    parser.add_argument(
        "--rate-limit-seconds",
        type=float,
        default=0.5,
        help="Minimum delay between live API requests for this process.",
    )
    parser.set_defaults(handler=run)


def run(args: argparse.Namespace) -> int:
    """Run the download-part subcommand."""
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

    bundle_dir = args.output_dir / lcsc_id
    bundle_dir.mkdir(parents=True, exist_ok=True)
    report = _write_component_bundle(
        lcsc_id=lcsc_id,
        component_data=component_data,
        bundle_dir=bundle_dir,
        model_format=args.model_format,
        timeout=args.timeout,
    )
    return 0 if report["success"] else 1


def _write_component_bundle(
    *,
    lcsc_id: str,
    component_data: JsonObject,
    bundle_dir: Path,
    model_format: str,
    timeout: int,
) -> JsonObject:
    """Write component JSON, summary JSON, model metadata, and model files."""
    raw_path = bundle_dir / "easyeda-api.json"
    summary_path = bundle_dir / "summary.json"
    models_path = bundle_dir / "3d-models.json"
    report_path = bundle_dir / "download-report.json"

    models = extract_3d_models_from_api_response(dict(component_data))
    downloads = _download_models(
        models=models,
        models_dir=bundle_dir / "models",
        model_format=model_format,
        timeout=timeout,
    )
    success = all(bool(download["success"]) for download in downloads)

    _write_json(raw_path, component_data)
    _write_json(summary_path, summarize_component(component_data, lcsc_id))
    _write_json(models_path, {"models": [model.to_json() for model in models]})

    report: JsonObject = {
        "lcsc_id": lcsc_id,
        "success": success,
        "output_dir": bundle_dir.as_posix(),
        "raw_json": raw_path.as_posix(),
        "summary_json": summary_path.as_posix(),
        "models_json": models_path.as_posix(),
        "model_count": len(models),
        "model_format": model_format,
        "downloads": cast(JsonValue, downloads),
    }
    _write_json(report_path, report)
    return report


def _download_models(
    *,
    models: list[EasyEda3DModel],
    models_dir: Path,
    model_format: str,
    timeout: int,
) -> list[JsonObject]:
    """Download all requested 3D model files and return report entries."""
    formats = _requested_formats(model_format)
    downloads: list[JsonObject] = []
    for model in models:
        for format_name in formats:
            output_path = models_dir / f"{model.uuid}.{format_name}"
            downloads.append(
                _download_one_model(
                    model=model,
                    format_name=format_name,
                    output_path=output_path,
                    timeout=timeout,
                )
            )
    return downloads


def _requested_formats(model_format: str) -> tuple[str, ...]:
    """Expand the user-facing model format option into concrete file formats."""
    if model_format == "both":
        return ("step", "obj")
    if model_format == "none":
        return ()
    return (model_format,)


def _download_one_model(
    *,
    model: EasyEda3DModel,
    format_name: str,
    output_path: Path,
    timeout: int,
) -> JsonObject:
    """Download one model file and return a machine-readable report entry."""
    if format_name == "step":
        success = model.download_step(output_path, timeout=timeout)
        url = model.step_url
    else:
        success = model.download_obj(output_path, timeout=timeout)
        url = model.obj_url

    return {
        "uuid": model.uuid,
        "format": format_name,
        "url": url,
        "path": output_path.as_posix(),
        "success": success,
    }


def _write_json(path: Path, payload: JsonValue) -> None:
    """Write a JSON payload to disk with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
