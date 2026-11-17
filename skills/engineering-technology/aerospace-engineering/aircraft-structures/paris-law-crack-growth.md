---
id: engineering-technology.aerospace-engineering.aircraft-structures.paris-law-crack-growth
name: paris-law-crack-growth
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, fatigue, damage-tolerance, paris-law, crack-growth, stress-intensity, forman, nasgro, fracture-mechanics]
level: advanced
status: draft
description: "Predict fatigue crack growth life with the Paris and Forman relations, stress intensity geometry factors and spectrum loading, and know what retardation and thresholds do."
sources:
  - "Anderson, Fracture Mechanics: Fundamentals and Applications"
  - "Broek, Elementary Engineering Fracture Mechanics"
  - "NASGRO documentation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Paris-law crack growth

**Goal:** cycles from an initial crack to a critical size.

## Relations
- Stress intensity: `K = beta * sigma * sqrt(pi a)` with geometry factor `beta`.
- Paris: `da/dN = C (Delta K)^m`; typical `m` for aluminium alloys is about 3 (values depend on alloy, units and R ratio; take `C` and `m` from the data source for the material and environment).
- Forman adds the R-ratio and instability near `K_c`: `da/dN = C (Delta K)^m / ((1 - R) K_c - Delta K)`.
- Threshold `Delta K_th`: below it growth rate is negligible.
- Life: `N = integral from a0 to ac of da / (C (beta Delta sigma sqrt(pi a))^m)`.
- Critical crack size `a_c`: where `K_max = K_c` (or net-section yield).

## Procedure
1. Select initial flaw size (assumed by damage-tolerance rules or inspection capability).
2. Compute the stress at the location from the spectrum (cycle count by rainflow).
3. Integrate with a code (NASGRO, AFGROW) or a script; include retardation models (Willenborg, Wheeler) only if validated against tests.
4. Compute inspection intervals as a fraction of the life from detectable size to critical, with a scatter factor.

## Gotchas
- Mixed-mode, corner cracks and multiple site damage need proper `beta`.
- Retardation models can be unconservative; the test dictates.

## Verify
- [ ] The integration reproduces a published life for a through crack in a plate.
