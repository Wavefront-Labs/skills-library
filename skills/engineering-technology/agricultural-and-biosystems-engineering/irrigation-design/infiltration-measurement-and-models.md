---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.infiltration-measurement-and-models
name: infiltration-measurement-and-models
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, infiltration-rate, soil-water, infiltrometer, kostiakov, basic-intake-rate, double-ring, nrcs-intake-family]
level: practitioner
status: gated
description: "Measure soil infiltration with double-ring or furrow inflow-outflow tests, fit Kostiakov or modified models, and use basic intake rate to limit sprinkler application rates."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Walker & Skogerboe, Surface Irrigation: Theory and Practice"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Infiltration measurement and models

**Goal:** an intake model that governs surface-irrigation design and sprinkler application rate limits.

## Measure
- **Double-ring infiltrometer**: drive two concentric rings; keep the same head in the outer ring to limit lateral flow; record the drop in the inner ring at intervals until intake becomes steady. It overestimates for furrows (lateral flow, no wetted perimeter effect) (gated: unconfirmed, source is paywalled or blocked).
- **Furrow inflow-outflow**: measure inflow and outflow in a blocked or free-draining furrow section; infiltration is inflow minus outflow per unit length. It represents field operation better for furrows.
- **Sprinkler infiltrometer / rainfall simulator** for sprinkler design on sloped soils.

## Models
- **Kostiakov** (gated: unconfirmed, source is paywalled or blocked): `Z = k t^a`; **modified Kostiakov**: `Z = k t^a + f0 t` (f0 basic intake rate) used in surface irrigation software.
- **NRCS intake families**: standard curves (intake families) used in handbook design. Check the handbook for the form.
- **Green-Ampt** for physically based infiltration under ponding.

## Use
- Sprinkler design: average application rate must be below the basic intake rate (or the rate of the crusted surface), accounting for surface storage and slope.
- Surface design: advance and recession rely on the infiltration function; variability along the field is large, so measure at several places and times.

## Gotchas
- Infiltration changes through the season with cultivation, crusting and swelling clays.
- Temperature affects water viscosity.

## Verify
- [ ] At least three tests in each major soil; coefficient of variation reported.
