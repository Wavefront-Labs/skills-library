---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.breguet-range-endurance
name: breguet-range-endurance
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, aircraft-performance, flight-performance, breguet-range, endurance, specific-range, cruise-performance, tsfc]
level: practitioner
status: verified
description: "Apply Breguet range and endurance equations for jet and propeller aircraft, choose optimum cruise conditions, and correct for climb, descent and reserves."
sources:
  - "Anderson, Aircraft Performance and Design"
  - "Raymer, Aircraft Design"
  - "Torenbeek, Synthesis of Subsonic Airplane Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Breguet range and endurance

**Goal:** range and endurance from fuel fraction and aerodynamic efficiency.

## Jet aircraft (thrust-specific fuel consumption `c` per unit thrust, in consistent units)
- Range: `R = (V/(c g)) (L/D) ln(W0/W1)` for constant `V` and `L/D` with `c` in kg/(N s) (or equivalent consistent units).
- Endurance: `E = (1/(c g)) (L/D) ln(W0/W1)`; maximum endurance at maximum `L/D`.
- Maximum range for a jet at constant altitude: `CL = sqrt(CD0/(3 K))`, i.e. maximum `CL^(1/2)/CD`.

## Propeller aircraft (`c_p` power-specific fuel consumption, propeller efficiency `eta_p`)
- Range: `R = (eta_p/c_p g) (L/D) ln(W0/W1)`; maximum at maximum `L/D`.
- Endurance: `E = (eta_p/c_p g) (CL^(3/2)/CD) sqrt(2 rho S) (1/sqrt(W1) - 1/sqrt(W0))`; maximum at `CL = sqrt(3 CD0/K)`.

## Practical corrections
- Add climb and descent segments (fuel and distance from the climb schedule), taxi, takeoff and landing allowances.
- Reserves: regulatory fuel reserves (diversion, contingency and final reserve) per the operating rules for the operation in question.
- Real cruise flies a step-climb or cruise-climb because `W` falls; use segment integration for accurate range.

## Procedure
1. Choose cruise `V`, altitude and `L/D` from the polar.
2. Compute `W1` from the fuel fraction after reserves.
3. Compute range; compare with a segmented mission analysis.

## Verify
- [ ] With `L/D = 17`, `c` = 0.6 lb/(lbf h) at 450 kt, and `W0/W1 = 1.25`, the range is about 2,845 nmi (computed: 450/0.6 x 17 x ln 1.25 = 2,845; check with units).
