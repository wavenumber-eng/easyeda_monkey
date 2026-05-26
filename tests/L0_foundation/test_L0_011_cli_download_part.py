"""L0-011: CLI download-part behavior."""

from __future__ import annotations

import json
from pathlib import Path

from easyeda_monkey.cli import main
from easyeda_monkey.easyeda_3d_model import EasyEda3DModel

CASES_DIR = Path(__file__).parent / "cases" / "api_responses"


def test_download_part_writes_bundle_from_cached_fixture(monkeypatch, tmp_path: Path) -> None:
    """download-part should write JSON and requested 3D model files."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    fixture = CASES_DIR / "C21190__resistor_0603_1k.json"
    (cache_dir / "C21190.json").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

    def fake_download_step(
        self: EasyEda3DModel,
        output_path: str | Path,
        timeout: int = 30,
    ) -> bool:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(f"STEP {self.uuid} {timeout}\n", encoding="utf-8")
        return True

    def fake_download_obj(
        self: EasyEda3DModel,
        output_path: str | Path,
        timeout: int = 30,
    ) -> bool:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(f"OBJ {self.uuid} {timeout}\n", encoding="utf-8")
        return True

    monkeypatch.setattr(EasyEda3DModel, "download_step", fake_download_step)
    monkeypatch.setattr(EasyEda3DModel, "download_obj", fake_download_obj)

    output_root = tmp_path / "output"
    exit_code = main(
        [
            "download-part",
            "21190",
            "--cache-dir",
            str(cache_dir),
            "--output-dir",
            str(output_root),
        ]
    )

    bundle_dir = output_root / "C21190"
    report = json.loads((bundle_dir / "download-report.json").read_text(encoding="utf-8"))
    models = json.loads((bundle_dir / "3d-models.json").read_text(encoding="utf-8"))
    summary = json.loads((bundle_dir / "summary.json").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert (bundle_dir / "easyeda-api.json").exists()
    assert report["success"] is True
    assert report["model_count"] == len(models["models"])
    assert report["model_format"] == "both"
    assert len(report["downloads"]) == 2 * len(models["models"])
    assert summary["models_3d"]["count"] == len(models["models"])
    for download in report["downloads"]:
        assert download["success"] is True
        assert Path(download["path"]).exists()


def test_download_part_can_skip_model_downloads(tmp_path: Path) -> None:
    """download-part --model-format none should still write data files."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    fixture = CASES_DIR / "C21190__resistor_0603_1k.json"
    (cache_dir / "C21190.json").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")

    output_root = tmp_path / "parts"
    exit_code = main(
        [
            "download-part",
            "C21190",
            "--cache-dir",
            str(cache_dir),
            "--output-dir",
            str(output_root),
            "--model-format",
            "none",
        ]
    )

    bundle_dir = output_root / "C21190"
    report = json.loads((bundle_dir / "download-report.json").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert report["success"] is True
    assert report["downloads"] == []
    assert (bundle_dir / "easyeda-api.json").exists()
    assert (bundle_dir / "summary.json").exists()
    assert (bundle_dir / "3d-models.json").exists()
