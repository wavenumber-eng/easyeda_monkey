"""
L0-008: SVG path string parser tests.
"""

from easyeda_monkey.easyeda_svg_path import parse_svg_path


def test_moveto_lineto():
    segs = parse_svg_path("M 10 20 L 30 40 L 50 60")
    assert len(segs) == 3
    assert segs[0] == {"kind": "moveto", "x": 10.0, "y": 20.0}
    assert segs[1] == {"kind": "lineto", "x": 30.0, "y": 40.0}
    assert segs[2] == {"kind": "lineto", "x": 50.0, "y": 60.0}


def test_horizontal_vertical():
    segs = parse_svg_path("M 0 0 H 100 V 200")
    assert len(segs) == 3
    assert segs[1] == {"kind": "lineto", "x": 100.0, "y": 0.0}
    assert segs[2] == {"kind": "lineto", "x": 100.0, "y": 200.0}


def test_cubic_bezier():
    segs = parse_svg_path("M 0 0 C 10 20 30 40 50 60")
    assert len(segs) == 2
    c = segs[1]
    assert c["kind"] == "cubicto"
    assert c["c1x"] == 10.0
    assert c["c1y"] == 20.0
    assert c["c2x"] == 30.0
    assert c["c2y"] == 40.0
    assert c["x"] == 50.0
    assert c["y"] == 60.0


def test_quadratic_bezier():
    segs = parse_svg_path("M 0 0 Q 50 100 100 0")
    assert len(segs) == 2
    q = segs[1]
    assert q["kind"] == "quadto"
    assert q["c1x"] == 50.0
    assert q["x"] == 100.0


def test_arc():
    segs = parse_svg_path("M 0 0 A 25 25 0 0 1 50 50")
    assert len(segs) == 2
    a = segs[1]
    assert a["kind"] == "arcto"
    assert a["rx"] == 25.0
    assert a["ry"] == 25.0
    assert a["large_arc"] is False
    assert a["sweep"] is True
    assert a["x"] == 50.0


def test_closepath():
    segs = parse_svg_path("M 0 0 L 100 0 L 100 100 Z")
    assert len(segs) == 4
    assert segs[3] == {"kind": "closepath"}


def test_no_spaces():
    """EasyEDA often has no spaces between commands and numbers."""
    segs = parse_svg_path("M670 300C830 370 850 230 920 300")
    assert len(segs) == 2
    assert segs[0]["kind"] == "moveto"
    assert segs[1]["kind"] == "cubicto"


def test_relative_commands():
    segs = parse_svg_path("M 100 200 l 10 20 l 30 40")
    assert len(segs) == 3
    assert segs[1] == {"kind": "lineto", "x": 110.0, "y": 220.0}
    assert segs[2] == {"kind": "lineto", "x": 140.0, "y": 260.0}


def test_empty_returns_empty():
    assert parse_svg_path("") == []
    assert parse_svg_path(None) == []


def test_easyeda_arc_path():
    """Real EasyEDA arc path from the format docs."""
    segs = parse_svg_path("M 1020 60 A 80 80 0 0 1 953.096 199.904")
    assert len(segs) == 2
    assert segs[0]["kind"] == "moveto"
    a = segs[1]
    assert a["kind"] == "arcto"
    assert a["rx"] == 80.0
    assert abs(a["x"] - 953.096) < 0.001


def test_negative_coordinates():
    segs = parse_svg_path("M -10 -20 L -30 -40")
    assert segs[0] == {"kind": "moveto", "x": -10.0, "y": -20.0}
    assert segs[1] == {"kind": "lineto", "x": -30.0, "y": -40.0}
