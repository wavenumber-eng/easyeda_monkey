"""
EasyEDA schematic pin model.

Pin format: 7 segments joined by ``^^``, each segment has ``~``-separated fields.

Segment layout:
  0: Settings — show/hide, electrical type, spice number, x, y, rotation, id
  1: Pin dot — x, y (connection hotspot)
  2: Pin path — SVG path string, color
  3: Pin name — visible, x, y, rotation, text, anchor, fontFamily, fontSize
  4: Pin number — visible, x, y, rotation, text, anchor, fontFamily, fontSize
  5: Dot display — visible, circle_x, circle_y (active-low indicator)
  6: Clock — visible, path_string (clock edge indicator)

Single-class module by design.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .easyeda_types import safe_bool, safe_float, safe_str


@dataclass
class EasyEdaPin:
    """One pin on an EasyEDA schematic symbol."""

    # Settings (segment 0)
    show: bool = True
    electrical_type: str = "0"  # EePinType value
    spice_number: str = ""
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0
    id: str = ""

    # Pin dot (segment 1) — connection hotspot
    dot_x: float = 0.0
    dot_y: float = 0.0

    # Pin path (segment 2) — graphical stub
    path_string: str = ""
    path_color: str = ""

    # Pin name (segment 3)
    name_visible: bool = True
    name_x: float = 0.0
    name_y: float = 0.0
    name_rotation: float = 0.0
    name: str = ""
    name_anchor: str = ""
    name_font_family: str = ""
    name_font_size: str = ""

    # Pin number (segment 4)
    number_visible: bool = True
    number_x: float = 0.0
    number_y: float = 0.0
    number_rotation: float = 0.0
    number: str = ""
    number_anchor: str = ""
    number_font_family: str = ""
    number_font_size: str = ""

    # Dot display (segment 5) — active-low indicator circle
    dot_visible: bool = False
    dot_circle_x: float = 0.0
    dot_circle_y: float = 0.0

    # Clock indicator (segment 6)
    clock_visible: bool = False
    clock_path: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "show": self.show, "electrical_type": self.electrical_type,
            "spice_number": self.spice_number,
            "x": self.x, "y": self.y, "rotation": self.rotation, "id": self.id,
            "dot_x": self.dot_x, "dot_y": self.dot_y,
            "path_string": self.path_string, "path_color": self.path_color,
            "name_visible": self.name_visible, "name_x": self.name_x,
            "name_y": self.name_y, "name_rotation": self.name_rotation,
            "name": self.name, "name_anchor": self.name_anchor,
            "name_font_family": self.name_font_family,
            "name_font_size": self.name_font_size,
            "number_visible": self.number_visible, "number_x": self.number_x,
            "number_y": self.number_y, "number_rotation": self.number_rotation,
            "number": self.number, "number_anchor": self.number_anchor,
            "number_font_family": self.number_font_family,
            "number_font_size": self.number_font_size,
            "dot_visible": self.dot_visible, "dot_circle_x": self.dot_circle_x,
            "dot_circle_y": self.dot_circle_y,
            "clock_visible": self.clock_visible, "clock_path": self.clock_path,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EasyEdaPin:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})

    @classmethod
    def from_shape_string(cls, shape_str: str) -> EasyEdaPin:
        """Parse from the full pin shape string (after removing 'P~' prefix)."""
        segments = shape_str.split("^^")
        pin = cls()

        # Segment 0: settings
        if len(segments) > 0:
            f = segments[0].split("~")
            pin.show = safe_bool(f[0] if len(f) > 0 else "", True)
            pin.electrical_type = safe_str(f[1] if len(f) > 1 else "0") or "0"
            pin.spice_number = safe_str(f[2] if len(f) > 2 else "")
            pin.x = safe_float(f[3] if len(f) > 3 else 0)
            pin.y = safe_float(f[4] if len(f) > 4 else 0)
            pin.rotation = safe_float(f[5] if len(f) > 5 else 0)
            pin.id = safe_str(f[6] if len(f) > 6 else "")

        # Segment 1: pin dot
        if len(segments) > 1:
            f = segments[1].split("~")
            pin.dot_x = safe_float(f[0] if len(f) > 0 else 0)
            pin.dot_y = safe_float(f[1] if len(f) > 1 else 0)

        # Segment 2: pin path
        if len(segments) > 2:
            f = segments[2].split("~")
            pin.path_string = safe_str(f[0] if len(f) > 0 else "")
            pin.path_color = safe_str(f[1] if len(f) > 1 else "")

        # Segment 3: name
        if len(segments) > 3:
            f = segments[3].split("~")
            pin.name_visible = safe_bool(f[0] if len(f) > 0 else "1")
            pin.name_x = safe_float(f[1] if len(f) > 1 else 0)
            pin.name_y = safe_float(f[2] if len(f) > 2 else 0)
            pin.name_rotation = safe_float(f[3] if len(f) > 3 else 0)
            pin.name = safe_str(f[4] if len(f) > 4 else "")
            pin.name_anchor = safe_str(f[5] if len(f) > 5 else "")
            pin.name_font_family = safe_str(f[6] if len(f) > 6 else "")
            pin.name_font_size = safe_str(f[7] if len(f) > 7 else "")

        # Segment 4: number
        if len(segments) > 4:
            f = segments[4].split("~")
            pin.number_visible = safe_bool(f[0] if len(f) > 0 else "1")
            pin.number_x = safe_float(f[1] if len(f) > 1 else 0)
            pin.number_y = safe_float(f[2] if len(f) > 2 else 0)
            pin.number_rotation = safe_float(f[3] if len(f) > 3 else 0)
            pin.number = safe_str(f[4] if len(f) > 4 else "")
            pin.number_anchor = safe_str(f[5] if len(f) > 5 else "")
            pin.number_font_family = safe_str(f[6] if len(f) > 6 else "")
            pin.number_font_size = safe_str(f[7] if len(f) > 7 else "")

        # Segment 5: dot display (active low)
        if len(segments) > 5:
            f = segments[5].split("~")
            pin.dot_visible = safe_bool(f[0] if len(f) > 0 else "0")
            pin.dot_circle_x = safe_float(f[1] if len(f) > 1 else 0)
            pin.dot_circle_y = safe_float(f[2] if len(f) > 2 else 0)

        # Segment 6: clock
        if len(segments) > 6:
            f = segments[6].split("~")
            pin.clock_visible = safe_bool(f[0] if len(f) > 0 else "0")
            pin.clock_path = safe_str(f[1] if len(f) > 1 else "")

        return pin
