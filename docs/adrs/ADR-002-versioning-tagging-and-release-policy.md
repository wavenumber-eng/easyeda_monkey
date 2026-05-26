# ADR-002: Versioning, Tagging, and Release Policy

## Status

Accepted.

## Context

`easyeda-monkey` is a public package and will be consumed by downstream tools
such as `altium-cruncher`. Releases need to be reproducible from Git tags and
automatable through GitHub Actions.

## Decision

The package uses date-based versions in `YYYY.M.DD` form. For example, the
May 26, 2026 release is `2026.5.26`.

Release tags use the package name and version:

```text
easyeda-monkey/v2026.5.26
```

Every release must include:

- a matching `pyproject.toml` version
- a matching `easyeda_monkey.__version__`
- a matching `CHANGELOG.md` entry
- a passing pytest suite
- a passing Rack suite
- a passing Python signoff baseline check
- successful source distribution and wheel builds
- successful `twine check`
- an installed-wheel smoke test

GitHub Actions is the preferred release path once PyPI Trusted Publishing is
configured for this repository.

## Consequences

Downstream repos can pin exact package dates and exact Git tags. Old names or
pre-public internal package flows are not part of the public contract.
