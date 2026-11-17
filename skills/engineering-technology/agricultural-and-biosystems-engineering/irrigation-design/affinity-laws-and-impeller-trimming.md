---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.affinity-laws-and-impeller-trimming
name: affinity-laws-and-impeller-trimming
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, affinity-laws, irrigation-pumping, pump-selection, impeller-trimming, pump-speed, pump-power]
level: practitioner
status: gated
description: "Apply pump affinity laws for speed and impeller diameter changes, estimate new flow, head and power, and know the limits of trimming and speed changes."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Affinity laws and impeller trimming

**Goal:** adjust an existing pump to a new duty point without buying a new one.

## Laws (speed N, diameter D)
- Flow `Q2 / Q1 = N2 / N1`
- Head `H2 / H1 = (N2 / N1)^2`
- Power `P2 / P1 = (N2 / N1)^3`
- For small impeller trims at constant speed: Q proportional to D, H to D^2, P to D^3 (approximate; the trim exponents deviate for larger trims).
The laws apply along a line of similar operating points; a point on the old curve maps to a point on the new curve, not any point.

## Procedure
1. Find the target (Q, H) and compute the point on the old curve with the same system-curve relation `H = c Q^2`. Compute the new speed (or diameter) that moves that point to the target.
2. For trimming, use the pump maker's trimming curves; typically limited to about 75 percent of full diameter (gated: unconfirmed, source is paywalled or blocked); efficiency drops after trimming and NPSHr changes.
3. Check motor loading: power falls with trim; speed up raises power as the cube.

## Gotchas
- Speed increases are limited by the pump's mechanical limit, bearings and motor.
- Efficiency does not remain constant at large speed ratios.
- Trimming is irreversible; confirm with the manufacturer.

## Verify
- [ ] Field readings at the new setting match the predicted flow and pressure within 5-10 percent (gated: unconfirmed, source is paywalled or blocked).
