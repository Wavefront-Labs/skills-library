---
id: engineering-technology.electrical-engineering.circuit-analysis.impedance-combination
name: impedance-combination
category: engineering-technology
field: electrical-engineering
product: circuit-analysis
tags: [admittance, circuit-analysis, delta-wye-transformation, electrical-engineering, impedance, impedance-combination, phasor-analysis, series-parallel-reduction]
level: intro
status: draft
description: "Reduce series, parallel and delta-wye impedance networks in AC circuits and find equivalent impedance and admittance."
sources:
  - "https://www.ncees.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Series-parallel impedance reduction

1. Work in complex impedance: `Z_R = R`, `Z_L = j w L`, `Z_C = 1/(j w C)`. Series: `Z = Z1 + Z2`. Parallel: `Y = Y1 + Y2` with `Y = 1/Z`, or for two branches `Z = Z1 Z2/(Z1 + Z2)`.
2. **Delta to wye:** `Z_a = Z_ab Z_ca/(Z_ab + Z_bc + Z_ca)` (and cyclic); wye to delta: `Z_ab = (Z_a Z_b + Z_b Z_c + Z_c Z_a)/Z_c`. For a balanced delta, `Z_Y = Z_delta/3`.
3. **Example:** 10 ohm in series with the parallel of `j20` and `-j10` ohm: parallel part = `(j20)(-j10)/(j10) = -j20`, so `Z = 10 - j20 = 22.4 at -63.4 degrees` ohm (capacitive).
4. **Check:** magnitude of the equivalent and the angle sign: inductive loads have positive angle.
5. Use admittance for parallel work (power factor correction capacitors add `j w C`).

**Failure modes:** mixing frequency across sources; dropping the `j`; using arithmetic instead of complex division.

**Verify:** compute the current and compare the complex power `V I*` with the sum of branch dissipation.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
