"""
EasyEDA PCB footprint data model and parser.

Parses the ``result.packageDetail.dataStr`` section of an LCSC API response.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .easyeda_pad import EeFootprintPad
from .easyeda_shapes import (
    EeArc,
    EeCircle,
    EePolyline,
    EeRectangle,
)
from .easyeda_types import safe_float, safe_str

log = logging.getLogger(__name__)


@dataclass
class EeFootprintInfo:
    """Footprint metadata."""
    name: str = ""
    fp_type: str = ""  # SMD, THT
    model_3d_uuid: str = ""
    lcsc_id: str = ""

    def to_json(self) -> dict[str, Any]:
        return self.__dict__.copy()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeFootprintInfo:
        return cls(**{k: data.get(k, "") for k in cls().__dict__})


@dataclass
class EeFootprintTrack:
    """Copper track on footprint. Format: TRACK~strokeWidth~layerId~net~points~id"""
    stroke_width: float = 0.0
    layer_id: str = ""
    net: str = ""
    points_str: str = ""
    id: str = ""

    def to_json(self) -> dict[str, Any]:
        return self.__dict__.copy()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeFootprintTrack:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})

    @classmethod
    def from_fields(cls, fields: list[str]) -> EeFootprintTrack:
        return cls(
            stroke_width=safe_float(fields[0] if len(fields) > 0 else 0),
            layer_id=safe_str(fields[1] if len(fields) > 1 else ""),
            net=safe_str(fields[2] if len(fields) > 2 else ""),
            points_str=safe_str(fields[3] if len(fields) > 3 else ""),
            id=safe_str(fields[4] if len(fields) > 4 else ""),
        )


@dataclass
class EeFootprintHole:
    """Mounting hole. Format: HOLE~x~y~diameter~id"""
    x: float = 0.0
    y: float = 0.0
    diameter: float = 0.0
    id: str = ""

    def to_json(self) -> dict[str, Any]:
        return self.__dict__.copy()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeFootprintHole:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})

    @classmethod
    def from_fields(cls, fields: list[str]) -> EeFootprintHole:
        return cls(
            x=safe_float(fields[0] if len(fields) > 0 else 0),
            y=safe_float(fields[1] if len(fields) > 1 else 0),
            diameter=safe_float(fields[2] if len(fields) > 2 else 0),
            id=safe_str(fields[3] if len(fields) > 3 else ""),
        )


@dataclass
class EeFootprintVia:
    """Via. Format: VIA~x~y~diameter~net~holeRadius~id"""
    x: float = 0.0
    y: float = 0.0
    diameter: float = 0.0
    net: str = ""
    hole_radius: float = 0.0
    id: str = ""

    def to_json(self) -> dict[str, Any]:
        return self.__dict__.copy()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeFootprintVia:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})

    @classmethod
    def from_fields(cls, fields: list[str]) -> EeFootprintVia:
        return cls(
            x=safe_float(fields[0] if len(fields) > 0 else 0),
            y=safe_float(fields[1] if len(fields) > 1 else 0),
            diameter=safe_float(fields[2] if len(fields) > 2 else 0),
            net=safe_str(fields[3] if len(fields) > 3 else ""),
            hole_radius=safe_float(fields[4] if len(fields) > 4 else 0),
            id=safe_str(fields[5] if len(fields) > 5 else ""),
        )


@dataclass
class EeFootprintText:
    """Text on footprint. Format: TEXT~type~x~y~strokeWidth~rotation~mirror~layerId~net~fontSize~string~textPath~id"""
    text_type: str = ""  # L (label), P (prefix)
    x: float = 0.0
    y: float = 0.0
    stroke_width: float = 0.0
    rotation: float = 0.0
    mirror: str = ""
    layer_id: str = ""
    net: str = ""
    font_size: float = 0.0
    text: str = ""
    text_path: str = ""
    id: str = ""

    def to_json(self) -> dict[str, Any]:
        return self.__dict__.copy()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EeFootprintText:
        return cls(**{k: data.get(k, v) for k, v in cls().__dict__.items()})

    @classmethod
    def from_fields(cls, fields: list[str]) -> EeFootprintText:
        return cls(
            text_type=safe_str(fields[0] if len(fields) > 0 else ""),
            x=safe_float(fields[1] if len(fields) > 1 else 0),
            y=safe_float(fields[2] if len(fields) > 2 else 0),
            stroke_width=safe_float(fields[3] if len(fields) > 3 else 0),
            rotation=safe_float(fields[4] if len(fields) > 4 else 0),
            mirror=safe_str(fields[5] if len(fields) > 5 else ""),
            layer_id=safe_str(fields[6] if len(fields) > 6 else ""),
            net=safe_str(fields[7] if len(fields) > 7 else ""),
            font_size=safe_float(fields[8] if len(fields) > 8 else 0),
            text=safe_str(fields[9] if len(fields) > 9 else ""),
            text_path=safe_str(fields[10] if len(fields) > 10 else ""),
            id=safe_str(fields[11] if len(fields) > 11 else ""),
        )


@dataclass
class EasyEdaFootprint:
    """EasyEDA PCB footprint — the native data model."""

    info: EeFootprintInfo = field(default_factory=EeFootprintInfo)
    bbox_x: float = 0.0
    bbox_y: float = 0.0
    pads: list[EeFootprintPad] = field(default_factory=list)
    tracks: list[EeFootprintTrack] = field(default_factory=list)
    holes: list[EeFootprintHole] = field(default_factory=list)
    vias: list[EeFootprintVia] = field(default_factory=list)
    circles: list[EeCircle] = field(default_factory=list)
    rectangles: list[EeRectangle] = field(default_factory=list)
    arcs: list[EeArc] = field(default_factory=list)
    polylines: list[EePolyline] = field(default_factory=list)
    texts: list[EeFootprintText] = field(default_factory=list)

    raw_head: str = ""
    passthrough: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "info": self.info.to_json(),
            "bbox_x": self.bbox_x, "bbox_y": self.bbox_y,
            "pads": [p.to_json() for p in self.pads],
            "tracks": [t.to_json() for t in self.tracks],
            "holes": [h.to_json() for h in self.holes],
            "vias": [v.to_json() for v in self.vias],
            "circles": [c.to_json() for c in self.circles],
            "rectangles": [r.to_json() for r in self.rectangles],
            "arcs": [a.to_json() for a in self.arcs],
            "polylines": [p.to_json() for p in self.polylines],
            "texts": [t.to_json() for t in self.texts],
            "raw_head": self.raw_head,
            "passthrough": self.passthrough,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any] | str | Path) -> EasyEdaFootprint:
        if isinstance(data, (str, Path)):
            path = Path(data)
            if path.exists():
                payload = json.loads(path.read_text(encoding="utf-8"))
            else:
                payload = json.loads(str(data))
        else:
            payload = data

        if "result" in payload:
            return cls._from_api_response(payload)

        return cls(
            info=EeFootprintInfo.from_json(payload.get("info", {})),
            bbox_x=safe_float(payload.get("bbox_x")),
            bbox_y=safe_float(payload.get("bbox_y")),
            pads=[EeFootprintPad.from_json(p) for p in payload.get("pads", [])],
            tracks=[EeFootprintTrack.from_json(t) for t in payload.get("tracks", [])],
            holes=[EeFootprintHole.from_json(h) for h in payload.get("holes", [])],
            vias=[EeFootprintVia.from_json(v) for v in payload.get("vias", [])],
            circles=[EeCircle.from_json(c) for c in payload.get("circles", [])],
            rectangles=[EeRectangle.from_json(r) for r in payload.get("rectangles", [])],
            arcs=[EeArc.from_json(a) for a in payload.get("arcs", [])],
            polylines=[EePolyline.from_json(p) for p in payload.get("polylines", [])],
            texts=[EeFootprintText.from_json(t) for t in payload.get("texts", [])],
            raw_head=payload.get("raw_head", ""),
            passthrough=payload.get("passthrough", {}),
        )

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_json(), indent=2), encoding="utf-8")

    @classmethod
    def _from_api_response(cls, api_data: dict[str, Any]) -> EasyEdaFootprint:
        result = api_data.get("result", {})
        pkg_detail = result.get("packageDetail", {})
        data_str = pkg_detail.get("dataStr", {})
        head = data_str.get("head", {})
        shapes = data_str.get("shape", [])
        bbox = data_str.get("BBox", {})

        head_str = head if isinstance(head, str) else ""

        info = EeFootprintInfo(
            name=safe_str(result.get("title", "")),
            lcsc_id=safe_str(result.get("lcsc", {}).get("number",
                      result.get("szlcsc", {}).get("number", ""))),
        )

        fp = cls(
            info=info,
            bbox_x=safe_float(bbox.get("x")),
            bbox_y=safe_float(bbox.get("y")),
            raw_head=head_str,
        )

        for shape_str in shapes:
            _parse_shape_into_footprint(shape_str, fp)

        return fp


def _parse_shape_into_footprint(shape_str: str, fp: EasyEdaFootprint) -> None:
    """Parse one shape string and add to the appropriate list."""
    if not shape_str or not isinstance(shape_str, str):
        return

    if shape_str.startswith("PAD~"):
        fields = shape_str.split("~")[1:]
        fp.pads.append(EeFootprintPad.from_fields(fields))
    elif shape_str.startswith("TRACK~"):
        fields = shape_str.split("~")[1:]
        fp.tracks.append(EeFootprintTrack.from_fields(fields))
    elif shape_str.startswith("HOLE~"):
        fields = shape_str.split("~")[1:]
        fp.holes.append(EeFootprintHole.from_fields(fields))
    elif shape_str.startswith("VIA~"):
        fields = shape_str.split("~")[1:]
        fp.vias.append(EeFootprintVia.from_fields(fields))
    elif shape_str.startswith("CIRCLE~"):
        fields = shape_str.split("~")[1:]
        fp.circles.append(EeCircle.from_fields(fields))
    elif shape_str.startswith("RECT~"):
        fields = shape_str.split("~")[1:]
        fp.rectangles.append(EeRectangle.from_fields(fields))
    elif shape_str.startswith("ARC~"):
        fields = shape_str.split("~")[1:]
        fp.arcs.append(EeArc.from_fields(fields))
    elif shape_str.startswith("PL~") or shape_str.startswith("SOLIDREGION~"):
        fields = shape_str.split("~")[1:]
        fp.polylines.append(EePolyline.from_fields(fields))
    elif shape_str.startswith("TEXT~"):
        fields = shape_str.split("~")[1:]
        fp.texts.append(EeFootprintText.from_fields(fields))
    else:
        prefix = shape_str[:30]
        log.debug("Skipping unrecognized footprint shape: %s...", prefix)
