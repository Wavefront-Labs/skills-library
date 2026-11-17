---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.in-bin-natural-air-and-low-temperature-drying
name: in-bin-natural-air-and-low-temperature-drying
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, in-bin-drying, grain-drying, grain-dryer-design, natural-air-drying, low-temperature-drying, drying-front, supplemental-heat]
level: practitioner
status: draft
description: "Plan in-bin natural-air or low-temperature drying: airflow rate, fill depth, drying front, weather limits, supplemental heat and fan control to avoid spoilage."
sources:
  - "Brooker, Bakker-Arkema & Hall, Drying and Storage of Grains and Oilseeds"
  - "Navarro & Noyes, The Mechanics and Physics of Modern Grain Aeration Management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# In-bin natural-air and low-temperature drying

**Goal:** dry grain in the storage bin with ambient air before the top layer spoils.

## Principles
Air at a given temperature and humidity brings grain to an equilibrium moisture; a drying front moves through the bed in the direction of airflow. If the front takes too long to arrive at the top, the top layer spoils.

## Design rules (extension-style, adapt to local data)
1. **Airflow**: higher for wetter grain; natural-air corn drying is often designed for around 1 cfm/bu or more for initial moisture near 20 percent (0.75-1.25 cfm/bu range in guides); lower rates only for already dry grain or cooling.
2. **Fill depth**: limited by fan pressure and initial moisture; fill in layers when the grain is wet; do not exceed the depth that the fan and moisture allow.
3. **Start early** in cool, dry weather and run the fan continuously; avoid shutting fans off for long periods of high humidity unless the control scheme is validated.
4. **Supplemental heat** raises air temperature to lower RH (a rise of roughly 5-10 F is used; as a rule of thumb, RH falls by about half per 20 F rise); excessive heating over-dries the bottom.
5. **Stirring and layer drying** options (stirring devices, layering) improve uniformity.
6. Use a drying simulation or an extension tool for the site's weather data to set the initial moisture limit and the dates.

## Monitoring
Check grain temperature and moisture at the top and bottom regularly; sample the top layer for mould and odour; the top is the last to dry.

## Gotchas
- Wet grain in warm weather can spoil before the front passes.
- Moisture re-wets at the top at night or in humid weather when fans run with bad weather (control by weather-based controllers).

## Verify
- [ ] Top-layer moisture reaches the safe level before the grain warms in spring.
