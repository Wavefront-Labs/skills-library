---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.yield-map-interpolation-and-classification
name: yield-map-interpolation-and-classification
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, yield-map-interpolation, yield-monitor, yield-mapping, kriging, idw, yield-stability, normalized-yield]
level: practitioner
status: draft
description: "Turn cleaned yield points into maps: grid size, inverse distance or kriging interpolation, normalising across years, classification breaks and stability zones."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Yield map interpolation and classification

**Goal:** a readable map and consistent management zones from point data.

## Interpolation
1. Choose a grid cell size consistent with the data density and machine width (for example 10-20 m); smaller cells do not add information beyond the swath spacing.
2. Interpolate with inverse distance weighting (simple, fast) or ordinary kriging (uses a variogram, gives uncertainty); use block kriging for smooth maps. Check the variogram range to judge spatial structure.
3. Keep the field boundary mask; do not extrapolate outside the boundary.

## Classification
- Equal-interval, quantile or natural-breaks classes; choose class number (3-5) to match decision needs.
- Use the same breaks across fields when comparing; otherwise normalise.

## Multi-year analysis
1. **Normalise** each year's yield to the field mean (percent of mean) before combining so that years with different crops or weather are comparable.
2. Compute the average and standard deviation of relative yield by cell: consistent high or low cells form stable zones; high variability marks unstable zones.
3. Overlay with soil EC, elevation and imagery to find causes.

## Gotchas
- Interpolation smooths real discontinuities (boundaries).
- Harvest and flow delay errors produce false stripes.

## Verify
- [ ] Cross-validate by removing a subset of points and checking prediction errors.
