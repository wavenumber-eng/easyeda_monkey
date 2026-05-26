# ADR-001: EasyEDA Native Data Model and API Conventions

## Status

Accepted.

## Date

2026-03-18.

## Context

`easyeda-monkey` parses EasyEDA schematic symbols and PCB footprints from the
LCSC / JLCPCB component API. Downstream tools can then convert that typed native
model into other EDA formats.

The EasyEDA format is JSON-based with tilde-delimited shape strings. It is
smaller than Altium binary formats, but still needs a dedicated native model to
preserve source-format details before conversion.

## Decision

### 1. EasyEDA-Native Data Model First

The package exposes typed Python classes that represent EasyEDA JSON semantics:

- tilde-delimited string parsing
- EasyEDA coordinate systems
- EasyEDA-specific shape prefixes
- symbol pin `^^` segment parsing
- footprint pad, track, hole, via, and 3D model references

Downstream conversion policy is intentionally outside this package.

### 2. Public Construction And Serialization

Primary public entry points:

- `EasyEdaSymbol.from_json(data_or_path)`
- `EasyEdaFootprint.from_json(data_or_path)`
- `EasyEdaApiClient.fetch_symbol(lcsc_id)`
- `EasyEdaApiClient.fetch_footprint(lcsc_id)`
- `EasyEdaApiClient.fetch_both(lcsc_id)`

Serialization methods:

- `.to_json()` returns a round-trippable dict.
- `.save(path)` writes JSON to disk.

The direct dataclass constructor remains available for advanced/internal use,
but parsing should go through `from_json` or the API client.

### 3. API Client Is Separate From The Data Model

`easyeda_api.py` handles HTTP fetches from the LCSC API. Data model classes
accept parsed dictionaries or saved JSON fixture paths and do not perform HTTP
requests themselves.

### 4. Minimal Core Dependencies

Core parsing uses the Python standard library. The API client uses `requests`.
The package avoids heavy model frameworks so downstream tools can embed it
without pulling in large application stacks.

### 5. Scope

In scope:

- schematic symbols
- PCB footprints
- SVG path parsing helpers
- 3D model references and download URLs

Out of scope for the initial public package:

- full EasyEDA schematic document support
- EasyEDA Pro
- direct Altium/KiCad conversion commands
- authoring/building EasyEDA components

## Consequences

Positive:

- Native model preserves source-format details for round-trip tests.
- Saved API fixture tests do not require network access.
- Downstream converters get a small parser dependency.

Tradeoffs:

- Format conversion remains the responsibility of downstream tools.
- Some inherited parser functions are complex and tracked in the signoff
  baseline until they can be split safely.

## Source Anchors

- EasyEDA format docs: https://docs.easyeda.com/en/DocumentFormat/EasyEDA-Document-Format/index.html
- Reference implementation studied for format behavior: https://github.com/uPesy/easyeda2kicad.py
- LCSC API shape: `https://easyeda.com/api/products/{LCSC_ID}/components?version=6.4.19.5`
