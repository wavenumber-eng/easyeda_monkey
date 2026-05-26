"""L0-010: CLI fetch-part behavior."""

from __future__ import annotations

import json
from pathlib import Path

from easyeda_monkey.cli import main, normalize_lcsc_id

CASES_DIR = Path(__file__).parent / "cases" / "api_responses"


def test_normalize_lcsc_id_accepts_prefixed_and_scalar_ids() -> None:
    """The CLI accepts C-number spellings with or without a leading C."""
    assert normalize_lcsc_id("C21190") == "C21190"
    assert normalize_lcsc_id("21190") == "C21190"
    assert normalize_lcsc_id(" c21190 ") == "C21190"


def test_fetch_part_summary_uses_cached_fixture(tmp_path: Path) -> None:
    """fetch-part should emit a compact summary from a cache file."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    fixture = CASES_DIR / "C21190__resistor_0603_1k.json"
    (cache_dir / "C21190.json").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

    output = tmp_path / "C21190.summary.json"
    exit_code = main(
        [
            "fetch-part",
            "21190",
            "--cache-dir",
            str(cache_dir),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    summary = json.loads(output.read_text(encoding="utf-8"))
    assert summary["lcsc_id"] == "C21190"
    assert summary["found"] is True
    assert summary["symbol"]["shape_count"] > 0
    assert summary["footprint"]["shape_count"] > 0


def test_fetch_part_raw_uses_cached_fixture(tmp_path: Path) -> None:
    """fetch-part --raw should emit the cached API response."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    fixture = CASES_DIR / "C21190__resistor_0603_1k.json"
    (cache_dir / "C21190.json").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

    output = tmp_path / "C21190.raw.json"
    exit_code = main(
        [
            "fetch-part",
            "C21190",
            "--cache-dir",
            str(cache_dir),
            "--raw",
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    raw = json.loads(output.read_text(encoding="utf-8"))
    assert raw["success"] is True
    assert raw["result"]["lcsc"]["number"] == "C21190"
