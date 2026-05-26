"""
EasyEDA PCB pad model.

Pad format: PAD~shape~x~y~width~height~layerId~net~number~holeRadius~points~rotation~id~holeLength~holePoints~plated~...

Single-class module by design.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .easyeda_types import safe_float, safe_str


@dataclass
class EeFootprintPad:
    """One pad on an EasyEDA PCB footprint."""

    shape: str = ""        # ELLIPSE, RECT, OVAL, POLYGON
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    layer_id: str = ""
    net: str = ""
    number: str = ""
    hole_radius: float = 0.0
    points_str: str = ""   # outline points for polygon/oval pads
    rotation: float = 0.0
    id: str = ""
    hole_length: float = 0.0
    hole_points_str: str = ""
    plated: str = ""       # "Y" or "N"

    @property
    def is_plated(self) -> bool:
        return self.plated.upper() == "Y"

    @property
    def is_through_hole(self) -> bool:
        return self.hole_radius > 0

    def to_json(self) -> dict[str, Any]:
        return {
            "shape": self.shape, "x": self.x, "y": self.y,
            "width": self.width, "height": self.height,
            "layer_id": self.layer_id, "net": self.net, "number": self.number,
            "hole_radius": self.hole_radius, "points_str": self.points_str,
            "rotation": self.rotation, "id": self.id,
            "hole_length": self.hole_length, "hole_points_str": self.hole_points_str,
            "plated": self.plated,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeFootprintPad:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})

    @classmethod
    def from_fields(cls, fields: list[str]) -> EeFootprintPad:
        """Parse from PAD tilde-delimited fields (after removing 'PAD~' prefix)."""
        return cls(
            shape=safe_str(fields[0] if len(fields) > 0 else ""),
            x=safe_float(fields[1] if len(fields) > 1 else 0),
            y=safe_float(fields[2] if len(fields) > 2 else 0),
            width=safe_float(fields[3] if len(fields) > 3 else 0),
            height=safe_float(fields[4] if len(fields) > 4 else 0),
            layer_id=safe_str(fields[5] if len(fields) > 5 else ""),
            net=safe_str(fields[6] if len(fields) > 6 else ""),
            number=safe_str(fields[7] if len(fields) > 7 else ""),
            hole_radius=safe_float(fields[8] if len(fields) > 8 else 0),
            points_str=safe_str(fields[9] if len(fields) > 9 else ""),
            rotation=safe_float(fields[10] if len(fields) > 10 else 0),
            id=safe_str(fields[11] if len(fields) > 11 else ""),
            hole_length=safe_float(fields[12] if len(fields) > 12 else 0),
            hole_points_str=safe_str(fields[13] if len(fields) > 13 else ""),
            plated=safe_str(fields[14] if len(fields) > 14 else ""),
        )
