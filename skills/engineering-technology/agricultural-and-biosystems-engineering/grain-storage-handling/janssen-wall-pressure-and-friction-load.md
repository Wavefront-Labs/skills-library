---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.janssen-wall-pressure-and-friction-load
name: janssen-wall-pressure-and-friction-load
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, janssen, silo-loads, bin-structural-design, wall-pressure, lateral-pressure-ratio, wall-friction, asabe-ep433, eurocode-silos]
level: practitioner
status: verified
description: "Calculate vertical and lateral grain pressures and wall friction load in a silo with Janssen's equation, and see which design codes apply to the structural check."
sources:
  - "Sinha & Muir, Grain Storage: Part of a System"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "Eurocodes, JRC (https://eurocodes.jrc.ec.europa.eu/EN-Eurocodes/eurocode-1-actions-structures)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Janssen wall pressure and friction load

**Goal:** pressures that wall, hopper and foundation must carry.

## Janssen equations
For a bin with cross-section area A and perimeter U, hydraulic radius `R = A / U`, grain unit weight gamma, lateral pressure ratio K (horizontal/vertical pressure) and wall friction coefficient mu at depth z below the top of the stored grain:

- Vertical pressure `p_v = (gamma R / (mu K)) (1 - exp(-mu K z / R))`
- Horizontal pressure `p_h = K p_v`
- Wall friction load per unit perimeter `= mu p_h`
- The formula satisfies the force balance dp_v/dz = gamma - mu K p_v / R with p_v tending to gamma R / (mu K) (checked numerically for gamma 7.5 kN/m3, R 1.5 m, mu 0.4, K 0.45: residual about 3e-9, limit 62.5 kPa).
- Total friction transferred to walls grows with depth until the vertical pressure saturates; the rest of the weight rests on the floor, not the full grain weight.
K typically about 0.4-0.5 for cereals (gated: unconfirmed, source is paywalled or blocked); mu depends on the wall material (smooth steel lower, corrugated sheet effectively grain-on-grain). Take K, mu and unit weight from the design code, not from memory.

## Codes
Design codes add load factors and extra cases (filling, discharge, eccentric discharge, thermal and wind): ASABE EP433 for farm bins (gated: unconfirmed, source is paywalled or blocked), Eurocode EN 1991-4 (Eurocode 1: Actions on structures, Part 4: Silos and tanks, per the JRC Eurocodes site), ACI 313 for concrete silos (gated: unconfirmed, source is paywalled or blocked). A structural engineer licensed for the jurisdiction must design and sign off bins; this skill is a check on the order of magnitude.

## Procedure
1. Determine R, K, mu and gamma from the bin and code.
2. Calculate profiles of p_h and p_v by depth and check against wall strength (hoop tension in corrugated steel).
3. Include the discharge pattern overpressure (see the flow-pattern skill).

## Verify
- [ ] The hoop tension from p_h x radius is checked against the sheet strength and bolt/seam capacity for the heaviest case.
