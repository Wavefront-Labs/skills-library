---
id: engineering-technology.chemical-engineering.heat-exchanger-design.tube-layout-pitch-and-baffles
name: tube-layout-pitch-and-baffles
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-shell-and-tube-selection, tube-layout-pitch-and-baffles, tube-pitch, tube-layout, triangular-pitch, square-pitch, baffle-cut, baffle-spacing, shell-diameter, tube-count, heat-exchanger-geometry]
level: practitioner
status: draft
description: "Set tube diameter, pitch, layout angle, baffle cut and spacing for a shell-and-tube exchanger, trading shell-side coefficient against pressure drop, fouling and cleaning."
sources:
  - "Kern Process Heat Transfer, Perry Handbook heat transfer section, TEMA Standards, Heat Exchanger Design Handbook (HEDH), Kemp Pinch Analysis and Process Integration, Smith Chemical Process Design and Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tube layout, pitch and baffle design

**Goal:** a geometry that balances heat transfer, pressure drop, cleanability and vibration.

## Tubes
- Common outside diameters: 19.05 mm (3/4 in) and 25.4 mm (1 in); smaller tubes give more area per volume but clean poorly.
- **Pitch** p_t = 1.25 to 1.5 times d_o (1.25 common).
- **Layout angle**: triangular (30 degrees) gives about 15% more tubes in a shell and higher shell-side coefficient but cannot be cleaned mechanically between tubes; square (90 degrees) or rotated square layouts permit cleaning lanes and are used for shell-side fouling.
- **Tube length**: 3.66 m (12 ft), 4.88 m (16 ft), 6.1 m (20 ft) are standard; a longer exchanger for the same area is cheaper, limited by bundle pulling space.
- **Tube count and shell diameter** from tubesheet layout counts (tables or software); allow for pass partition lanes and the clearance between the bundle and shell (larger for floating heads).

## Baffles
- Segmental baffle cut about 20 to 25% of the shell diameter (up to 35% in some designs); smaller cuts give higher velocity and pressure drop.
- **Spacing**: between roughly 0.2 and 1.0 times the shell inside diameter, with a practical minimum of about 50 mm and a minimum of one fifth of the shell diameter commonly used; the maximum is set by tube support span (vibration) and the TEMA limit for the tube size and material.
- Design for crossflow velocity: liquids near 0.3 to 1 m/s, gases 5 to 15 m/s (indicative).

## Procedure
1. Choose pitch and layout by cleaning needs.
2. Start from baffle spacing near 0.3 to 0.5 D_s and adjust to use the allowable pressure drop.
3. Evaluate shell-side h and pressure drop; iterate.
4. Check tube vibration at the final spacing.

## Gotchas
- Allowable pressure drop is the main design lever; use it fully, not just meet the area.
- Very close baffle spacing causes poor flow distribution and dead zones.

## Verify
- [ ] Shell-side velocity, pressure drop and Reynolds within targets.
- [ ] Unsupported span below the vibration limit.
