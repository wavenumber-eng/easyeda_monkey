# Contributing

`easyeda-monkey` accepts direct public pull requests once CI is enabled.

Use `uv` for local development and test commands. Public CLI install
documentation should prefer `uv tool install easyeda-monkey`; use
`pip install easyeda-monkey` when documenting library use inside an existing
Python environment.

Before opening a PR:

1. Keep changes focused on one parser, model, fixture, contract, or
   infrastructure slice.
2. Add or update tests for every public parser/API behavior change.
3. Update docs for public interfaces, JSON behavior, or fixture contracts.
4. Add or update `docs/design/` HTML for every public CLI command.
5. Justify every new public feature, command, and dependency in the commit,
   PR, or linked plan.
6. Run package tests and signoff locally.

Minimize external dependencies. This is a general Wavenumber tool convention,
not only an EasyEDA Monkey rule. A new dependency must explain why the standard
library and existing project dependencies are not enough, whether it is
runtime/optional/test-only, its license compatibility, and the expected
packaging impact.

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

## CLI Structure Rules

The top-level CLI module is an orchestrator. It creates the root parser,
registers commands, handles global options, and dispatches command handlers.

Every public subcommand must live in its own module under
`easyeda_monkey.cli_commands`, even if the first implementation is small. The
command module owns command-specific arguments, behavior, output formatting,
and command-specific imports.

This convention is documented in
`docs/adrs/ADR-003-cli-command-and-dependency-discipline.md`. L99 signoff
checks the parts that are mechanically enforceable; reviewers can still reject
a PR when command or dependency justification is missing.
