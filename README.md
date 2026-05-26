# EasyEDA Monkey

`easyeda_monkey` is a small Python package for reading EasyEDA / LCSC component
data into typed Python objects. It also exposes a small diagnostic CLI for
package-local fetch and inspection workflows.

Current scope:

- EasyEDA / LCSC component API responses
- schematic symbols
- PCB footprints
- 3D model references and URL extraction
- SVG path parsing helpers

The package is intentionally focused on parsing and close-to-format data
models. Larger workflow commands and conversion applications should live in
downstream tools such as `altium-cruncher`.

## Install

Install `uv` first if it is not already available:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

On macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For the command-line tool, use `uv tool install` so the executable is installed
in an isolated tool environment and exposed on PATH:

```powershell
uv tool install easyeda-monkey
uv tool update-shell
easyeda-monkey --version
```

For library use inside an existing Python environment:

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
uv run --extra test rack run --all
```

Rack is the primary local gate. L99 signoff runs release metadata checks,
Python signoff, CLI design-doc checks, API design-doc checks, ruff, and pyright.

## CLI

The package installs the `easyeda-monkey` console script.

```powershell
easyeda-monkey --version
easyeda-monkey fetch-part C21190
easyeda-monkey fetch-part C21190 --cache-dir .cache/easyeda --output C21190.summary.json
```

The top-level CLI module is only an orchestrator. Each public subcommand lives
in its own `easyeda_monkey.cli_commands` module, even when the command is
small.

## Design And Test Docs

`docs/` is the source of truth for architecture, tests, and contracts. The
master design entry point is [docs/design/index.html](docs/design/index.html).

Every public CLI command must have a matching HTML design document under
`docs/design/cli/`. The filename must match the command name, and signoff fails
when a registered command is missing its design document.

Commands that accept config files must also define a machine-readable contract
and validation tests before release.

New public features, commands, and external dependencies need explicit
justification in the commit, PR, or linked plan. Prefer the standard library
and existing dependencies unless a new dependency has a clear install,
licensing, and maintenance case.

Every public dataclass and major interface needs design documentation under
`docs/design/api/`. L99 signoff fails when interface docs or Rack test
ownership are missing.

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

## License

MIT.
