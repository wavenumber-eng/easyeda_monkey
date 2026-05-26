"""Design documentation signoff for dataclasses and major interfaces."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path


def _project_root() -> Path:
    """Find the repository root from this test file."""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repository root")


@dataclass(frozen=True)
class InterfaceDoc:
    """Machine-readable interface documentation metadata."""

    name: str
    doc_path: Path
    section_text: str
    rack_stratum: str
    test_file: Path
    test_target: str


PACKAGE_ROOT = _project_root()
SOURCE_ROOT = PACKAGE_ROOT / "src" / "py" / "easyeda_monkey"
DESIGN_ROOT = PACKAGE_ROOT / "docs" / "design"

MAJOR_INTERFACES = frozenset(
    {
        "EasyEdaApiClient",
        "extract_3d_models_from_api_response",
        "parse_svg_path",
    }
)


def _is_dataclass_decorator(decorator: ast.expr) -> bool:
    """Return whether an AST decorator represents dataclass usage."""
    if isinstance(decorator, ast.Name):
        return decorator.id == "dataclass"
    if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
        return decorator.func.id == "dataclass"
    return False


def _public_dataclasses() -> set[str]:
    """Return all package dataclass names that require design docs."""
    dataclasses: set[str] = set()
    for source_path in SOURCE_ROOT.glob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and any(
                _is_dataclass_decorator(decorator) for decorator in node.decorator_list
            ):
                dataclasses.add(node.name)
    return dataclasses


def _interface_docs() -> dict[str, InterfaceDoc]:
    """Collect interface design-doc sections from HTML design docs."""
    docs: dict[str, InterfaceDoc] = {}
    section_pattern = re.compile(
        r"<section\b(?P<attrs>[^>]*)data-interface=\"(?P<name>[^\"]+)\"(?P<attrs2>[^>]*)>"
        r"(?P<body>.*?)</section>",
        re.DOTALL,
    )
    attr_pattern = re.compile(r"(?P<name>data-[a-z-]+)=\"(?P<value>[^\"]+)\"")

    for doc_path in DESIGN_ROOT.rglob("*.html"):
        text = doc_path.read_text(encoding="utf-8")
        for match in section_pattern.finditer(text):
            attrs = dict(attr_pattern.findall(match.group("attrs") + match.group("attrs2")))
            name = match.group("name")
            docs[name] = InterfaceDoc(
                name=name,
                doc_path=doc_path,
                section_text=match.group("body"),
                rack_stratum=attrs.get("data-rack-stratum", ""),
                test_file=PACKAGE_ROOT / attrs.get("data-test-file", ""),
                test_target=attrs.get("data-test-target", ""),
            )
    return docs


def test_dataclasses_and_major_interfaces_have_design_docs() -> None:
    """Verify design-doc coverage for data classes and major interfaces."""
    required = _public_dataclasses() | MAJOR_INTERFACES
    docs = _interface_docs()

    missing = sorted(required - set(docs))
    assert missing == []


def test_interface_design_docs_define_rationale_tests_and_working_state() -> None:
    """Verify each interface doc section records design and test expectations."""
    required = _public_dataclasses() | MAJOR_INTERFACES
    docs = _interface_docs()

    for name in sorted(required):
        doc = docs[name]
        assert "Rationale" in doc.section_text, name
        assert "Purpose" in doc.section_text, name
        assert "Test Requirements" in doc.section_text, name
        assert "Working Definition" in doc.section_text, name


def test_interface_design_docs_point_to_rack_exercising_tests() -> None:
    """Verify interface docs point to an exercising Rack stratum and test target."""
    required = _public_dataclasses() | MAJOR_INTERFACES
    docs = _interface_docs()

    for name in sorted(required):
        doc = docs[name]
        stratum = PACKAGE_ROOT / "tests" / doc.rack_stratum / "STRATUM.toml"
        assert stratum.exists(), f"{name} references missing Rack stratum {doc.rack_stratum}"
        assert doc.test_file.exists(), f"{name} references missing test file {doc.test_file}"

        test_text = doc.test_file.read_text(encoding="utf-8")
        assert doc.test_target in test_text, f"{name} test target not found: {doc.test_target}"
