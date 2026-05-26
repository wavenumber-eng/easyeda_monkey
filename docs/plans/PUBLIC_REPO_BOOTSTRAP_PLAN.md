# Public Repo Bootstrap Plan

## Goal

Stand up `easyeda-monkey` as a standalone public package before wiring it into
`altium-cruncher`.

## Completed Bootstrap Items

- [x] Copy parser source, local fixtures, and tests from the existing package.
- [x] Remove local workspace path assumptions from public docs.
- [x] Add MIT license, contribution guide, issue template, and PR template.
- [x] Add Rack `L99_signoff` coverage for version, changelog, and source
      quality.
- [x] Add CI across Windows, Linux, and macOS.
- [x] Add a PyPI release workflow using Trusted Publishing.
- [x] Add build, `twine check`, and installed-wheel test coverage.
- [x] Add ruff lint checking to local and CI signoff.
- [x] Add pyright type checking to local and CI signoff.
- [x] Push `main` to `wavenumber-eng/easyeda_monkey`.
- [x] Add first CLI command and registry-backed HTML design-document signoff
      rule.
- [x] Adopt MIT licensing for the public package.
- [x] Document `uv tool install` as the preferred CLI install path and `uv` as
      the development/test workflow.
- [x] Add ADR-003 for per-command CLI modules and dependency-minimization
      review discipline.
- [x] Make Rack the primary local signoff gate and move ruff/pyright under
      L99.
- [x] Add API design-doc signoff for dataclasses, major interfaces, and Rack
      test ownership.

## Current Blocker

GitHub reports the `CI` and `Publish` workflows as active and repository
Actions permissions as enabled, but no run was created for the first two pushes
to `main`. Manual dispatch for `CI` also failed with GitHub HTTP 500 on
2026-05-26. Tracked as
https://github.com/wavenumber-eng/easyeda_monkey/issues/1.

Local release-equivalent checks pass on Windows:

- `uv run --extra test rack run --all`
- `uv run --extra test python -m build`
- `uv run --extra test twine check dist\*`
- `uv run --extra test python tests/support_scripts/install_test.py`

## Before First Release

- [ ] Resolve GitHub Actions run creation / manual dispatch failure.
- [ ] Verify GitHub CI passes on Windows, Linux, and macOS.
- [ ] Configure PyPI Trusted Publishing for
      `wavenumber-eng/easyeda_monkey`.
- [ ] Create tag `easyeda-monkey/v2026.5.26`.
- [ ] Publish the GitHub release after final approval.
- [ ] Verify `uv tool install easyeda-monkey==2026.5.26` and
      `pip install easyeda-monkey==2026.5.26` from clean environments.

## Follow-Up Work

- [ ] Reduce inherited parser complexity baseline without changing EasyEDA
      format semantics.
- [ ] Add contract tests for any new public parser methods or data model
      fields.
- [ ] Add JSON format design docs before exposing downstream machine-readable
      command output through `altium-cruncher`.
- [ ] Link `altium-cruncher` to the public `easyeda-monkey` package once this
      repo has a published release.
