---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.active-optical-sensors-for-nitrogen
name: active-optical-sensors-for-nitrogen
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, active-optical-sensor, ndvi, ndre, canopy-sensor, nitrogen-sensing, n-rich-strip, sufficiency-index, greenseeker]
level: advanced
status: draft
description: "Use active optical canopy sensors for in-season nitrogen: reflectance indices, mounting height, N-rich reference strip, sufficiency index, saturation and validation."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Active optical sensors for nitrogen

**Goal:** sense crop nitrogen status on the go and vary the top-dress rate with an algorithm that has been validated for the crop and region.

## How they work
Active optical sensors emit their own light (red and near-infrared, or red-edge and near-infrared) and measure the reflectance of the canopy, so they work in any ambient light. Indices such as NDVI (red-based) or NDRE and similar red-edge indices relate to biomass and chlorophyll. Commercial examples include sensors such as GreenSeeker and Crop Circle.

## Procedure
1. Establish an N-rich reference: a strip or plot in the field given ample nitrogen, so the crop there is not nitrogen limited; the sensor reading of the field divided by that of the reference gives a sufficiency index or response index.
2. Mount the sensor at the manufacturer's height above the canopy (usually under about a metre above it, within the field of view stated) and level; keep the lenses clean.
3. Choose an algorithm from the university or extension work for your crop and growth stage (several recommended algorithms exist for corn and wheat). The algorithm converts the index and yield potential into a recommended N rate; set minimum and maximum rates and a ceiling.
4. Drive at steady speed, sense and apply simultaneously, or sense and apply in a second pass; log data.
5. Check against tissue tests, soil nitrate tests and a few leaf chlorophyll meter checks.

## Limits
- NDVI saturates at high biomass: use red-edge indices in dense canopies.
- Water stress, disease, weeds and other nutrient deficiencies also change the index; do not attribute all variation to nitrogen.
- Timing: the growth stage window for the algorithm; applying too late fails.
- Soil background at early stages: use a reference and an appropriate index.

## Verify
- [ ] The reference strip receives enough N and is in representative soil.
- [ ] Compare yield on the sensor-driven N rate versus a uniform check strip over several fields and years.
- Unconfirmed: algorithm parameters; use a locally validated source.
