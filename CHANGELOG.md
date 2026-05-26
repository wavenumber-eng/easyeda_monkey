# Changelog

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
