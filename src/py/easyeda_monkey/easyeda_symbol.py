"""
EasyEDA schematic symbol data model and parser.

Parses the ``result.dataStr`` section of an LCSC API response into
a typed Python object with pins, graphics, and metadata.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .easyeda_pin import EasyEdaPin
from .easyeda_shapes import (
    EeArc,
    EeCircle,
    EeEllipse,
    EePath,
    EePolygon,
    EePolyline,
    EeRectangle,
)
from .easyeda_types import safe_float, safe_str

log = logging.getLogger(__name__)


@dataclass
class EeSymbolInfo:
    """Symbol metadata extracted from the head and API response."""
    name: str = ""
    prefix: str = ""
    package: str = ""
    manufacturer: str = ""
    datasheet: str = ""
    lcsc_id: str = ""
    description: str = ""

    def to_json(self) -> dict[str, Any]:
        return self.__dict__.copy()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeSymbolInfo:
        return cls(**{k: data.get(k, "") for k in cls().__dict__})


@dataclass
class EasyEdaSymbol:
    """
    EasyEDA schematic symbol — the native data model.

    Constructed from an LCSC API response or saved JSON fixture.
    """

    info: EeSymbolInfo = field(default_factory=EeSymbolInfo)
    bbox_x: float = 0.0
    bbox_y: float = 0.0
    pins: list[EasyEdaPin] = field(default_factory=list)
    rectangles: list[EeRectangle] = field(default_factory=list)
    circles: list[EeCircle] = field(default_factory=list)
    ellipses: list[EeEllipse] = field(default_factory=list)
    arcs: list[EeArc] = field(default_factory=list)
    polylines: list[EePolyline] = field(default_factory=list)
    polygons: list[EePolygon] = field(default_factory=list)
    paths: list[EePath] = field(default_factory=list)

    # Raw head string and passthrough for fields we don't model
    raw_head: str = ""
    passthrough: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "info": self.info.to_json(),
            "bbox_x": self.bbox_x, "bbox_y": self.bbox_y,
            "pins": [p.to_json() for p in self.pins],
            "rectangles": [s.to_json() for s in self.rectangles],
            "circles": [s.to_json() for s in self.circles],
            "ellipses": [s.to_json() for s in self.ellipses],
            "arcs": [s.to_json() for s in self.arcs],
            "polylines": [s.to_json() for s in self.polylines],
            "polygons": [s.to_json() for s in self.polygons],
            "paths": [s.to_json() for s in self.paths],
            "raw_head": self.raw_head,
            "passthrough": self.passthrough,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any] | str | Path) -> EasyEdaSymbol:
        """Parse from a dict, JSON string, or file path."""
        if isinstance(data, (str, Path)):
            path = Path(data)
            if path.exists():
                payload = json.loads(path.read_text(encoding="utf-8"))
            else:
                payload = json.loads(str(data))
        else:
            payload = data

        # If this is a full API response, drill into result.dataStr
        if "result" in payload:
            return cls._from_api_response(payload)

        # Otherwise it's our own serialized format
        return cls(
            info=EeSymbolInfo.from_json(payload.get("info", {})),
            bbox_x=safe_float(payload.get("bbox_x")),
            bbox_y=safe_float(payload.get("bbox_y")),
            pins=[EasyEdaPin.from_json(p) for p in payload.get("pins", [])],
            rectangles=[EeRectangle.from_json(s) for s in payload.get("rectangles", [])],
            circles=[EeCircle.from_json(s) for s in payload.get("circles", [])],
            ellipses=[EeEllipse.from_json(s) for s in payload.get("ellipses", [])],
            arcs=[EeArc.from_json(s) for s in payload.get("arcs", [])],
            polylines=[EePolyline.from_json(s) for s in payload.get("polylines", [])],
            polygons=[EePolygon.from_json(s) for s in payload.get("polygons", [])],
            paths=[EePath.from_json(s) for s in payload.get("paths", [])],
            raw_head=payload.get("raw_head", ""),
            passthrough=payload.get("passthrough", {}),
        )

    def save(self, path: str | Path) -> None:
        """Write to JSON file."""
        Path(path).write_text(json.dumps(self.to_json(), indent=2), encoding="utf-8")

    @classmethod
    def _from_api_response(cls, api_data: dict[str, Any]) -> EasyEdaSymbol:
        """Parse from a full LCSC API JSON response."""
        result = api_data.get("result", {})
        data_str = result.get("dataStr", {})
        head = data_str.get("head", {})
        shapes = data_str.get("shape", [])
        bbox = data_str.get("BBox", {})

        # Extract info from result + head
        head_str = head if isinstance(head, str) else ""
        head_attrs = _parse_head_attributes(head_str) if head_str else {}

        info = EeSymbolInfo(
            name=safe_str(result.get("title", "")),
            prefix=safe_str(head_attrs.get("pre", "")),
            package=safe_str(head_attrs.get("package", "")),
            manufacturer=safe_str(result.get("owner", {}).get("username", "")),
            datasheet=safe_str(head_attrs.get("link", "")),
            lcsc_id=safe_str(result.get("lcsc", {}).get("number",
                      result.get("szlcsc", {}).get("number", ""))),
            description=safe_str(result.get("description", "")),
        )

        sym = cls(
            info=info,
            bbox_x=safe_float(bbox.get("x")),
            bbox_y=safe_float(bbox.get("y")),
            raw_head=head_str,
            passthrough={"api_uuid": result.get("uuid", "")},
        )

        # Parse shapes
        for shape_str in shapes:
            _parse_shape_into_symbol(shape_str, sym)

        return sym


def _parse_head_attributes(head_str: str) -> dict[str, str]:
    """Parse backtick-separated key-value pairs from head string."""
    attrs: dict[str, str] = {}
    # Head format: "7~1.7.5~400~300~package`DIP08`nameDisplay`0`pre`U?`..."
    # Split by backtick, pair up
    parts = head_str.split("`")
    for i in range(0, len(parts) - 1, 2):
        key = parts[i].strip()
        value = parts[i + 1] if i + 1 < len(parts) else ""
        # The key might be preceded by other fields separated by ~
        if "~" in key:
            key = key.rsplit("~", 1)[-1]
        if key:
            attrs[key] = value
    return attrs


def _parse_shape_into_symbol(shape_str: str, sym: EasyEdaSymbol) -> None:
    """Parse one shape string and add to the appropriate list on sym."""
    if not shape_str or not isinstance(shape_str, str):
        return

    # Determine prefix
    if shape_str.startswith("P~") or shape_str.startswith("P "):
        # Pin — remove the "P~" prefix and parse
        pin_data = shape_str[2:]
        sym.pins.append(EasyEdaPin.from_shape_string(pin_data))
    elif shape_str.startswith("R~"):
        fields = shape_str.split("~")[1:]
        sym.rectangles.append(EeRectangle.from_fields(fields))
    elif shape_str.startswith("C~"):
        fields = shape_str.split("~")[1:]
        sym.circles.append(EeCircle.from_fields(fields))
    elif shape_str.startswith("E~"):
        fields = shape_str.split("~")[1:]
        sym.ellipses.append(EeEllipse.from_fields(fields))
    elif shape_str.startswith("A~"):
        fields = shape_str.split("~")[1:]
        sym.arcs.append(EeArc.from_fields(fields))
    elif shape_str.startswith("PL~"):
        fields = shape_str.split("~")[1:]
        sym.polylines.append(EePolyline.from_fields(fields))
    elif shape_str.startswith("PG~"):
        fields = shape_str.split("~")[1:]
        sym.polygons.append(EePolygon.from_fields(fields))
    elif shape_str.startswith("PT~"):
        fields = shape_str.split("~")[1:]
        sym.paths.append(EePath.from_fields(fields))
    else:
        # Unrecognized shape — log and skip
        prefix = shape_str[:20]
        log.debug("Skipping unrecognized symbol shape: %s...", prefix)
