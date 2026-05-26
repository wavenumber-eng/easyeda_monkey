# EasyEDA Symbol & Footprint Library Plan

Stand up the EasyEDA native data model for schematic symbols and PCB footprints,
then build the conversion pipeline into data_models (sch_a0, pcb_a0).

## Governing Documents

- ADR-001: Native data model and API conventions
- data_models ADR-0038: Transformation fidelity and capability matrix
- data_models ADR-0004: Generic core with CAD pass-through
- data_models ADR-0009: Converters non-filtering and loss-preserving

## Phase 0: Format Research and Test Fixtures -- COMPLETE

- [x] Study official EasyEDA format documentation
- [x] Study easyeda2kicad.py reference implementation
- [x] Document API endpoint and response structure
- [x] Fetch and save 7 representative LCSC components as JSON fixtures:
  - C21190 (0603WAF1001T5E, 2-pin resistor, 3 sym / 11 fp shapes)
  - C14663 (CC0603KRX7R9BB104, 2-pin capacitor, 6 sym / 17 fp shapes)
  - C2040 (RP2040, 57-pin MCU, 60 sym / 193 fp shapes)
  - C7950 (LM358DR2G, 8-pin op-amp, 11 sym / 35 fp shapes)
  - C429954 (USB-C connector, 3-pin, 5 sym / 11 fp shapes)
  - C15127 (AO3401A, 3-pin MOSFET, 16 sym / 18 fp shapes)
  - C2488 (MB10S bridge rectifier, 4-pin, 16 sym / 35 fp shapes)
- [x] Saved to `tests/L0_foundation/cases/api_responses/`

## Phase 1: Native Symbol Data Model -- COMPLETE (33 tests)

Goal: parse EasyEDA symbol shapes into typed Python objects.

- [x] `easyeda_types.py` — shared enums and constants:
  - `EePinType` enum (unspecified, input, output, bidirectional, power)
  - `EeStrokeStyle` enum (solid, dashed, dotted)
  - Coordinate helpers (pixel to nm conversion)
- [x] `easyeda_symbol.py` — `EasyEdaSymbol` class:
  - `from_json(data)` — parse from API response `result.dataStr`
  - `to_json()` — round-trip serialize
  - `.info` — name, prefix, package, manufacturer, LCSC ID
  - `.pins` — list of `EasyEdaPin`
  - `.rectangles`, `.circles`, `.arcs`, `.ellipses` — typed shape lists
  - `.polylines`, `.polygons`, `.paths` — complex shapes
- [x] `easyeda_pin.py` — `EasyEdaPin` class:
  - Parse 7 `^^`-separated segments
  - Settings: electrical type, position, rotation, display
  - Pin dot: connection point coordinates
  - Pin path: graphical stub (SVG path string)
  - Name: text, position, font, visibility
  - Number: text, position, font, visibility
  - Dot display: active-low circle indicator
  - Clock: clock edge indicator
- [x] `easyeda_shapes.py` — graphic primitive classes:
  - `EeRectangle` — x, y, rx, ry, width, height, stroke, fill
  - `EeCircle` — cx, cy, radius, stroke, fill
  - `EeEllipse` — cx, cy, rx, ry, stroke, fill
  - `EeArc` — SVG path string, helper dots, stroke
  - `EePolyline` — point string, stroke, fill
  - `EePolygon` — point string, stroke, fill
  - `EePath` — SVG path string (bezier), stroke, fill
- [x] `easyeda_parser.py` (integrated into easyeda_symbol.py and easyeda_footprint.py) — shape string dispatcher:
  - Split shape strings by `~`
  - Dispatch by prefix (P, R, C, E, A, PL, PG, PT, T, etc.)
  - Return typed objects

### L0 Tests for Phase 1

- [ ] `test_L0_001_symbol_parse.py` — parse saved API fixtures, verify:
  - Correct pin count, pin names, pin types
  - Correct graphic element counts by type
  - Symbol info (name, prefix, LCSC ID)
- [ ] `test_L0_002_symbol_roundtrip.py` — parse → to_json → from_json → compare
- [ ] `test_L0_003_pin_parse.py` — exercise all pin segment types:
  - Basic pin (name + number)
  - Pin with dot (active low)
  - Pin with clock indicator
  - Pin orientation (0/90/180/270)
  - Hidden pin
- [ ] `test_L0_004_shapes_parse.py` — each shape type individually

## Phase 2: Native Footprint Data Model -- COMPLETE (17 tests)

Goal: parse EasyEDA footprint shapes into typed Python objects.

