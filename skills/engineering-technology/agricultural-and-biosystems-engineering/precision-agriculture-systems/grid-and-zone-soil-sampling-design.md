---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.grid-and-zone-soil-sampling-design
name: grid-and-zone-soil-sampling-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, grid-soil-sampling, zone-sampling, management-zones, soil-test, composite-sample, soil-variability, sample-georeferencing]
level: practitioner
status: draft
description: "Design grid or zone soil sampling: grid size, management zone delineation, cores per composite, depth, timing, georeferencing and lab handling."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Grid and zone soil sampling design

**Goal:** soil test data that captures the spatial variation that matters at an affordable cost.

## Approaches
- Whole-field composite: one sample per uniform area; cheap, no spatial information.
- Grid sampling: a regular grid (a commonly used spacing is one sample per hectare or per 2.5 acres (2.5 acres = 1.01 ha, computed), often 100 m by 100 m; finer grids improve the maps but cost more). Samples can be taken at the grid point or as a composite of cores around the point.
- Zone sampling: define management zones from stable data (soil EC maps, elevation, soil survey, yield maps over several years, imagery) and sample within each zone; often more cost-effective than a fine grid when the zones are real.

## Procedure
1. Georeference sample points with GNSS; keep the same points over years for trend analysis.
2. Collect cores at a consistent depth (commonly 15-20 cm for tilled fields; shallower, such as 7.5 cm, for no-till surface stratification of P and pH, or per the local recommendation system), 10-20 cores per composite within a small radius or zone area, avoiding fertiliser bands, headlands, wet spots and old manure piles.
3. Mix, subsample into a clean labelled bag, keep cool, and send to a laboratory that follows the method used by your recommendation system (accredited and in a proficiency testing programme).
4. Timing: same time each year relative to cropping (such as after harvest or before planting) so results are comparable.
5. Interpolate maps carefully (`yield-map-interpolation-and-classification`) and treat maps from sparse grids as rough guides.

## Pitfalls
Too few points for the amount of variation (maps look like bullseyes); sampling right after lime or fertiliser; mixing depths; position error. Check the semivariogram if you interpolate by kriging.

## Verify
- [ ] Sample plan map and coordinates saved.
- [ ] Duplicate samples at a few points to see sampling plus lab noise.
- Unconfirmed: the grid size that suits your field's variability.
