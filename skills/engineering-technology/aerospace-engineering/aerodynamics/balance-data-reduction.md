---
id: engineering-technology.aerospace-engineering.aerodynamics.balance-data-reduction
name: balance-data-reduction
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, wind-tunnel, aero-testing, balance-data, data-reduction, tare, balance-interaction, axis-transfer, uncertainty]
level: advanced
status: draft
description: "Reduce force-balance data to aerodynamic coefficients, covering tares, balance interactions, upflow, axis transfer and uncertainty."
sources:
  - "Barlow, Rae and Pope, Low-Speed Wind Tunnel Testing"
  - "AIAA S-071A, Assessment of Experimental Uncertainty with Application to Wind Tunnel Testing"
  - "Balance manufacturer manuals"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Balance data reduction

**Goal:** repeatable `CL`, `CD`, `Cm` from raw strain-gauge balance readings.

## Steps
1. **Zero and tares:** zero the balance with the model weight (weight tare) and record wind-off readings at each attitude; subtract.
2. **Apply the balance calibration matrix** including interaction terms (first- and second-order) to get loads in the balance axis.
3. **Rotate to body or wind axes:** normal/axial to lift/drag: `L = N cos(alpha) - A sin(alpha)`, `D = N sin(alpha) + A cos(alpha)`, using corrected alpha.
4. **Transfer moments** to the reference centre (moment reference point) using the balance-to-reference offsets.
5. **Non-dimensionalise** with corrected `q` (see wall-corrections skill), reference area, chord, span.
6. **Support tares and interference:** run with dummy support or image system to subtract support effects.
7. **Upflow and flow angularity:** run the model upright and inverted and halve the difference.

## Uncertainty
Propagate balance accuracy, pressure, temperature, geometry and angle uncertainties per AIAA S-071A; report repeatability from repeat polars.

## Gotchas
- Sign conventions differ between balances; verify with a calibration weight check.
- Base pressure correction for axial force with a sting-mounted model.
- Thermal drift of the gauges: allow warm-up and compare wind-off zero before and after the run.

## Verify
- [ ] Wind-off zero repeats within the balance repeatability specification.
- [ ] Inverted-model data agree after upflow correction.
