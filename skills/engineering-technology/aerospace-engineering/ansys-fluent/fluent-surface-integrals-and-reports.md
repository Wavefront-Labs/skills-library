---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-surface-integrals-and-reports
name: fluent-surface-integrals-and-reports
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-postprocessing, surface-integrals, mass-flow-rate, area-weighted-average, pressure-recovery, total-pressure]
level: practitioner
status: draft
description: "Use Fluent surface integrals for mass flow, pressure recovery and area-weighted quantities at planes, such as inlet distortion and wake rakes."
sources:
  - "Ansys Fluent user guide (surface integrals)"
  - "Fluent post-processing documentation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent: surface integrals

**Goal:** engineering numbers from planes and surfaces.

## Steps
1. Create surfaces: **Results > Surfaces > Create > Plane / Iso-Surface / Rake** at the station of interest (inlet face, fan face, wake rake plane).
2. **Results > Reports > Surface Integrals:** choose Mass Flow Rate, Area, Area-Weighted Average, Mass-Weighted Average, Facet Maximum or Minimum for the field (for example Total Pressure, Mach number).
3. Pressure recovery of an inlet: mass-weighted average total pressure at the engine face divided by freestream total pressure.
4. Distortion: compute max/min or a circumferential distortion descriptor from rake or sector data exported to a spreadsheet.

## Practice
- Use mass-weighted averages for total quantities, area-weighted for static pressure.
- Use enough resolution on the surface (refine mesh at the plane).

## Gotchas
- Average of total pressure by area weighting gives a different answer than by mass weighting: state which one.
- Surfaces created from iso-surfaces in the boundary layer at the wall give noise.

## Verify
- [ ] Mass flow at inlet and outlet planes differ by below about 0.1-1%.
