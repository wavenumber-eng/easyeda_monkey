# Changelog

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
