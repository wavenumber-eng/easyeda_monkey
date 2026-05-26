"""
EasyEDA graphic shape primitives — rectangle, circle, ellipse, arc, polyline, polygon, path.

Each shape is parsed from a tilde-delimited string with a type prefix.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .easyeda_types import safe_float, safe_str


@dataclass
class EeRectangle:
    """EasyEDA rectangle. Format: R~x~y~rx~ry~width~height~strokeColor~strokeWidth~strokeStyle~fillColor~id"""
    x: float = 0.0
    y: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    width: float = 0.0
    height: float = 0.0
    stroke_color: str = "#000000"
    stroke_width: float = 1.0
    stroke_style: str = "0"
    fill_color: str = "none"
    id: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "type": "rectangle", "x": self.x, "y": self.y,
            "rx": self.rx, "ry": self.ry, "width": self.width, "height": self.height,
            "stroke_color": self.stroke_color, "stroke_width": self.stroke_width,
            "stroke_style": self.stroke_style, "fill_color": self.fill_color, "id": self.id,
        }

    @classmethod
    def from_fields(cls, fields: list[str]) -> EeRectangle:
        return cls(
            x=safe_float(fields[0]), y=safe_float(fields[1]),
            rx=safe_float(fields[2]), ry=safe_float(fields[3]),
            width=safe_float(fields[4]), height=safe_float(fields[5]),
            stroke_color=safe_str(fields[6] if len(fields) > 6 else ""),
            stroke_width=safe_float(fields[7] if len(fields) > 7 else 1),
            stroke_style=safe_str(fields[8] if len(fields) > 8 else "0"),
            fill_color=safe_str(fields[9] if len(fields) > 9 else "none"),
            id=safe_str(fields[10] if len(fields) > 10 else ""),
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeRectangle:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})


@dataclass
class EeCircle:
    """EasyEDA circle. Format: C~cx~cy~radius~strokeColor~strokeWidth~strokeStyle~fillColor~id"""
    cx: float = 0.0
    cy: float = 0.0
    radius: float = 0.0
    stroke_color: str = "#000000"
    stroke_width: float = 1.0
    stroke_style: str = "0"
    fill_color: str = "none"
    id: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "type": "circle", "cx": self.cx, "cy": self.cy, "radius": self.radius,
            "stroke_color": self.stroke_color, "stroke_width": self.stroke_width,
            "stroke_style": self.stroke_style, "fill_color": self.fill_color, "id": self.id,
        }

    @classmethod
    def from_fields(cls, fields: list[str]) -> EeCircle:
        return cls(
            cx=safe_float(fields[0]), cy=safe_float(fields[1]),
            radius=safe_float(fields[2]),
            stroke_color=safe_str(fields[3] if len(fields) > 3 else ""),
            stroke_width=safe_float(fields[4] if len(fields) > 4 else 1),
            stroke_style=safe_str(fields[5] if len(fields) > 5 else "0"),
            fill_color=safe_str(fields[6] if len(fields) > 6 else "none"),
            id=safe_str(fields[7] if len(fields) > 7 else ""),
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeCircle:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})


@dataclass
class EeEllipse:
    """EasyEDA ellipse. Format: E~cx~cy~rx~ry~strokeColor~strokeWidth~strokeStyle~fillColor~id"""
    cx: float = 0.0
    cy: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    stroke_color: str = "#000000"
    stroke_width: float = 1.0
    stroke_style: str = "0"
    fill_color: str = "none"
    id: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "type": "ellipse", "cx": self.cx, "cy": self.cy,
            "rx": self.rx, "ry": self.ry,
            "stroke_color": self.stroke_color, "stroke_width": self.stroke_width,
            "stroke_style": self.stroke_style, "fill_color": self.fill_color, "id": self.id,
        }

    @classmethod
    def from_fields(cls, fields: list[str]) -> EeEllipse:
        return cls(
            cx=safe_float(fields[0]), cy=safe_float(fields[1]),
            rx=safe_float(fields[2]), ry=safe_float(fields[3]),
            stroke_color=safe_str(fields[4] if len(fields) > 4 else ""),
            stroke_width=safe_float(fields[5] if len(fields) > 5 else 1),
            stroke_style=safe_str(fields[6] if len(fields) > 6 else "0"),
            fill_color=safe_str(fields[7] if len(fields) > 7 else "none"),
            id=safe_str(fields[8] if len(fields) > 8 else ""),
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeEllipse:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})


@dataclass
class EeArc:
    """EasyEDA arc. Format: A~pathString~helperDots~strokeColor~strokeWidth~strokeStyle~fillColor~id"""
    path_string: str = ""
    helper_dots: str = ""
    stroke_color: str = "#000000"
    stroke_width: float = 1.0
    stroke_style: str = "0"
    fill_color: str = "none"
    id: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "type": "arc", "path_string": self.path_string, "helper_dots": self.helper_dots,
            "stroke_color": self.stroke_color, "stroke_width": self.stroke_width,
            "stroke_style": self.stroke_style, "fill_color": self.fill_color, "id": self.id,
        }

    @classmethod
    def from_fields(cls, fields: list[str]) -> EeArc:
        return cls(
            path_string=safe_str(fields[0] if len(fields) > 0 else ""),
            helper_dots=safe_str(fields[1] if len(fields) > 1 else ""),
            stroke_color=safe_str(fields[2] if len(fields) > 2 else ""),
            stroke_width=safe_float(fields[3] if len(fields) > 3 else 1),
            stroke_style=safe_str(fields[4] if len(fields) > 4 else "0"),
            fill_color=safe_str(fields[5] if len(fields) > 5 else "none"),
            id=safe_str(fields[6] if len(fields) > 6 else ""),
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeArc:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})


@dataclass
class EePolyline:
    """EasyEDA polyline. Format: PL~points~strokeColor~strokeWidth~strokeStyle~fillColor~id"""
    points_str: str = ""
    stroke_color: str = "#000000"
    stroke_width: float = 1.0
    stroke_style: str = "0"
    fill_color: str = "none"
    id: str = ""

    @property
    def points(self) -> list[tuple[float, float]]:
        """Parse point string into (x, y) tuples."""
        parts = self.points_str.strip().split()
        return [(safe_float(parts[i]), safe_float(parts[i + 1]))
                for i in range(0, len(parts) - 1, 2)]

    def to_json(self) -> dict[str, Any]:
        return {
            "type": "polyline", "points_str": self.points_str,
            "stroke_color": self.stroke_color, "stroke_width": self.stroke_width,
            "stroke_style": self.stroke_style, "fill_color": self.fill_color, "id": self.id,
        }

    @classmethod
    def from_fields(cls, fields: list[str]) -> EePolyline:
        return cls(
            points_str=safe_str(fields[0] if len(fields) > 0 else ""),
            stroke_color=safe_str(fields[1] if len(fields) > 1 else ""),
            stroke_width=safe_float(fields[2] if len(fields) > 2 else 1),
            stroke_style=safe_str(fields[3] if len(fields) > 3 else "0"),
            fill_color=safe_str(fields[4] if len(fields) > 4 else "none"),
            id=safe_str(fields[5] if len(fields) > 5 else ""),
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EePolyline:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})


@dataclass
class EePolygon:
    """EasyEDA polygon. Format: PG~points~strokeColor~strokeWidth~strokeStyle~fillColor~id"""
    points_str: str = ""
    stroke_color: str = "#000000"
    stroke_width: float = 1.0
    stroke_style: str = "0"
    fill_color: str = "none"
    id: str = ""

    @property
    def points(self) -> list[tuple[float, float]]:
        parts = self.points_str.strip().split()
        return [(safe_float(parts[i]), safe_float(parts[i + 1]))
                for i in range(0, len(parts) - 1, 2)]

    def to_json(self) -> dict[str, Any]:
        return {
            "type": "polygon", "points_str": self.points_str,
            "stroke_color": self.stroke_color, "stroke_width": self.stroke_width,
            "stroke_style": self.stroke_style, "fill_color": self.fill_color, "id": self.id,
        }

    @classmethod
    def from_fields(cls, fields: list[str]) -> EePolygon:
        return cls(
            points_str=safe_str(fields[0] if len(fields) > 0 else ""),
            stroke_color=safe_str(fields[1] if len(fields) > 1 else ""),
            stroke_width=safe_float(fields[2] if len(fields) > 2 else 1),
            stroke_style=safe_str(fields[3] if len(fields) > 3 else "0"),
            fill_color=safe_str(fields[4] if len(fields) > 4 else "none"),
            id=safe_str(fields[5] if len(fields) > 5 else ""),
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EePolygon:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})


@dataclass
class EePath:
    """EasyEDA path (SVG path string, may contain bezier curves). Format: PT~pathString~strokeColor~strokeWidth~strokeStyle~fillColor~id"""
    path_string: str = ""
    stroke_color: str = "#000000"
    stroke_width: float = 1.0
    stroke_style: str = "0"
    fill_color: str = "none"
    id: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "type": "path", "path_string": self.path_string,
            "stroke_color": self.stroke_color, "stroke_width": self.stroke_width,
            "stroke_style": self.stroke_style, "fill_color": self.fill_color, "id": self.id,
        }

    @classmethod
    def from_fields(cls, fields: list[str]) -> EePath:
        return cls(
            path_string=safe_str(fields[0] if len(fields) > 0 else ""),
            stroke_color=safe_str(fields[1] if len(fields) > 1 else ""),
            stroke_width=safe_float(fields[2] if len(fields) > 2 else 1),
            stroke_style=safe_str(fields[3] if len(fields) > 3 else "0"),
            fill_color=safe_str(fields[4] if len(fields) > 4 else "none"),
            id=safe_str(fields[5] if len(fields) > 5 else ""),
        )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EePath:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})
