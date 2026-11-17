---
id: engineering-technology.chemical-engineering.process-safety.relief-valve-sizing-vapour-and-liquid
name: relief-valve-sizing-vapour-and-liquid
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-relief-sizing, relief-valve-sizing-vapour-and-liquid, relief-valve-sizing, api-520, api-526, orifice-area, psv, discharge-coefficient, back-pressure-correction, safety-valve, critical-flow]
level: advanced
status: verified
description: "Size spring-loaded relief valves for vapour and liquid with API 520 Part I formulas, orifice letters per API 526, back-pressure correction and set-pressure basis."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relief valve sizing for vapour and liquid

**Goal:** the required effective discharge area and the standard orifice. Relief valve selection and sizing is safety-critical; formulas below are the commonly published US customary forms of API 520 Part I for screening and checking, to be verified against the current edition and by a qualified engineer, using the manufacturer's certified capacities for the final selection.

## Vapour or gas, critical (choked) flow
A = W / (C K_d P_1 K_b K_c) x sqrt(T Z / M)
with A in in^2, W in lb/h, P_1 the relieving pressure (set pressure plus overpressure, plus atmospheric) in psia, T in R, Z compressibility, M molecular weight, K_d the coefficient of discharge (typically 0.975 for gas valves and 0.65 for liquid valves (gated: unconfirmed, source is paywalled or blocked); use the manufacturer value), K_b the back-pressure correction factor (1 for conventional valves when back pressure is at or below about 10% of set pressure; use the vendor's curve for balanced bellows valves), K_c the rupture disc combination factor (1 without a disc, 0.9 with one if no data), and C = 520 sqrt( k (2/(k + 1))^((k + 1)/(k - 1)) ) with k the ideal gas specific heat ratio. Flow is critical when P_back/P_1 is below (2/(k + 1))^(k/(k - 1)) (about 0.53 for k = 1.4; recomputed: 0.528, and C = 356 for k = 1.4).

## Liquid
A = Q / (38 K_d K_w K_c K_v) x sqrt(G/(P_1 - P_2)), with Q in gpm, G specific gravity, P_1 and P_2 relieving and back pressure in psig, K_d about 0.65 (liquid valves), K_w the back-pressure correction for balanced bellows valves, K_v the viscosity correction.

## Procedure
1. Take the relief load (W or Q) from the governing scenario, at relieving pressure and temperature.
2. Compute the required A; select the next larger standard orifice from API 526: D, E, F, G, H, J, K, L, M, N, P, Q, R, T with effective areas of (API 526 values, (gated: unconfirmed, source is paywalled or blocked)) 0.110, 0.196, 0.307, 0.503, 0.785, 1.287, 1.838, 2.853, 3.60, 4.34, 6.38, 11.05, 16.0 and 26.0 in^2 respectively.
3. Check the inlet pressure drop (the 3% rule: inlet line loss at rated capacity no more than 3% of set pressure, to avoid chatter) and the outlet back pressure (built-up plus superimposed).
4. Check reaction forces and noise, discharge location and the fate of the discharge.
5. Document in a data sheet with the basis and use the vendor's certified coefficient to finalise.

## Gotchas
- Using the fluid properties at normal operating conditions instead of relieving conditions.
- Conventional valves are sensitive to back pressure; choose balanced bellows or pilot-operated when back pressure is variable or high.
- Letter orifice areas are effective areas, not the physical ones.

## Verify
- [ ] Independent hand calculation reproduces the software result.
- [ ] Inlet loss at or below 3% of set pressure at rated flow.
