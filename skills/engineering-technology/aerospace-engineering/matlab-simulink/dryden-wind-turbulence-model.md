---
id: engineering-technology.aerospace-engineering.matlab-simulink.dryden-wind-turbulence-model
name: dryden-wind-turbulence-model
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, aerospace-blockset, dryden-turbulence, wind-turbulence, gust-model, mil-hdbk-1797, disturbance-modelling]
level: practitioner
status: docs-checked
description: "Add Dryden turbulence to a Simulink flight model with the Aerospace Blockset block, choose the spec version and intensities, and keep noise seeding reproducible."
sources:
  - "https://www.mathworks.com/help/aeroblks/drydenwindturbulencemodelcontinuous.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Dryden wind turbulence

**Goal:** realistic random gusts for handling and autopilot studies.

## Blocks
Aerospace Blockset has a **Dryden Wind Turbulence Model (Continuous)** block. Choose the military reference: `MIL-F-8785C` (default), `MIL-HDBK-1797` or `MIL-HDBK-1797B`; it affects the lateral and vertical turbulence scale lengths.

## Inputs
- Inputs: altitude `h`, aircraft speed `V` and a 3-by-3 direction cosine matrix `DCM` from flat Earth to body axes.
- Parameter: the measured wind speed at 6 m (`W20`, default 15) sets the low-altitude turbulence intensity.
- Four noise seeds as a vector `[ug vg wg pg]` (default `[23341 23342 23343 23344]`); set them explicitly.
- Outputs: `Vwind` (turbulence velocities) and `omega wind` (turbulence angular rates, rad/s), in body coordinates.

## Procedure
1. Pick a suitable solver for the continuous block.
2. Set the seed vector; vary it in Monte Carlo runs.
3. Feed the outputs to the wind inputs of the 6DOF block; verify frame conventions.
4. Compare RMS gust speed with the specification's expected value for the altitude and severity.

## Gotchas
- Seed duplication gives identical gusts.

## Verify
- [ ] Time history RMS of the gust components matches the expected sigma within statistical scatter over a long run.

## Checked
2026-11-01. Confirmed on the MathWorks Dryden continuous block page: specification options and default, W20 parameter and default, inputs h, V, DCM, four-seed vector and default, outputs Vwind and angular rates. Removed: the Discrete block, the units and intensity-level wording, the 1-cosine gust remark and the MIL-HDBK source (not on the page read).
Method: documentation only; no commands were run.
