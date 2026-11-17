---
id: energy-mining-utilities.renewable-energy-field-operations.solar-pv-plant-operations.pv-string-and-inverter-fault-isolation
name: pv-string-and-inverter-fault-isolation
category: energy-mining-utilities
field: renewable-energy-field-operations
product: solar-pv-plant-operations
tags: [renewable-energy-field-operations, solar-pv-plant-operations, solar-farm, pv-plant, utility-scale-solar, string-fault, inverter-fault, central-inverter, string-inverter, combiner-box, string-fuse, dc-isolation, ground-fault, insulation-fault, riso, arc-fault, performance-ratio, pr, availability, specific-yield, soiling, tracker, mc4-connector, clamp-meter, dc-clamp, hot-spot, bypass-diode, pv-technician]
level: practitioner
status: draft
description: "Isolate underperformance in a utility-scale PV plant from monitoring to string: compare inverters and combiner currents, safely open DC circuits, find ground faults and dead strings."
sources:
  - "IEC 62446-1 (PV systems testing and documentation) and IEC 61724-1 (performance monitoring), concepts paraphrased"
  - "SolarPower Europe O&M Best Practice Guidelines, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PV string and inverter fault isolation

**Goal:** work down from "the plant is under-producing" to the specific inverter, combiner,
string or module — and fix it without drawing a DC arc.

## 1. Start in the monitoring
- Compare **specific yield** (kWh/kWp) or power normalised by DC capacity across inverters
  for the same hour. Equal irradiance → similar output; an outlier is your target.
- Check **performance ratio** against irradiance (POA pyranometer) and module temperature —
  a plant-wide drop with good irradiance points at soiling, curtailment, grid limits or
  a sensor fault, not a single failure.
- Inverter **event log**: ground fault/isolation (Riso low), DC overvoltage, grid faults,
  over-temperature derating (check filters/fans), communication loss.
- Trackers: stow position stuck → whole tracker row low at morning/evening.

## 2. Drill down to string level
- If combiner/string monitoring exists, compare string currents; a string at zero = open
  circuit (blown fuse, connector, cable); a string at a fraction = shading, soiling,
  bypass diodes or module failures.
- Without string monitoring: at the combiner, under similar irradiance, measure each
  string's current with a **DC clamp meter** — clamping doesn't require opening the circuit.
  Strings on the same inverter MPPT should agree within a few percent.

## 3. Safe DC work
DC from PV can't be switched off at the source while the sun shines.
- **Never open a string fuse holder or unplug a connector under load** — DC arcs sustain.
  Open the combiner's DC disconnect or stop the inverter (so current falls to zero) first,
  then verify with the clamp meter that current is zero before pulling fuses or connectors.
- Treat all conductors as live; insulated tools and gloves rated for the DC voltage
  (often 1000–1500 V DC); arc-flash PPE per your site's assessment.

## 4. Common faults and how to confirm
- **Blown string fuse:** check continuity of fuse off-load; replace with the same rating
  and find why it blew (often a reverse current from a ground fault or damaged module).
- **Ground fault / low insulation:** inverter trips mornings with dew. Isolate strings
  one at a time and insulation-test each (see the PV test-instruments skill
  `energy-mining-utilities.renewable-energy-field-operations.pv-test-instruments.iv-curve-tracing-and-insulation-testing-pv-strings`).
  Typical culprits: cable chafed on tracker or rail, rodent damage, water in connectors.
- **Connector failure:** mismatched brands of "MC4-compatible" connectors, poorly crimped
  connectors → hot, discoloured, melted. Thermal camera finds them under load.
- **Module faults:** hot spots, broken glass, failed bypass diodes (one-third of the module
  lost → string voltage low by ~ a third of a module's Voc).
- **Inverter internal:** IGBT, fan or filter faults, comms boards — vendor procedures.

## 5. Close out
Record the fault, location (block/inverter/combiner/string/module), lost energy estimate,
fix and parts. Re-check the string current against neighbours after repair.

## Gotchas
- Clamp meters read wrong near large DC busbars or when not zeroed; zero before each use.
- Comparing strings with different orientations, lengths or shading is meaningless.
- Moisture-related ground faults vanish by midday; test early morning.

## Verify
- [ ] Underperformance confirmed against irradiance and peers, not raw kW.
- [ ] Current verified zero before opening any DC connection.
- [ ] Root cause found, not just fuse replaced.
- [ ] String current matches peers after repair; monitoring alarm cleared.

*Uncertain:* PPE and DC isolation procedures are site-specific; follow your electrical
safety rules and the inverter maker's manual.
