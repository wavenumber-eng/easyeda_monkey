# ADR-004: Interface Design Documentation And Rack Ownership

## Status

Accepted.

## Context

Dataclasses and major interfaces become long-lived contracts quickly. A class
can pass unit tests while still leaving future maintainers unclear about why it
exists, where its boundary is, or what behavior counts as working.

The test system already uses Rack strata as the release gate, so interface
documentation should point back to Rack-owned tests instead of separate ad hoc
checklists.

## Decision

Every public dataclass and major interface requires design documentation under
`docs/design/api/`.

Each interface design section must include:

- rationale for why the interface exists;
- purpose and ownership boundary;
- test requirements;
- a working definition;
- Rack stratum and test target metadata.

L99 signoff scans source dataclasses and the major-interface list, then fails
if any required interface lacks design documentation.

L99 signoff also fails if an interface design section does not point to an
existing Rack stratum, existing test file, and test target. For nested data
classes, the exercising test may be an aggregate parser test when that is the
natural coverage boundary.

## Consequences

New dataclasses and major interfaces require docs and tests in the same change.

The first enforcement pass checks source, design docs, Rack strata, test files,
and declared test targets. A later refinement can inspect Rack result reports
directly if the report format provides a stable machine-readable target map.
