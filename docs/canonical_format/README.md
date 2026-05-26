# EasyEDA Canonical Format Notes

This folder holds stable EasyEDA format and API notes that are safe to treat as
public reference material. Raw research and reverse-engineering notes belong in
`docs/research/` until their useful findings are promoted here, into
`docs/design/`, or into machine-readable contracts.

## References

- Official EasyEDA document format:
  <https://docs.easyeda.com/en/DocumentFormat/EasyEDA-Document-Format/index.html>
- LCSC component API pattern:
  `https://easyeda.com/api/products/{LCSC_ID}/components?version=6.4.19.5`
- Fixture-backed parser coverage lives under `tests/L0_foundation/` and records
  the current executable contract for symbols, footprints, SVG paths, pads, and
  3D model references.

## Current Scope

The package currently models the EasyEDA/LCSC component payloads needed for:

- schematic symbols;
- PCB footprints;
- SVG path geometry embedded in symbols and footprints;
- pad, hole, via, and track primitives;
- 3D model reference metadata.

When a new payload field or primitive becomes a stable parser contract, document
the format here or in a more specific canonical-format file before relying on
it as public behavior.
