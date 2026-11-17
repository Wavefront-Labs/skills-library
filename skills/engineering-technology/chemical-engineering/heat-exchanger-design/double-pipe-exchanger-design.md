---
id: engineering-technology.chemical-engineering.heat-exchanger-design.double-pipe-exchanger-design
name: double-pipe-exchanger-design
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-compact-and-air-cooled, double-pipe-exchanger-design, double-pipe-exchanger, hairpin-exchanger, annulus]
level: practitioner
status: gated
description: "Design double-pipe and hairpin exchangers for small duties and high pressure: annulus and pipe sides, hairpin count and LMTD."
sources:
  - "Kern Process Heat Transfer, Heat Exchanger Design Handbook, TEMA Standards, Kemp Pinch Analysis and Process Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Double pipe exchanger design

**Goal:** Design double-pipe and hairpin exchangers for small duties and high pressure: annulus and pipe sides, hairpin count and LMTD.

## Steps
1. Use for small areas (typical practice is below several tens of m2 (gated: unconfirmed, source is paywalled or blocked)), high pressure, or large temperature cross needing countercurrent flow.
2. Place the high-pressure or fouling fluid in the inner pipe; calculate the annulus equivalent diameter for heat transfer (hydraulic and thermal equivalent diameters differ).
3. Countercurrent flow gives F = 1; compute the area from Q / (U delta T_lm) and the number of hairpins from the length per hairpin.
4. Check the pressure drop on both sides, including return bends, and the thermal expansion (U-bend arrangement handles it).
5. Add longitudinally finned inner tubes if the annulus side is the controlling resistance.

## Gotchas
- Many hairpins in series need a lot of connection piping; consider shell-and-tube beyond a point.
- Use the thermal equivalent diameter for the film coefficient.

## Verify
- [ ] Area meets duty plus margin.
- [ ] Both pressure drops are within allowance.
