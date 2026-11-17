---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.bulk-density-test-weight-and-porosity
name: bulk-density-test-weight-and-porosity
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, bulk-density, grain-properties, grain-physical-properties, test-weight, porosity, bin-capacity, packing]
level: practitioner
status: verified
description: "Measure bulk density and test weight, relate them to moisture, packing and fill method, and use porosity in storage capacity, aeration and hopper calculations."
sources:
  - "Sinha & Muir, Grain Storage: Part of a System"
  - "Chakraverty & Singh, Postharvest Technology and Food Process Engineering"
  - "US eCFR, 7 CFR part 810 Official United States Standards for Grain (https://www.ecfr.gov/current/title-7/part-810)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bulk density, test weight and porosity

**Goal:** accurate bin capacity, airflow resistance and load estimates.

## Definitions
- **Bulk density** = mass of grain per unit container volume (kg/m3 or lb/bu). **Test weight** is the standardised bulk density measured with a specified cup (for the US, lb per Winchester bushel; the US No. 1 grade minimum is 56 lb per bushel for corn and 60 lb for wheat other than hard red spring and white club (58 lb), per 7 CFR 810.404 and 810.2204; soybeans are conventionally traded at 60 lb per bushel but have no test weight limit in 810.1604, and that 60 lb figure is (gated: unconfirmed, source is paywalled or blocked)).
- **Porosity** = 1 - bulk density / kernel density; commonly about 35-45 percent for cereals (gated: unconfirmed, source is paywalled or blocked); this is the volume available for air.

## Measurement
1. Use a standard test-weight apparatus with a fixed drop height, strike off the surface, weigh, and convert.
2. Report with moisture content; test weight rises as grain dries and shrinks.
3. In bins, packing under grain depth increases density by a few percent (gated: unconfirmed, source is paywalled or blocked) (more at higher moisture); filling method (centre fill with spreader, drop height) changes density and the distribution of fines.

## Use
- Bin capacity: volume x bulk density, allowing for peak, cone and packing.
- Aeration and drying: porosity and packing set airflow resistance (see airflow resistance skill).
- Structural loads: density as unit weight in Janssen calculations (use the design code's characteristic values).

## Gotchas
- Different grains and varieties differ; do not apply corn values to sorghum or oilseeds.
- Damaged, shrivelled and fines-rich grain reads low.

## Verify
- [ ] Bin inventory by volume reconciles with scale tickets within a few percent.
