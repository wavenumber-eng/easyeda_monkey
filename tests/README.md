# EasyEDA Monkey Tests

The test suite exercises the public parser surface through package-owned saved
EasyEDA / LCSC API fixtures.

Rules:

- fixtures must be redistributable with the public repository
- no `WN_TEST_CORPUS` dependency is required for the current suite
- `input/`, `reference_output/`, and `output/` are the preferred case shape for
  future fixture families
- `output/` is transient and must not be committed

Quick start:

```powershell
uv run --extra test rack list
uv run --extra test rack run --all
```

Current active strata:

- `L0_foundation`: parser and fixture coverage
- `L99_signoff`: release, changelog, Python quality, CLI docs, API docs, and
  interface test ownership gates
