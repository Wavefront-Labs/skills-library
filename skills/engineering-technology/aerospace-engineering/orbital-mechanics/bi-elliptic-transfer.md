---
id: engineering-technology.aerospace-engineering.orbital-mechanics.bi-elliptic-transfer
name: bi-elliptic-transfer
category: engineering-technology
field: aerospace-engineering
product: orbital-mechanics
tags: [bielliptic, bi-elliptic-transfer, orbit-transfers, delta-v, three-impulse]
level: practitioner
status: verified
description: "Compute bi-elliptic transfer delta-v and time of flight, and compare with Hohmann across radius ratios to see when the extra burn pays off."
sources:
  - "Curtis, Orbital Mechanics for Engineering Students"
  - "Vallado, Fundamentals of Astrodynamics and Applications"
  - "Recomputed in Python from the burn formulas above (scipy root-finding for the 11.94 and 15.58 thresholds)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Bi-elliptic transfer

**Goal:** a three-burn coplanar transfer that can use less delta-v than Hohmann for large radius ratios.

## Burns (circular `r1` to circular `r2`, intermediate apoapsis `rb > r2`)
1. `dv1 = sqrt(2 mu/r1 - 2 mu/(r1 + rb)) - sqrt(mu/r1)`.
2. `dv2 = sqrt(2 mu/rb - 2 mu/(rb + r2)) - sqrt(2 mu/rb - 2 mu/(r1 + rb))` (at `rb`).
3. `dv3 = sqrt(2 mu/r2 - 2 mu/(rb + r2)) - sqrt(mu/r2)` magnitude (retrograde at `r2`).
Total `dv = |dv1| + |dv2| + |dv3|`; time of flight `= pi (sqrt(a1^3/mu) + sqrt(a2^3/mu))` with `a1 = (r1+rb)/2`, `a2 = (rb+r2)/2`.

## When it wins
- For radius ratio `r2/r1` above 15.58, every bi-elliptic transfer with `rb > r2` needs less delta-v than Hohmann (computed: the limit `rb -> r2` meets Hohmann at 15.58).
- Between 11.94 and 15.58, it wins only when `rb` is large enough; small `rb` loses (computed at ratio 13: `rb = 50 r1` wins by 0.0001 v1, `rb = 1000 r1` by 0.006 v1; `rb` just above `r2` loses). The `rb -> infinity` (bi-parabolic) limit equals Hohmann at 11.94.
- Below 11.94, Hohmann is better for every `rb`.
- The saving is a few percent and costs a very long flight time (many days to months, or years).

## Procedure
1. Compute Hohmann `dv` first.
2. Scan `rb` from `r2` upward; plot `dv`.
3. Check the time of flight and perturbations at the far apoapsis.

## Gotchas
- Limits of the sphere of influence cap `rb`.
- Plane change at `rb` (low speed) is cheap; combine plane change with the second burn when needed.

## Verify
- [ ] As `rb` approaches `r2`, the total tends to the Hohmann delta-v.
