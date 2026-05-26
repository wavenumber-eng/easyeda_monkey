# Public Repo Bootstrap Plan

## Goal

Stand up `easyeda-monkey` as a standalone public package before wiring it into
`altium-cruncher`.

## Completed Bootstrap Items

- [x] Copy parser source, local fixtures, and tests from the existing package.
- [x] Remove local workspace path assumptions from public docs.
- [x] Add AGPL license, contribution guide, issue template, and PR template.
- [x] Add Rack `L99_signoff` coverage for version, changelog, and source
      quality.
- [x] Add CI across Windows, Linux, and macOS.
- [x] Add a PyPI release workflow using Trusted Publishing.
- [x] Add build, `twine check`, and installed-wheel smoke coverage.
- [x] Add ruff lint checking to local and CI signoff.
- [x] Add pyright type checking to local and CI signoff.

## Before First Release

- [ ] Push `main` and verify GitHub CI passes.
- [ ] Configure PyPI Trusted Publishing for
      `wavenumber-eng/easyeda_monkey`.
- [ ] Create tag `easyeda-monkey/v2026.5.26`.
- [ ] Publish the GitHub release after final approval.
- [ ] Verify `pip install easyeda-monkey==2026.5.26` from a clean venv.

## Follow-Up Work

- [ ] Reduce inherited parser complexity baseline without changing EasyEDA
      format semantics.
- [ ] Add contract tests for any new public parser methods or data model
      fields.
- [ ] Add JSON format design docs before exposing downstream machine-readable
      command output through `altium-cruncher`.
- [ ] Link `altium-cruncher` to the public `easyeda-monkey` package once this
      repo has a published release.
