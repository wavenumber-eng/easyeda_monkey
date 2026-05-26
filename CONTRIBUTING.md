# Contributing

`easyeda-monkey` accepts direct public pull requests once CI is enabled.

Before opening a PR:

1. Keep changes focused on one parser, model, fixture, contract, or
   infrastructure slice.
2. Add or update tests for every public parser/API behavior change.
3. Update docs for public interfaces, JSON behavior, or fixture contracts.
4. Add or update `docs/design/` HTML for every public CLI command.
5. Run package tests and signoff locally.

Expected local checks:

```powershell
uv run --extra test pytest
uv run --extra test rack run --all
uv run --extra test python scripts\py_signoff.py --root . --baseline scripts\py_signoff_baseline.json
uv run --extra test ruff check .
uv run --extra test pyright src\py tests
```

Release decisions, compatibility policy, and public contract changes should be
recorded in `docs/adrs/`.

## Design Documentation Rules

`docs/` owns architecture, test, and contract documentation. `docs/design/`
contains human-readable and machine-inspectable HTML design docs.

Every public CLI command requires:

- a command registry entry in code;
- a matching `docs/design/cli/<command>.html` file;
- a link from `docs/design/cli/index.html`;
- usage, invocation, argument, output, and test sections.

Signoff fails when those links are missing. Commands with config files also
need a machine-readable contract and validation tests.
