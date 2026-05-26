"""
L0-009: 3D model reference extraction from API fixtures.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from easyeda_monkey.easyeda_3d_model import (
    EasyEda3DModel,
    extract_3d_models_from_api_response,
)

CASES_DIR = Path(__file__).parent / "cases" / "api_responses"


def _fixture_files() -> list[Path]:
    if not CASES_DIR.exists():
        return []
    return sorted(CASES_DIR.glob("*.json"))


def test_3d_model_urls():
    """Model should generate correct STEP and OBJ URLs from UUID."""
    model = EasyEda3DModel(uuid="abc123def456")
    assert "abc123def456" in model.step_url
    assert "abc123def456" in model.obj_url
    assert model.step_url.startswith("https://")
    assert model.obj_url.startswith("https://")


def test_3d_model_empty_uuid():
    """Empty UUID should produce empty URLs."""
    model = EasyEda3DModel()
    assert model.step_url == ""
    assert model.obj_url == ""


def test_3d_model_json_roundtrip():
    """3D model should round-trip through JSON."""
    model = EasyEda3DModel(
        uuid="test123",
        title="Test Part",
        translation_x=1.0, translation_y=2.0, translation_z=3.0,
        rotation_x=90.0, rotation_y=0.0, rotation_z=180.0,
    )
    data = model.to_json()
    restored = EasyEda3DModel.from_json(data)
    assert restored.uuid == model.uuid
    assert restored.title == model.title
    assert restored.translation_x == model.translation_x
    assert restored.rotation_x == model.rotation_x


@pytest.mark.parametrize("fixture_path", _fixture_files(), ids=lambda p: p.stem)
def test_extract_3d_models_no_crash(fixture_path: Path):
    """3D model extraction should not crash on any fixture."""
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    models = extract_3d_models_from_api_response(data)
    # May or may not find models — just verify no crash
    assert isinstance(models, list)
