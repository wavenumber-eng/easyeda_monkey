"""
Minimal SVG path string parser for EasyEDA arc and bezier primitives.

Handles the subset of SVG path commands used by EasyEDA:
  M (moveto), L (lineto), H (horizontal), V (vertical),
  C (cubic bezier), Q (quadratic bezier), A (elliptical arc), Z (close).

Returns a list of typed segment dicts suitable for conversion to
DwgPathSegment or SymbolGraphic objects.
"""

from __future__ import annotations

import re
from typing import Any


def parse_svg_path(d: str | None) -> list[dict[str, Any]]:
    """
    Parse an SVG path ``d`` attribute into a list of segment dicts.

    Each segment dict has a ``kind`` key and relevant coordinate fields.
    All coordinates are floats in the source coordinate system (not converted).

    Returns:
        List of segment dicts, each with ``kind`` and point fields.
    """
    if not d or not isinstance(d, str):
        return []

    segments: list[dict[str, Any]] = []
    tokens = _tokenize(d)
    i = 0
    cx, cy = 0.0, 0.0  # current point

    while i < len(tokens):
        cmd = tokens[i]
        if not isinstance(cmd, str) or not cmd.isalpha():
            i += 1
            continue

        is_relative = cmd.islower()
        cmd_upper = cmd.upper()
        i += 1

        if cmd_upper == "M":
            # moveto — may have implicit lineto args after first pair
            first = True
            while i + 1 < len(tokens) and _is_number(tokens[i]):
                x, y = float(tokens[i]), float(tokens[i + 1])
                if is_relative:
                    x += cx
                    y += cy
                cx, cy = x, y
                if first:
                    segments.append({"kind": "moveto", "x": x, "y": y})
                    first = False
                else:
                    segments.append({"kind": "lineto", "x": x, "y": y})
                i += 2

        elif cmd_upper == "L":
            while i + 1 < len(tokens) and _is_number(tokens[i]):
                x, y = float(tokens[i]), float(tokens[i + 1])
                if is_relative:
                    x += cx
                    y += cy
                cx, cy = x, y
                segments.append({"kind": "lineto", "x": x, "y": y})
                i += 2

        elif cmd_upper == "H":
            while i < len(tokens) and _is_number(tokens[i]):
                x = float(tokens[i])
                if is_relative:
                    x += cx
                cx = x
                segments.append({"kind": "lineto", "x": cx, "y": cy})
                i += 1

        elif cmd_upper == "V":
            while i < len(tokens) and _is_number(tokens[i]):
                y = float(tokens[i])
                if is_relative:
                    y += cy
                cy = y
                segments.append({"kind": "lineto", "x": cx, "y": cy})
                i += 1

        elif cmd_upper == "C":
            while i + 5 < len(tokens) and _is_number(tokens[i]):
                c1x, c1y = float(tokens[i]), float(tokens[i + 1])
                c2x, c2y = float(tokens[i + 2]), float(tokens[i + 3])
                ex, ey = float(tokens[i + 4]), float(tokens[i + 5])
                if is_relative:
                    c1x += cx
                    c1y += cy
                    c2x += cx
                    c2y += cy
                    ex += cx
                    ey += cy
                cx, cy = ex, ey
                segments.append({
                    "kind": "cubicto",
                    "c1x": c1x, "c1y": c1y,
                    "c2x": c2x, "c2y": c2y,
                    "x": ex, "y": ey,
                })
                i += 6

        elif cmd_upper == "Q":
            while i + 3 < len(tokens) and _is_number(tokens[i]):
                c1x, c1y = float(tokens[i]), float(tokens[i + 1])
                ex, ey = float(tokens[i + 2]), float(tokens[i + 3])
                if is_relative:
                    c1x += cx
                    c1y += cy
                    ex += cx
                    ey += cy
                cx, cy = ex, ey
                segments.append({
                    "kind": "quadto",
                    "c1x": c1x, "c1y": c1y,
                    "x": ex, "y": ey,
                })
                i += 4

        elif cmd_upper == "A":
            while i + 6 < len(tokens) and _is_number(tokens[i]):
                rx = float(tokens[i])
                ry = float(tokens[i + 1])
                x_rotation = float(tokens[i + 2])
                large_arc = int(float(tokens[i + 3]))
                sweep = int(float(tokens[i + 4]))
                ex, ey = float(tokens[i + 5]), float(tokens[i + 6])
                if is_relative:
                    ex += cx
                    ey += cy
                cx, cy = ex, ey
                segments.append({
                    "kind": "arcto",
                    "rx": rx, "ry": ry,
                    "x_rotation": x_rotation,
                    "large_arc": bool(large_arc),
                    "sweep": bool(sweep),
                    "x": ex, "y": ey,
                })
                i += 7

        elif cmd_upper == "Z":
            segments.append({"kind": "closepath"})

        else:
            i += 1  # skip unknown

    return segments


# Regex to tokenize SVG path: splits on commands and numbers (including negatives/decimals)
_TOKEN_RE = re.compile(r"([A-Za-z]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)")


def _tokenize(d: str) -> list[str]:
    """Split SVG path string into command letters and number strings."""
    return _TOKEN_RE.findall(d)


def _is_number(token: str) -> bool:
    """Check if a token is a number (not a command letter)."""
    if not token:
        return False
    try:
        float(token)
        return True
    except ValueError:
        return False
