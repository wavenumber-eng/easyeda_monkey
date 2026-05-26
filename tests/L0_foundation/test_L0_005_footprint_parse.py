"""
L0-005: Parse saved API fixtures into EasyEdaFootprint objects.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from easyeda_monkey.easyeda_footprint import EasyEdaFootprint

CASES_DIR = Path(__file__).parent / "cases" / "api_responses"


def _fixture_files() -> list[Path]:
    if not CASES_DIR.exists():
        return []
    return sorted(CASES_DIR.glob("*.json"))


def _load_footprint(filename: str) -> EasyEdaFootprint:
    data = json.loads((CASES_DIR / filename).read_text(encoding="utf-8"))
    return EasyEdaFootprint.from_json(data)


@pytest.mark.parametrize("fixture_path", _fixture_files(), ids=lambda p: p.stem)
def test_all_fixtures_parse_footprint(fixture_path: Path):
    """Every API fixture should parse into a valid EasyEdaFootprint."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    fp = EasyEdaFootprint.from_json(data)
    # Every component should have at least one pad
    assert len(fp.pads) >= 1, f"No pads in {fixture_path.name}"


def test_resistor_footprint():
    """C21190 (0603 resistor) — 2 pads, SMD."""
    data = json.loads((CASES_DIR / "C21190__resistor_0603_1k.json").read_text(encoding="utf-8"))
    fp = EasyEdaFootprint.from_json(data)
    assert len(fp.pads) == 2
    # Pads should have numbers
    numbers = sorted(p.number for p in fp.pads)
    assert "1" in numbers
    assert "2" in numbers


def test_mcu_footprint():
    """C2040 (RP2040 QFN-56) — many pads."""
    data = json.loads((CASES_DIR / "C2040__mcu_rp2040.json").read_text(encoding="utf-8"))
    fp = EasyEdaFootprint.from_json(data)
    assert len(fp.pads) >= 30  # QFN-56 has 57 pads (56 + exposed pad)


def test_power_step_footprint():
    """C80192 (POWERSTEP01) dense VFQFPN footprint."""
    data = json.loads(
        (CASES_DIR / "C80192__power_step_powerstep01.json").read_text(encoding="utf-8")
    )
    fp = EasyEdaFootprint.from_json(data)
    assert len(fp.pads) == 102
    assert len(fp.tracks) >= 30
    assert len(fp.polylines) >= 100


def test_transistor_footprint():
    """C57668 (BC847B,215) SOT-23 footprint."""
    data = json.loads(
        (CASES_DIR / "C57668__transistor_bc847b_215.json").read_text(encoding="utf-8")
    )
    fp = EasyEdaFootprint.from_json(data)
    assert len(fp.pads) == 3
    assert len(fp.tracks) == 3
    assert len(fp.polylines) >= 5


def test_oled_footprint():
    """C2890616 OLED footprint with arcs, rectangle, and mixed graphics."""
    fp = _load_footprint("C2890616__oled_n096_1608tbbig11_h13.json")

    assert len(fp.pads) == 13
    assert len(fp.tracks) == 10
    assert len(fp.circles) == 1
    assert len(fp.arcs) == 3
    assert len(fp.rectangles) == 1
    assert len(fp.polylines) == 18
    assert len(fp.texts) == 2


def test_led_matrix_footprint_circles():
    """C53078 LED matrix footprint with many circular silkscreen graphics."""
    fp = _load_footprint("C53078__led_matrix_fj2088bh.json")

    assert len(fp.pads) == 16
    assert len(fp.tracks) == 4
    assert len(fp.circles) == 81
    assert len(fp.polylines) == 1
    assert len(fp.texts) == 4


def test_rj45_footprint_through_hole_and_slots():
    """C7501824 RJ45 through-hole footprint with slotted mounting pads."""
    fp = _load_footprint("C7501824__rj45_hc_wk88_h16_db.json")
    slotted_pads = [pad for pad in fp.pads if pad.hole_length > 0]

    assert len(fp.pads) == 14
    assert len(fp.tracks) == 6
    assert len(fp.holes) == 2
    assert {pad.layer_id for pad in fp.pads} == {"11"}
    assert sum(1 for pad in fp.pads if pad.hole_radius > 0) == 14
    assert [pad.number for pad in slotted_pads] == ["10", "9"]


def test_usb_connector_footprint_slotted_mounts():
    """C963370 USB footprint with slotted through-hole mounting pads."""
    fp = _load_footprint("C963370__usb_gt_usb_7010an.json")
    slotted_pads = [pad for pad in fp.pads if pad.hole_length > 0]

    assert len(fp.pads) == 16
    assert len(fp.tracks) == 3
    assert len(fp.circles) == 4
    assert len(fp.polylines) == 33
    assert len(fp.holes) == 2
    assert {pad.number for pad in slotted_pads} == {"13", "14", "15", "16"}


