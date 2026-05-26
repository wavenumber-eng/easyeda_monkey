"""
L0-001: Parse saved API fixtures into EasyEdaSymbol objects.

Verifies correct pin count, graphic element counts, and metadata
for each test fixture component.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from easyeda_monkey.easyeda_symbol import EasyEdaSymbol

CASES_DIR = Path(__file__).parent / "cases" / "api_responses"


def _load_fixture(filename: str) -> dict:
    path = CASES_DIR / filename
    assert path.exists(), f"Fixture not found: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def _fixture_files() -> list[Path]:
    if not CASES_DIR.exists():
        return []
    return sorted(CASES_DIR.glob("*.json"))


# ── Parametric: every fixture parses without error ────────────────────


@pytest.mark.parametrize("fixture_path", _fixture_files(), ids=lambda p: p.stem)
def test_all_fixtures_parse(fixture_path: Path):
    """Every API fixture should parse into a valid EasyEdaSymbol."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    sym = EasyEdaSymbol.from_json(data)
    assert sym.info.name != "" or sym.info.lcsc_id != "", (
        f"Symbol from {fixture_path.name} has no name or LCSC ID"
    )


# ── Specific fixture tests ────────────────────────────────────────────


def test_resistor_c21190():
    """C21190 (0603 1k resistor) — simple 2-pin passive."""
    data = _load_fixture("C21190__resistor_0603_1k.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C21190"
    assert len(sym.pins) == 2
    # Should have at least one rectangle (body)
    assert len(sym.rectangles) >= 1 or len(sym.polylines) >= 1


def test_mcu_c2040():
    """C2040 (RP2040) — multi-pin IC."""
    data = _load_fixture("C2040__mcu_rp2040.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C2040"
    assert sym.info.name == "RP2040"
    # RP2040 has 56 pins (QFN-56)
    assert len(sym.pins) >= 30  # at least most pins parsed


def test_opamp_c7950():
    """C7950 (LM358) — dual op-amp."""
    data = _load_fixture("C7950__opamp_lm358.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C7950"
    assert len(sym.pins) >= 5  # at least 5 pins for a dual opamp


def test_power_step_c80192():
    """C80192 (POWERSTEP01) large power-step motor driver."""
    data = _load_fixture("C80192__power_step_powerstep01.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C80192"
    assert sym.info.name == "POWERSTEP01"
    assert len(sym.pins) == 98
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 1


def test_transistor_c57668():
    """C57668 (BC847B,215) transistor symbol with line/polygon geometry."""
    data = _load_fixture("C57668__transistor_bc847b_215.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C57668"
    assert sym.info.name == "BC847B,215"
    assert len(sym.pins) == 3
    assert len(sym.polylines) == 3
    assert len(sym.polygons) == 1


def test_oled_c2890616():
    """C2890616 OLED display symbol."""
    data = _load_fixture("C2890616__oled_n096_1608tbbig11_h13.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C2890616"
    assert sym.info.name == "N096-1608TBBIG11-H13"
    assert len(sym.pins) == 13
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 1


def test_led_matrix_c53078():
    """C53078 LED matrix symbol with many repeated ellipses."""
    data = _load_fixture("C53078__led_matrix_fj2088bh.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C53078"
    assert sym.info.name == "LED FJ2088BH"
    assert len(sym.pins) == 16
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 64


def test_rj45_c7501824():
    """C7501824 RJ45 symbol with rectangle and interior line graphics."""
    data = _load_fixture("C7501824__rj45_hc_wk88_h16_db.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C7501824"
    assert sym.info.name == "HC-WK88-H16-DB"
    assert len(sym.pins) == 14
    assert len(sym.rectangles) == 1
    assert len(sym.polylines) == 9


def test_usb_connector_c963370():
    """C963370 USB connector symbol."""
    data = _load_fixture("C963370__usb_gt_usb_7010an.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C963370"
    assert sym.info.name == "GT-USB-7010AN"
    assert len(sym.pins) == 16
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 1


def test_led_segment_c132660():
    """C132660 through-hole LED segment symbol with line graphics."""
    data = _load_fixture("C132660__led_segment_sr410361n.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C132660"
    assert sym.info.name == "SR410361N"
    assert len(sym.pins) == 12
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 4
    assert len(sym.polylines) == 8


def test_pled18s_c42413366():
    """C42413366 protection diode symbol with internal line/path graphics."""
    data = _load_fixture("C42413366__pled18s_internal_graphics.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C42413366"
    assert sym.info.name == "PLED18S_C42413366"
    assert len(sym.pins) == 2
    assert len(sym.rectangles) == 1
    assert len(sym.polylines) == 12
    assert len(sym.paths) == 2


def test_sd_socket_c266603():
    """C266603 SD socket symbol."""
    data = _load_fixture("C266603__sd_socket_sd_106m.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C266603"
    assert sym.info.name == "SD-106M"
    assert len(sym.pins) == 13
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 1


def test_esp32_castellated_module_c701343():
    """C701343 ESP32 castellated module symbol."""
    data = _load_fixture("C701343__esp32_wroom_32e_castellated.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C701343"
    assert sym.info.name == "ESP32-WROOM-32E(16MB)"
    assert len(sym.pins) == 39
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 1


def test_lm317_through_hole_c7463411():
    """C7463411 standard through-hole regulator symbol."""
    data = _load_fixture("C7463411__lm317_to220_through_hole.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C7463411"
    assert sym.info.name == "LM317_C7463411"
    assert len(sym.pins) == 3
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 1


def test_smt_pogo_c5203974():
    """C5203974 single-pin SMT pogo symbol."""
    data = _load_fixture("C5203974__smt_pogo_yz110615028f_01.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C5203974"
    assert sym.info.name == "YZ110615028F-01"
    assert len(sym.pins) == 1
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 1


def test_through_hole_pogo_c7471747():
    """C7471747 single-pin through-hole pogo symbol."""
    data = _load_fixture("C7471747__through_hole_pogo_yzp0436_30165_01.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.lcsc_id == "C7471747"
    assert sym.info.name == "YZP0436-30165-01"
    assert len(sym.pins) == 1
    assert len(sym.rectangles) == 1
    assert len(sym.ellipses) == 1


def test_symbol_has_info():
    """Symbol info should be populated from API response."""
    data = _load_fixture("C21190__resistor_0603_1k.json")
    sym = EasyEdaSymbol.from_json(data)

    assert sym.info.name != ""
    assert sym.info.lcsc_id == "C21190"


def test_symbol_pin_has_name_and_number():
    """Pins should have parsed name and number."""
    data = _load_fixture("C21190__resistor_0603_1k.json")
    sym = EasyEdaSymbol.from_json(data)

    for pin in sym.pins:
        # At minimum, number should be present (name may be empty for passives)
        assert pin.number != "" or pin.name != "", (
            f"Pin {pin.id} has neither name nor number"
        )
