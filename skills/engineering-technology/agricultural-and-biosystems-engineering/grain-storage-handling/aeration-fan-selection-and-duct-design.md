---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.aeration-fan-selection-and-duct-design
name: aeration-fan-selection-and-duct-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, aeration-fan-sizing, aeration-control, storage-monitoring, fan-selection, perforated-floor, static-pressure, duct-design]
level: practitioner
status: verified
description: "Select an aeration fan and size ducts: airflow from bushels, total static pressure from grain, floor and transitions, fan curve match, motor, and vent area."
sources:
  - "Navarro & Noyes, The Mechanics and Physics of Modern Grain Aeration Management"
  - "Sinha & Muir, Grain Storage: Part of a System"
  - "Purdue Extension GQTF-38 Temporary Grain Storage Considerations (https://www.extension.purdue.edu/extmedia/gq/gqtf38/gqtf-38.html)"
  - "Purdue Extension AED-20 Managing Dry Grain in Storage (https://www.extension.purdue.edu/extmedia/aed/aed-20.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Aeration fan selection and duct design

**Goal:** a fan that delivers the design airflow against real static pressure at reasonable power.

## Steps
1. **Airflow**: `Q = airflow rate (e.g. cfm/bu) x bushels`. Purdue Extension recommends about 1/10 to 1/5 cfm/bu for dry grain and calls 1/10 the most common in farm bins; at 0.1 cfm/bu the minimum cooling time is 150 hours, and halving the airflow doubles it. 1 cfm/bu equals about 0.80 m3/min per m3 of grain (computed). Drying needs much more.
2. **Static pressure**: grain resistance (see the Shedd curve skill) at the airflow per area, times depth; add a margin for fines and packing.
3. **Perforated floor and ducts**: choose open area (commonly about 10-15 percent or more (gated: unconfirmed, source is paywalled or blocked)) to keep pressure drop small; duct velocities below about 5-8 m/s for low loss (gated: unconfirmed, source is paywalled or blocked); pressure drop through floors and transitions from the maker's data. Avoid elbows or restrictions at the fan inlet.
4. **Fan selection**: plot the system curve (pressure versus Q) on the fan curve (centrifugal or axial); pick the fan so the duty point is on the stable part of the curve and the efficiency is good.
5. **Motor**: power `P = Q x dP / (eta_fan)`, with safety factor and non-overloading check across the operating range, including when the bin is empty (low pressure raises flow and power for some fans).
6. **Exhaust vent area** at the roof to prevent back-pressure: at least 1 square foot per 1000 cfm (Purdue GQTF-38; see the roof vent skill).
7. Controls: weather-based or timers (see aeration controller skill).

## Gotchas
- Fans operate differently at altitude (air density) and at low temperature.
- Upgrades to deeper fill require re-check of fans.

## Verify
- [ ] After installation, measure static pressure and compare to design; test with airflow measurement.
