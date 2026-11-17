---
id: engineering-technology.electrical-engineering.matlab-simulink.simscape-three-phase-grid-model
name: simscape-three-phase-grid-model
category: engineering-technology
field: electrical-engineering
product: matlab-simulink
tags: [electrical-engineering, grid-model, matlab, matlab-simulink, short-circuit-level, simscape-electrical, simscape-three-phase-grid-model, simulink, three-phase-source]
level: practitioner
status: draft
description: "Model a three-phase grid, source impedance and loads in Simscape Electrical and check short-circuit level and phase sequence."
sources:
  - "https://www.mathworks.com/help/sps/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Three-phase grid and source models in Simscape Electrical

1. **Source:** use a three-phase voltage source with the line-to-line RMS voltage, frequency and phase sequence; add series R-L representing the grid: `Z = V_LL^2 / S_sc` with `X/R` ratio (for example 10); `L = X/(2 pi f)`.
2. **Neutral and grounding:** connect the neutral explicitly (solid, resistance, or isolated); unconnected neutrals produce a singular network or floating voltage; add a high-value reference resistor only to resolve numerical problems and note it.
3. **Transformer and line blocks:** enter the percent impedance and X/R from the nameplate, the winding connection (vector group) and the core magnetisation if the study needs inrush; for lines use the pi-section for short lines or distributed parameters for long lines.
4. **Loads:** constant impedance (RLC), constant power (dynamic) or machine loads; constant-power loads cause negative incremental resistance that can destabilise the simulation.
5. **Measurement:** three-phase V/I sensors with the PLL or RMS blocks; use the same base for per-unit logging.
6. **Solver:** a Solver Configuration block per physical network; start with a local or variable-step solver for the grid and fixed-step for the real-time target (see simscape-converter-simulation).

**Caveat:** block names are described from general Simscape Electrical practice; confirm in the installed release (draft).

**Verify:** apply a bolted three-phase fault in the model and compare the fault current with `V/(sqrt(3) Zth)` from the source impedance.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
