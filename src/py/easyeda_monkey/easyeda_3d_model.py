"""
EasyEDA 3D model reference and download support.

3D models are referenced by UUID in the footprint data and downloaded
from the EasyEDA modules API as STEP or OBJ files.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

log = logging.getLogger(__name__)

_STEP_URL_BASE = "https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y"
_OBJ_URL_BASE = "https://modules.easyeda.com/3dmodel"

if TYPE_CHECKING:
    from .easyeda_footprint import EasyEdaFootprint


@dataclass
class EasyEda3DModel:
    """3D model reference extracted from an EasyEDA footprint."""

    uuid: str = ""
    title: str = ""
    translation_x: float = 0.0
    translation_y: float = 0.0
    translation_z: float = 0.0
    rotation_x: float = 0.0
    rotation_y: float = 0.0
    rotation_z: float = 0.0
    raw_attrs: dict[str, Any] = field(default_factory=dict)

    @property
    def step_url(self) -> str:
        """URL to download STEP file."""
        if not self.uuid:
            return ""
        return f"{_STEP_URL_BASE}/{self.uuid}"

    @property
    def obj_url(self) -> str:
        """URL to download OBJ file."""
        if not self.uuid:
            return ""
        return f"{_OBJ_URL_BASE}/{self.uuid}"

    def to_json(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "title": self.title,
            "translation_x": self.translation_x,
            "translation_y": self.translation_y,
            "translation_z": self.translation_z,
            "rotation_x": self.rotation_x,
            "rotation_y": self.rotation_y,
            "rotation_z": self.rotation_z,
            "step_url": self.step_url,
            "obj_url": self.obj_url,
            "raw_attrs": self.raw_attrs,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> EasyEda3DModel:
        return cls(
            uuid=data.get("uuid", ""),
            title=data.get("title", ""),
            translation_x=float(data.get("translation_x", 0)),
            translation_y=float(data.get("translation_y", 0)),
            translation_z=float(data.get("translation_z", 0)),
            rotation_x=float(data.get("rotation_x", 0)),
            rotation_y=float(data.get("rotation_y", 0)),
            rotation_z=float(data.get("rotation_z", 0)),
            raw_attrs=data.get("raw_attrs", {}),
        )

    def download_step(self, output_path: str | Path, timeout: int = 30) -> bool:
        """Download STEP file to the given path. Returns True on success."""
        if not self.uuid:
            log.warning("No 3D model UUID — cannot download")
            return False

        import requests

        url = self.step_url
        log.info("Downloading STEP from %s", url)
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            Path(output_path).write_bytes(resp.content)
            log.info("Saved STEP (%d bytes) to %s", len(resp.content), output_path)
            return True
        except Exception as e:
            log.error("Failed to download STEP: %s", e)
            return False

    def download_obj(self, output_path: str | Path, timeout: int = 30) -> bool:
        """Download OBJ file to the given path. Returns True on success."""
        if not self.uuid:
            return False

        import requests

        url = self.obj_url
        log.info("Downloading OBJ from %s", url)
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            Path(output_path).write_text(resp.text, encoding="utf-8")
            log.info("Saved OBJ (%d bytes) to %s", len(resp.content), output_path)
            return True
        except Exception as e:
            log.error("Failed to download OBJ: %s", e)
            return False


def extract_3d_model_from_footprint(ee_fp: EasyEdaFootprint) -> EasyEda3DModel | None:
    """
    Extract 3D model reference from an EasyEdaFootprint's raw data.

    EasyEDA stores 3D model info in SVGNODE elements within the footprint
    shape list, containing JSON-encoded attributes with UUID, translation,
    and rotation.
    """
    # Look for the 3D model UUID in the footprint info
    model_uuid = ee_fp.info.model_3d_uuid
    if model_uuid:
        return EasyEda3DModel(uuid=model_uuid, title=ee_fp.info.name)

    # Fallback: search passthrough for SVGNODE-derived data
    return None


def extract_3d_models_from_api_response(api_data: dict[str, Any]) -> list[EasyEda3DModel]:
    """
    Extract all 3D model references from a raw API response.

    Searches packageDetail.dataStr.shape for SVGNODE entries containing
    3D model metadata.
    """
    models: list[EasyEda3DModel] = []
    result = api_data.get("result", {})
    pkg_detail = result.get("packageDetail", {})
    data_str = pkg_detail.get("dataStr", {})
    shapes = data_str.get("shape", [])

    for shape_str in shapes:
        if not isinstance(shape_str, str):
            continue
        if "SVGNODE" not in shape_str and "3dmodel" not in shape_str.lower():
            continue

        # Try to extract JSON from the SVGNODE
        model = _parse_svgnode_3d(shape_str)
        if model:
            models.append(model)

    # Also check head attributes for 3D model references
    head = data_str.get("head", "")
    if isinstance(head, str) and "3d" in head.lower():
        # Some footprints embed the UUID in head attributes
        uuid_match = re.search(r"([0-9a-f]{32}|[0-9a-f-]{36})", head)
        if uuid_match and not models:
            models.append(EasyEda3DModel(
                uuid=uuid_match.group(1),
                title=result.get("title", ""),
            ))

    return models


def _parse_svgnode_3d(shape_str: str) -> EasyEda3DModel | None:
    """Try to extract a 3D model reference from an SVGNODE shape string."""
    # SVGNODE shapes contain JSON-like attribute strings
    # Look for c_origin (translation) and c_rotation patterns
    try:
        # Extract UUID — look for a 32-char hex string or standard UUID
        uuid_match = re.search(r'"uuid"\s*:\s*"([^"]+)"', shape_str)
        if not uuid_match:
            uuid_match = re.search(r"([0-9a-f]{32})", shape_str)
        if not uuid_match:
            return None

        uuid = uuid_match.group(1)

        # Extract translation
        tx = ty = tz = 0.0
        origin_match = re.search(r'"c_origin"\s*:\s*"([^"]*)"', shape_str)
        if origin_match:
            parts = origin_match.group(1).split(",")
            if len(parts) >= 3:
                tx, ty, tz = float(parts[0]), float(parts[1]), float(parts[2])

        # Extract rotation
        rx = ry = rz = 0.0
        rot_match = re.search(r'"c_rotation"\s*:\s*"([^"]*)"', shape_str)
        if rot_match:
            parts = rot_match.group(1).split(",")
            if len(parts) >= 3:
                rx, ry, rz = float(parts[0]), float(parts[1]), float(parts[2])

        return EasyEda3DModel(
            uuid=uuid,
            translation_x=tx, translation_y=ty, translation_z=tz,
            rotation_x=rx, rotation_y=ry, rotation_z=rz,
        )
    except (ValueError, IndexError, AttributeError):
        return None
