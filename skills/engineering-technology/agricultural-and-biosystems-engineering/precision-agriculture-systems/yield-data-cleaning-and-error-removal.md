---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.yield-data-cleaning-and-error-removal
name: yield-data-cleaning-and-error-removal
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, yield-data-cleaning, yield-monitor, yield-mapping, outlier-removal, yield-editor, header-up, data-filtering]
level: practitioner
status: draft
description: "Clean combine yield data: remove start and end of pass delays, speed and header-up errors, moisture and GNSS outliers, overlaps and short swaths before mapping or analysis."
sources:
  - "USDA-ARS Yield Editor (https://www.ars.usda.gov/research/software/download/?softwareid=449)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Yield data cleaning and error removal

**Goal:** a dataset free of artefacts that distort maps and zone delineation.

## Typical errors
- **Start and end of pass**: low or high values while the combine fills and empties; remove several seconds at pass start and end.
- **Header up/down**: points recorded with the header raised; use header status flag.
- **Speed outliers**: very slow or very fast speed distorts flow-to-yield conversion; apply a speed range filter.
- **Yield outliers**: values outside a statistical range (for example mean plus or minus 3 standard deviations, or local filters).
- **Moisture outliers** and swath width errors (partial cut width, entered incorrectly).
- **GNSS position errors**: jumps, lost fix, overlapping points.
- **Overlap**: points recorded twice in passes that overlap; remove or average.

## Tools and procedure
1. Use software designed for yield data cleaning such as the USDA-ARS Yield Editor (v2.0.7, imports Ag Leader advanced or Greenstar text files), or commercial farm software filters; check which filters (flow delay, start/end pass, velocity, yield, position) the tool offers.
2. Run filters in order; inspect maps before and after; keep the raw file.
3. Remove spurious data but do not erase real variation (for example, headlands, waterways).
4. Export cleaned data with the same units and metadata for the next step (see interpolation skill).

## Gotchas
- Over-filtering removes extremes that matter.
- Different crops and combines need different filter thresholds.

## Verify
- [ ] Field total yield after cleaning still reconciles with scale data within a few percent.
