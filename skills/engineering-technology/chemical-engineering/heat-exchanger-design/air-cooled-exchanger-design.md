---
id: engineering-technology.chemical-engineering.heat-exchanger-design.air-cooled-exchanger-design
name: air-cooled-exchanger-design
category: engineering-technology
field: chemical-engineering
product: heat-exchanger-design
tags: [chemical-engineering, heat-exchanger-design, hx-compact-and-air-cooled, air-cooled-exchanger-design, air-cooled-exchanger, fin-fan, air-cooler]
level: practitioner
status: gated
description: "Specify an air-cooled exchanger: design air temperature, approach, bundle and fan selection, and recirculation and winter operation."
sources:
  - "Kern Process Heat Transfer, Heat Exchanger Design Handbook, TEMA Standards, Kemp Pinch Analysis and Process Integration"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Air cooled exchanger design

**Goal:** Specify an air-cooled exchanger: design air temperature, approach, bundle and fan selection, and recirculation and winter operation.

## Steps
1. Set the design dry-bulb temperature from site data (a high percentile of the summer temperature) and allow for recirculation of hot air.
2. The approach of the process outlet to the air inlet is typically 10 to 20 C or more for economic designs; closer is costly (gated: unconfirmed, source is paywalled or blocked).
3. Use extended (finned) tube data and the bare surface equivalent, estimate U based on the bare area, and size the face area and the number of tube rows.
4. Choose the fan type and drive, forced draft or induced draft, and consider variable pitch or speed control for turndown and noise.
5. Protect against freezing and cold-weather overcooling (louvres, recirculation, steam coil), and consider the process fluid pour point.

## Gotchas
- Air-side fouling and wind effects reduce performance.
- Noise limits apply near the site fence and the personnel areas.

## Verify
- [ ] Required duty is met at the design air temperature.
- [ ] Winter operation avoids the freeze or pour point.
