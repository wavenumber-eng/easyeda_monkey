"""
L0-002: EasyEdaSymbol JSON round-trip.

Parse from API fixture → to_json → from_json → compare.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from easyeda_monkey.easyeda_symbol import EasyEdaSymbol

CASES_DIR = Path(__file__).parent / "cases" / "api_responses"


def _fixture_files() -> list[Path]:
    if not CASES_DIR.exists():
        return []
    return sorted(CASES_DIR.glob("*.json"))


@pytest.mark.parametrize("fixture_path", _fixture_files(), ids=lambda p: p.stem)
def test_symbol_json_roundtrip(fixture_path: Path):
    """Parse → to_json → from_json → to_json should produce identical output."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    sym1 = EasyEdaSymbol.from_json(data)
    json1 = sym1.to_json()

    # Round-trip through JSON string
    json_str = json.dumps(json1)
    json2_raw = json.loads(json_str)
    sym2 = EasyEdaSymbol.from_json(json2_raw)
    json2 = sym2.to_json()

    assert json1 == json2, (
        f"Round-trip mismatch for {fixture_path.name}: "
        f"pin counts {len(sym1.pins)} vs {len(sym2.pins)}"
    )


@pytest.mark.parametrize("fixture_path", _fixture_files(), ids=lambda p: p.stem)
def test_symbol_preserves_pin_count(fixture_path: Path):
    """Pin count should be identical after round-trip."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    sym1 = EasyEdaSymbol.from_json(data)
    sym2 = EasyEdaSymbol.from_json(sym1.to_json())
    assert len(sym1.pins) == len(sym2.pins)


@pytest.mark.parametrize("fixture_path", _fixture_files(), ids=lambda p: p.stem)
def test_symbol_preserves_graphic_counts(fixture_path: Path):
    """Graphic element counts should be identical after round-trip."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    sym1 = EasyEdaSymbol.from_json(data)
    sym2 = EasyEdaSymbol.from_json(sym1.to_json())

    assert len(sym1.rectangles) == len(sym2.rectangles)
    assert len(sym1.circles) == len(sym2.circles)
    assert len(sym1.ellipses) == len(sym2.ellipses)
    assert len(sym1.arcs) == len(sym2.arcs)
    assert len(sym1.polylines) == len(sym2.polylines)
    assert len(sym1.polygons) == len(sym2.polygons)
    assert len(sym1.paths) == len(sym2.paths)