def test_led_segment_through_hole_footprint():
    """C132660 through-hole LED segment footprint with rich silkscreen."""
    fp = _load_footprint("C132660__led_segment_sr410361n.json")

    assert len(fp.pads) == 12
    assert len(fp.tracks) == 32
    assert len(fp.circles) == 17
    assert len(fp.polylines) == 29
    assert {pad.shape for pad in fp.pads} == {"ELLIPSE"}
    assert {pad.layer_id for pad in fp.pads} == {"11"}
    assert sum(1 for pad in fp.pads if pad.hole_radius > 0) == 12


def test_pled18s_footprint_graphics():
    """C42413366 two-pad footprint with internal graphics coverage."""
    fp = _load_footprint("C42413366__pled18s_internal_graphics.json")

    assert len(fp.pads) == 2
    assert len(fp.tracks) == 5
    assert len(fp.circles) == 1
    assert len(fp.polylines) == 5


def test_sd_socket_footprint_arcs_and_non_pad_holes():
    """C266603 SD socket footprint with arcs and non-pad holes."""
    fp = _load_footprint("C266603__sd_socket_sd_106m.json")

    assert len(fp.pads) == 13
    assert len(fp.tracks) == 7
    assert len(fp.circles) == 3
    assert len(fp.arcs) == 5
    assert len(fp.polylines) == 14
    assert len(fp.holes) == 2
    assert {pad.shape for pad in fp.pads} == {"RECT"}
    assert {pad.layer_id for pad in fp.pads} == {"1"}
    assert all(pad.hole_radius == 0 for pad in fp.pads)
    assert [hole.diameter for hole in fp.holes] == [2.9528, 2.9528]


def test_esp32_castellated_module_footprint():
    """C701343 castellated ESP32 module footprint."""
    fp = _load_footprint("C701343__esp32_wroom_32e_castellated.json")
    duplicate_ground_pads = [pad for pad in fp.pads if pad.number == "39"]

    assert len(fp.pads) == 47
    assert len(fp.tracks) == 8
    assert len(fp.circles) == 2
    assert len(fp.polylines) == 48
    assert {pad.shape for pad in fp.pads} == {"RECT"}
    assert {pad.layer_id for pad in fp.pads} == {"1"}
    assert len(duplicate_ground_pads) == 9
    assert all(pad.hole_radius == 0 for pad in fp.pads)


def test_lm317_through_hole_regulator_footprint():
    """C7463411 through-hole regulator with oval pads and round holes."""
    fp = _load_footprint("C7463411__lm317_to220_through_hole.json")

    assert len(fp.pads) == 3
    assert len(fp.tracks) == 2
    assert len(fp.circles) == 2
    assert len(fp.polylines) == 5
    assert {pad.shape for pad in fp.pads} == {"RECT", "OVAL"}
    assert {pad.layer_id for pad in fp.pads} == {"11"}
    assert [pad.number for pad in fp.pads] == ["1", "3", "2"]
    assert all(pad.hole_radius == 2.4606 for pad in fp.pads)
    assert all(pad.hole_length == 0 for pad in fp.pads)
    assert len(fp.holes) == 0


def test_smt_pogo_single_pad_footprint():
    """C5203974 single-pad SMT pogo footprint."""
    fp = _load_footprint("C5203974__smt_pogo_yz110615028f_01.json")

    assert len(fp.pads) == 1
    assert len(fp.tracks) == 1
    assert len(fp.circles) == 1
    assert len(fp.polylines) == 3
    assert fp.pads[0].number == "1"
    assert fp.pads[0].shape == "RECT"
    assert fp.pads[0].layer_id == "1"
    assert fp.pads[0].hole_radius == 0
    assert len(fp.holes) == 0


def test_through_hole_pogo_single_pad_footprint():
    """C7471747 single-pad through-hole pogo footprint."""
    fp = _load_footprint("C7471747__through_hole_pogo_yzp0436_30165_01.json")

    assert len(fp.pads) == 1
    assert len(fp.circles) == 1
    assert fp.pads[0].number == "1"
    assert fp.pads[0].shape == "ELLIPSE"
    assert fp.pads[0].layer_id == "11"
    assert fp.pads[0].hole_radius == 1.9685
    assert fp.pads[0].hole_length == 0
    assert len(fp.holes) == 0


def test_footprint_has_silkscreen():
    """Footprints should have at least some silkscreen (tracks or circles)."""
    data = json.loads((CASES_DIR / "C21190__resistor_0603_1k.json").read_text(encoding="utf-8"))
    fp = EasyEdaFootprint.from_json(data)
    total_gfx = len(fp.tracks) + len(fp.circles) + len(fp.arcs) + len(fp.rectangles) + len(fp.polylines)
    assert total_gfx >= 1, "Footprint has no silkscreen/graphics"


@pytest.mark.parametrize("fixture_path", _fixture_files(), ids=lambda p: p.stem)
def test_footprint_json_roundtrip(fixture_path: Path):
    """Parse → to_json → from_json → to_json should match."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    fp1 = EasyEdaFootprint.from_json(data)
    json1 = fp1.to_json()
    fp2 = EasyEdaFootprint.from_json(json1)
    json2 = fp2.to_json()
    assert json1 == json2
