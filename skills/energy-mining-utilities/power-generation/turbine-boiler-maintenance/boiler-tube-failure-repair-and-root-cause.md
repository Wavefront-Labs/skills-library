---
id: energy-mining-utilities.power-generation.turbine-boiler-maintenance.boiler-tube-failure-repair-and-root-cause
name: boiler-tube-failure-repair-and-root-cause
category: energy-mining-utilities
field: power-generation
product: turbine-boiler-maintenance
tags: [turbine-boiler-maintenance, power-generation, boiler-tube-failure, btf, tube-leak, waterwall, superheater, reheater, economiser, fish-mouth, window-opening, creep, long-term-overheat, short-term-overheat, hydrogen-damage, fly-ash-erosion, sootblower-erosion, corrosion-fatigue, dissimilar-metal-weld, pad-weld, window-weld, tube-replacement, radiography, hydrostatic-test, forced-outage, root-cause-analysis, ndt]
level: advanced
status: draft
description: "Handle a boiler tube leak: find it, read the failure shape, take samples, repair by tube replacement, prove it with NDT and hydrotest, and fix the root cause so it doesn't come back."
sources: ["EPRI boiler tube failure mechanism concepts (public summaries)", "ASME BPVC Section I (repair principles, paraphrased)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Boiler tube failure: repair and root cause

**Goal:** turn a tube leak forced outage into a repair that holds *and* a root-cause
finding that stops the next one. Boiler tube failures are a leading cause of forced
outages on fossil units, and most repeat because the repair team replaced the tube and
moved on.

## 1. Find and confirm the leak
- Early signs before the outage: rising makeup water demand, acoustic leak detection
  alarm, furnace pressure disturbance, steam noise at a peephole.
- Take the unit off on a planned basis if it's safe; a small leak erodes neighbouring
  tubes (steam cutting), so a delayed outage often means more tubes.
- After cool-down and gas-free/entry permits: locate by visual walk with lighting,
  air test or a low-pressure hydro to show weeping.

## 2. Read the failure before you cut
Photograph in place, record location (elevation, tube row/number from a fixed
datum), and identify the damage form:
- **Thick-lipped, longitudinal, small opening, oxide scale heavy** → long-term
  overheat / creep. Look for scale build-up, flow restriction, design overheating.
- **Thin-lipped "fish-mouth" rupture with wall thinning** → short-term overheat
  (flow loss, blockage at start-up, low drum level).
- **Thick-edged window blown out of the tube, brittle** → hydrogen damage, usually
  from an acidic chemistry upset under deposits (link the chemistry log).
- **Thinned, polished, flattened wall** on the gas side → fly-ash or sootblower
  erosion.
- **Cracks transverse to the tube near attachments** → corrosion fatigue from
  thermal cycling or restrained expansion.
- **Crack at a ferritic-austenitic weld** → dissimilar-metal weld failure (common in
  superheater/reheater sections).

## 3. Sample and measure
- Cut out a sample including the failure plus some length either side; mark flow
  direction and fireside. Send for metallurgical analysis (wall thickness, oxide
  thickness, microstructure, deposit weight density).
- Measure wall thickness on neighbours by ultrasonic thickness gauging; map erosion.
- Check for blockage (debris, a forgotten plug, a weld drip) in the affected circuit.

## 4. Repair
- Preferred: **replace a full tube section** (typically at least ~300 mm / 12 in
  beyond damage) with material to the original specification, by qualified welders on
  an approved procedure (WPS/PQR, Section I or local code).
- Pad welds and window patches are temporary measures only, where code and the
  insurer/authority allow — record them for permanent repair next outage.
- Preheat/PWHT for the material grade (e.g. P22, P91 have strict heat-treatment
  regimes — P91 in particular is unforgiving).
- NDT: radiography or phased-array UT of each new weld; visual of fit-up and root.
- **Hydrostatic test** per code and plant procedure before return to service, with an
  authorised inspector where required.

## 5. Close the loop
- Root cause written: mechanism + driver (chemistry, design, operation, maintenance).
- Corrective action for the *driver*: sootblower lance alignment, chemistry
  control, flow restriction removal, support repair.
- Extend inspection to sister locations — the same mechanism is usually present
  elsewhere in the same circuit.

## Gotchas
- Replacing only the leaking tube while neighbours are at 60 % wall guarantees another
  outage. Measure around it.
- Debris left after maintenance (rags, welding rods) causes short-term overheats on
  start-up; foreign material exclusion matters.
- Uncertain: lengths, margins and NDT requirements depend on code, jurisdiction and
  insurer — confirm with the plant engineer and authorised inspector.

## Verify
- [ ] Failure photographed, located and classified before cutting.
- [ ] Sample sent for metallurgy; neighbours UT-gauged.
- [ ] Repair welds made to an approved procedure, heat-treated and NDT-accepted.
- [ ] Hydrotest passed and recorded.
- [ ] Root cause and driver-level corrective action documented; sister locations inspected.
