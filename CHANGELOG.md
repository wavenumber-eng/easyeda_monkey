# Changelog

## 2026.9.11

- Support Python 3.12 through 3.14, allowing downstream tools to adopt Python 3.14.
- Test all three supported Python versions in CI and publish using Python 3.14.
- Pin Hatchling to 1.31.0 so release metadata remains compatible with the
  release validator.
- Preserve parser behavior, CLI arguments, and component bundle formats.

## 2026.6.4

- Align the public package structure with the Wavenumber Python standard:
  repository hygiene files, setup/architecture docs, release notes, and
  machine-readable command/interface/exception contracts.
- Add `easyeda-monkey version` and `python -m easyeda_monkey` support.
- Update CI and release workflows to native Node 24 GitHub Actions.
- Update release tooling to require `wn-rack>=2026.6.4`.
- Document current JSON `Any`, parser complexity, `src/py` layout, and Pyright
  mode exceptions for future ratcheting.

## 2026.5.26.2

- Add `easyeda-monkey download-part` to write a local EasyEDA/LCSC component
  bundle with raw API JSON, summary JSON, extracted 3D model metadata, and
  requested STEP/OBJ model files.
- Include 3D model reference counts and URLs in the compact `fetch-part`
  summary output.
- Add CLI design documentation and fixture-backed tests for the download
  workflow.

## 2026.5.26

- Bootstrap `easyeda-monkey` as a standalone public package from the existing
  EasyEDA parser package.
- Include EasyEDA/LCSC symbol, footprint, SVG path, pad, and 3D model reference
  parser coverage using package-local saved API fixtures.
- Add public CI, release workflow, Rack tests, Python signoff, package build
  checks, and clean install-test coverage.
- Add the `easyeda-monkey fetch-part` CLI and design-document signoff policy
  for registered commands.
- Use an MIT license for the public package.
- Document `uv tool install` as the preferred CLI install path and `uv` as the
  development/test workflow.
- Add ADR-003 for CLI command-module discipline and dependency minimization.
- Add API/interface design documentation with Rack test ownership checks.
- Move signoff and install-test helpers under `tests/support_scripts/`.
- Exclude developer-only planning and research docs from release artifacts
  while promoting stable EasyEDA format references into `docs/canonical_format/`.
