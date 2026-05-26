# EasyEDA Monkey

`easyeda_monkey` is a small Python package for reading EasyEDA / LCSC component
data into typed Python objects.

Current scope:

- EasyEDA / LCSC component API responses
- schematic symbols
- PCB footprints
- 3D model references and URL extraction
- SVG path parsing helpers

The package is intentionally focused on parsing and close-to-format data
models. Workflow commands and conversion applications should live in downstream
tools such as `altium-cruncher`.

## Install

```powershell
pip install easyeda-monkey
```

For development:

```powershell
git clone https://github.com/wavenumber-eng/easyeda_monkey.git
cd easyeda_monkey
uv sync --extra test
```

## Testing

The active suite uses redistributable saved EasyEDA / LCSC API response
fixtures and does not require a private corpus.

```powershell
uv run --extra test pytest -q
uv run --extra test rack run --all
uv run --extra test python scripts/py_signoff.py --root . --baseline scripts/py_signoff_baseline.json
uv run --extra test ruff check .
uv run --extra test pyright src/py tests
```

## CLI

The package installs the `easyeda-monkey` console script.

```powershell
easyeda-monkey --version
easyeda-monkey fetch-part C21190
easyeda-monkey fetch-part C21190 --cache-dir .cache/easyeda --output C21190.summary.json
```

## Design And Test Docs

`docs/` is the source of truth for architecture, tests, and contracts. The
master design entry point is [docs/design/index.html](docs/design/index.html).

Every public CLI command must have a matching HTML design document under
`docs/design/cli/`. The filename must match the command name, and signoff fails
when a registered command is missing its design document.

Commands that accept config files must also define a machine-readable contract
and validation tests before release.

## Fixture Model

Active fixtures live under:

- `tests/L0_foundation/cases/api_responses`

Broader fixture families should use this shape when needed:

- `input/`
- `reference_output/`
- `output/`

`output/` is transient and should stay local or temporary.

## Scope Boundaries

Core package responsibilities:

- parse EasyEDA-native JSON structures into typed Python objects
- preserve EasyEDA-native semantics
- expose a clean parser/API surface for downstream converters

Deferred or downstream responsibilities:

- command-line workflow applications
- Altium, KiCad, or other EDA conversion policy
- private project corpus handling

## Documentation

- [Architecture Decision Records](docs/adrs)
- [Design Notes](docs/design)
- [Plans](docs/plans)
