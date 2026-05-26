"""Shared CLI command metadata types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CliCommandSpec:
    """Public CLI command metadata used by docs and signoff tests."""

    name: str
    design_doc: str
    help: str