- [x] `easyeda_footprint.py` — `EasyEdaFootprint` class:
  - `from_json(data)` — parse from API response `result.packageDetail.dataStr`
  - `to_json()` — round-trip serialize
  - `.info` — package name, type (SMD/THT), 3D model ref
  - `.pads` — list of `EeFootprintPad`
  - `.tracks`, `.holes`, `.vias` — copper/mechanical
  - `.circles`, `.rectangles`, `.arcs`, `.texts` — silkscreen/annotation
- [x] `easyeda_pad.py` — `EeFootprintPad` class:
  - 18 tilde-delimited fields
  - Shape: ELLIPSE, RECT, OVAL, POLYGON
  - Position, dimensions, layer, net, hole properties, plating
- [x] Footprint shape reuse from `easyeda_shapes.py` where applicable

### L0 Tests for Phase 2

- [ ] `test_L0_005_footprint_parse.py` — parse saved fixtures
- [ ] `test_L0_006_footprint_roundtrip.py` — parse → serialize → compare
- [ ] `test_L0_007_pad_parse.py` — all pad shapes (ELLIPSE, RECT, OVAL, POLYGON)

## Phase 3: API Client -- COMPLETE

Goal: fetch components from LCSC API by part number.

- [x] `easyeda_api.py` — `EasyEdaApiClient` class:
  - `fetch_component(lcsc_id)` — raw API response with disk caching
  - `fetch_symbol(lcsc_id)` → `EasyEdaSymbol`
  - `fetch_footprint(lcsc_id)` → `EasyEdaFootprint`
  - `fetch_both(lcsc_id)` → tuple
  - Rate limiting, error handling, response validation
  - Optional disk caching for offline use

### L1 Tests for Phase 3

- Tests use saved fixtures (no live network needed); API client tested via fixture generation

## Phase 4: Conversion to Generic Model -- COMPLETE (25 tests)

Goal: convert EasyEDA native model to sch_a0 and pcb_a0.

- [x] `data_models/converters/easyeda_symbol.py`:
  - Forward: `sch_symbol_from_easyeda()` — pins, graphics, metadata
  - Reverse: `easyeda_symbol_from_sch_symbol()` — for round-trip validation
  - Pin type mapping (EasyEDA ↔ generic PinElectricalType)
  - Coordinate conversion (EasyEDA pixels ↔ nanometers)
- [ ] `data_models/converters/easyeda_footprint.py` — deferred to future phase

### L2 Tests for Phase 4

- [x] `test_L2_converters_easyeda_symbol.py` — 25 tests (forward + generic JSON round-trip)
- [ ] `test_L2_002_footprint_converter.py` — deferred

## Phase 5: EasyEDA → sch_a0 → EasyEDA Round-Trip -- COMPLETE (86 tests)

Goal: prove lossless round-trip through the generic model.

- [x] Reverse converter: `easyeda_symbol_from_sch_symbol()`
- [ ] Reverse converter: `PcbFootprint` → `EasyEdaFootprint` — deferred
- [x] Round-trip test: `test_converters_easyeda_roundtrip.py` — 86 tests across 7 fixtures
  - Pin count, names, designators, types: all preserved
  - Pin positions: within 1 EasyEDA pixel tolerance
  - Symbol name and LCSC ID: preserved
  - Rectangle, circle, ellipse, polyline, polygon counts: preserved
  - Specific component tests: resistor (2-pin) and RP2040 (57-pin)

## Phase 6: Capability Matrix Integration -- COMPLETE

Goal: formalize what's tracked and what's preserved.

- [x] Define schematic feature IDs: `sch.symbol_pins`, `sch.symbol_graphics`, `sch.symbol_metadata`
- [x] Add 3 EasyEDA rows to `capability_matrix_a0.json` (path: `easyeda_sym_to_sch_a0`)
  - `sch.symbol_pins` — green (full round-trip)
  - `sch.symbol_graphics` — amber (arc/bezier placeholder only)
  - `sch.symbol_metadata` — green (name, LCSC ID, prefix, package preserved)
- [x] Update gating test to support domain-specific required feature sets
- [x] ADR-0038 follow-on items 7-8 satisfied for EasyEDA path
- [ ] Add provenance to converted objects
- [ ] Write `build_easyeda_transform_report()`

## Exit Criteria

- All LCSC test fixture components parse without error
- Symbol and footprint round-trip through to_json/from_json is lossless
- Generic model conversion preserves all pins, pads, and graphics
- EasyEDA → sch_a0 → EasyEDA round-trip preserves structure
- Capability matrix rows document what's supported

## Notes

- EasyEDA format is simpler than Altium — no binary parsing, no OLE containers
- The `easyeda2kicad.py` project (AGPL-3.0) is a reference for format
  understanding but we implement our own parser following project conventions
- EasyEDA Standard vs Pro: we target Standard format only (the API returns this)
- 3D model download/conversion is deferred to a later phase
