# Agent Guide

`easyeda-monkey` is a public Python package for EasyEDA / LCSC parser and
component-download primitives. Keep changes focused on parser fidelity, stable
CLI behavior, and downstream compatibility.

## Setup

Use `uv` for local development:

```bash
uv sync --all-extras
```

Commit `uv.lock`. Do not hand-edit it.

## Test And Signoff

Run the package signoff before release-facing changes:

```bash
uv run rack run --all
uv run python -m build
uv run twine check dist/*
```

## Architecture Boundaries

- The package preserves EasyEDA-native semantics.
- Format conversion policy belongs in downstream tools.
- The top-level CLI remains an orchestrator; each public command lives in its
  own module under `easyeda_monkey.cli_commands`.
- `docs/design/`, `docs/canonical_format/`, and `docs/contracts/` are durable
  release documentation.

## Release Rules

- `main` should represent the latest released/tagged source.
- Public changes should merge through PRs with required CI.
- Release publication should trigger validation and trusted PyPI publishing.
- Date-based versions are standard, for example `2026.6.4`.
- `CHANGELOG.md` and `docs/releases/<YYYY-MM-DD>.md` must mention the current
  package version.

## Local Secrets

Do not commit `.env` files, PyPI tokens, private corpora, or customer data.
PyPI publishing should use trusted publishing.

## Exceptions

Strict rules are the target. Current exceptions must be documented in
`docs/contracts/exceptions.json` and should ratchet down over time.
