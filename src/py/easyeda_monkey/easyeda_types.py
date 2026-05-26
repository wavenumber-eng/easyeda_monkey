"""
Shared enums, constants, and coordinate helpers for EasyEDA parsing.

Single-module by design — no external dependencies.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

# EasyEDA schematic uses pixel units. 1 pixel = 10 mils = 0.254 mm.
# PCB uses 10-mil units (same as Altium internal units).
# 1 mil = 25,400 nm.  10 mils = 254,000 nm.
EE_SCH_PIXEL_TO_NM = 254_000  # 1 EasyEDA sch pixel = 10 mils = 254,000 nm
EE_PCB_UNIT_TO_NM = 254_000   # 1 EasyEDA PCB unit = 10 mils = 254,000 nm
NM_PER_MIL = 25_400
NM_PER_MM = 1_000_000


class EePinType(Enum):
    """EasyEDA pin electrical type."""
    UNSPECIFIED = "0"
    INPUT = "1"
    OUTPUT = "2"
    BIDIRECTIONAL = "3"
    POWER = "4"


class EeStrokeStyle(Enum):
    """EasyEDA stroke/line style."""
    SOLID = "0"
    DASHED = "1"
    DOTTED = "2"


def safe_float(value: Any, default: float = 0.0) -> float:
    """Convert to float, returning default for empty/invalid values."""
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """Convert to int, returning default for empty/invalid values."""
    if value is None or value == "":
        return default
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


def safe_str(value: Any, default: str = "") -> str:
    """Convert to str, returning default for None."""
    if value is None:
        return default
    return str(value)


def safe_bool(value: Any, default: bool = False) -> bool:
    """Convert to bool — handles '0'/'1', '', 'true'/'false'."""
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return value
    s = str(value).strip().lower()
    return s in ("1", "true", "yes", "show")
