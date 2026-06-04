# EasyEDA Design Notes

Design notes describe public interfaces, CLI behavior, data contracts, test
policy, and signoff policies that are too detailed for ADRs.

The master browser-readable entry point is [index.html](index.html). New public
CLI command designs belong under `docs/design/cli/` and must be linked from the
HTML index.

## Index

- [index.html](index.html) - master design index for humans and tooling
- [../architecture.html](../architecture.html) - architecture and package boundaries
- [../setup.html](../setup.html) - setup, release, and artifact policy
- [../contracts/command_manifest.v0.json](../contracts/command_manifest.v0.json) -
  machine-readable command contract manifest
- [cli/index.html](cli/index.html) - public CLI command design index
- [quality-signoff-status.md](quality-signoff-status.md) - current quality gate
  expectations and inherited baseline handling
