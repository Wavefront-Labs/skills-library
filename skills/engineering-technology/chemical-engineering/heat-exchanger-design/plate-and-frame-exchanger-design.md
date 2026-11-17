---
id: engineering-technology.chemical-engineering.heat-exchanger-design.plate-and-frame-exchanger-design
name: plate-and-frame-exchanger-design
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-compact-and-air-cooled, plate-and-frame-exchanger-design, plate-and-frame, plate-heat-exchanger, gasketed-plate]
level: practitioner
status: draft
description: "Rate and select a gasketed plate-and-frame exchanger: plate count, flow arrangement, pressure drop and gasket limits."
sources:
  - "Kern Process Heat Transfer, Heat Exchanger Design Handbook, TEMA Standards, Kemp Pinch Analysis and Process Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plate and frame exchanger design

**Goal:** Rate and select a gasketed plate-and-frame exchanger: plate count, flow arrangement, pressure drop and gasket limits.

## Steps
1. Check the application limits: pressure and temperature limits of the gaskets and plates, fluid compatibility, and solids content.
2. Use close temperature approaches (down to about 1 to 3 C is possible with counterflow); LMTD correction is near 1.
3. Estimate the area from Q / (U delta T_lm) with U values typically several times those of shell-and-tube for clean liquids; confirm with the vendor.
4. Pressure drop is set by the number of passes and channels; allow margin for fouling (usually lower fouling resistance than shell-and-tube).
5. Request the vendor rating with the full data and ask for the excess area and the maximum design conditions.

## Gotchas
- Gasket material limits the temperature and the chemical compatibility.
- Plate exchangers are sensitive to particles and fibres; fit a strainer.

## Verify
- [ ] Vendor rating confirms duty with margin.
- [ ] Both side pressure drops are within limits.
