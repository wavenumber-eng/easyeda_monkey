# ADR-003: CLI Command And Dependency Discipline

## Status

Accepted.

## Context

Python tools in this package family should stay small, easy to install, and
easy to review. `easyeda-monkey` is the first small public repo where this
convention is being codified, but the rule is intended for `altium-cruncher`
and future tool repos as well.

CLI commands can grow quickly if each command places parser setup, command
behavior, output formatting, and dependency imports into the top-level entry
point.

External dependencies also create long-term install, packaging, CI, and user
support costs. Even small dependencies need a reason to exist.

## Decision

The top-level CLI module is an orchestrator only. It may create the root
argument parser, register subcommands, handle global options, dispatch handlers,
and expose command metadata for docs/signoff.

Each public subcommand must live in its own module under
`easyeda_monkey.cli_commands`. The command module owns command-specific parser
arguments, handler implementation, output behavior, and command-specific
imports.

Every new public CLI command requires:

- a command module;
- a command registry entry;
- a matching `docs/design/cli/<command>.html` design document;
- tests for behavior and help/registration;
- a short justification in the commit, PR, or plan.

Every tool in this package family should minimize external dependencies. New
dependencies are accepted only when the commit or PR explains:

- why the dependency is needed;
- why the standard library or existing project dependencies are not sufficient;
- expected install/package impact;
- license compatibility;
- whether the dependency is required, optional, or test-only.

## Consequences

Reviewers can reject a command or dependency addition that lacks justification,
even when tests pass.

L99 signoff should enforce the parts that are mechanically checkable, including
the per-command module convention and matching design docs. Human review still
owns dependency justification quality.
