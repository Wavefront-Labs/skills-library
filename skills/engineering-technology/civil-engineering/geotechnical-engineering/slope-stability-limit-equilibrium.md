---
id: engineering-technology.civil-engineering.geotechnical-engineering.slope-stability-limit-equilibrium
name: slope-stability-limit-equilibrium
category: engineering-technology
field: civil-engineering
product: geotechnical-engineering
tags: [slope-stability, limit-equilibrium, factor-of-safety, bishop, spencer, morgenstern-price, slope-w, phreatic-surface, drawdown, embankment]
level: advanced
status: draft
description: "Check slope stability by limit equilibrium: drained/undrained cases, groundwater, method (Bishop, Spencer), search surfaces, target factors of safety and sensitivity."
sources: ["USACE EM 1110-2-1902 Slope Stability", "Duncan, Wright and Brandon, Soil Strength and Slope Stability", "Abramson et al., Slope Stability and Stabilization Methods"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Slope stability by limit equilibrium

**Goal:** factor of safety FS (available shear strength / strength required for equilibrium) on the critical slip surface, for each design condition.

## Cases
- End of construction (undrained, total stress, su, clays); long term (drained, c' and phi', pore pressures from steady seepage); rapid drawdown (multi-stage); seismic (pseudo-static or Newmark displacement, per authority).
- USACE guidance for embankment dams uses about 1.3 end of construction and 1.5 long-term. For other slopes use the owner's criteria; no single number applies everywhere.

## Method
1. Geometry from survey, layers from borings, groundwater from piezometers (use the design water level, not the day of drilling).
2. Strength: effective-stress parameters for drained cases. Use residual or fully softened strength on pre-existing shear surfaces and first-time slides in stiff fissured clays, not peak.
3. Method: ordinary (Fellenius) is conservative and not for final design; Bishop simplified satisfies moment equilibrium for circles; Spencer or Morgenstern-Price satisfy force and moment equilibrium for any surface. Bishop and Spencer usually agree within a few percent on circles.
4. Search with grids and radii for circles, plus non-circular/block searches where weak layers exist. Confirm the minimum is not on the edge of the search grid.
5. Add surcharge, tension cracks and reinforcement (nails, geogrids) only with their pull-out checks.

## Gotchas
- A pore pressure ratio ru shortcut hides the real piezometric surface.
- Sensitivity: vary phi' and water level over a credible range; a design that fails by one step is fragile.

## Verify
Hand-check against an infinite slope (dry, cohesionless: FS = tan phi' / tan beta) before trusting software.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
