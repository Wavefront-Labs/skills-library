---
id: engineering-technology.chemical-engineering.piping-instrumentation.level-measurement-selection
name: level-measurement-selection
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-instrument-selection, level-measurement-selection, level-measurement, differential-pressure-level, radar-level]
level: practitioner
status: draft
description: "Select a level instrument: differential pressure, guided wave radar, radar, displacer, with density and interface effects."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Level measurement selection

**Goal:** Select a level instrument: differential pressure, guided wave radar, radar, displacer, with density and interface effects.

## Steps
1. Define the range, the fluid, the density variations, interface needs, foam, vapour and the vessel internals.
2. Differential pressure transmitters are simple but depend on the density, and the wet or dry leg needs attention.
3. Radar and guided wave radar are independent of density and good for most liquids; guided wave radar can measure an interface.
4. Displacers suit interface duties and clean liquids in cages; check the density change effect.
5. Use independent instruments for the safety functions and the control, and plan the external chambers and the isolation.

## Gotchas
- Level readings in boiling or foaming service need care.
- For safety trips follow the SIS design rules.

## Verify
- [ ] Calibration range matches the vessel taps.
- [ ] Density effect is calculated at the extremes.
