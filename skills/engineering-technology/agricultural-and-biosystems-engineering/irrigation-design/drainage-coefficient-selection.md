---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.drainage-coefficient-selection
name: drainage-coefficient-selection
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, drainage-coefficient, drainage-design-rate, design-drainage-rate, subsurface-drainage, drainage-criteria, water-table-depth]
level: practitioner
status: gated
description: "Select a drainage coefficient: climate and rainfall, crop sensitivity, soil, surface drainage interaction and the design drawdown rate."
sources:
  - "USDA NRCS National Engineering Handbook, Part 650 Engineering Field Handbook (https://www.nrcs.usda.gov)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drainage coefficient selection

**Goal:** the design discharge per unit area (mm/day or inch/day) that drains the field fast enough for the crop at acceptable cost.

## What it is
The drainage coefficient is the rate at which excess water must be removed from the root zone (or the equivalent depth over a design period). It depends on:
- Climate: humid regions use larger coefficients (rain drives recharge) than arid, irrigated regions (where deep percolation and seepage drive drainage and rates are much lower).
- Crop: sensitive crops and shallow-rooted vegetables need quick removal of ponding; tolerant forages less.
- Soil and surface drainage: with good surface drainage (`surface-drainage-and-field-ditches`) less subsurface capacity is needed.
- Criterion: a typical approach is a water table drawdown to a target depth within a given time after a design storm.

## Source of numbers
Regional agencies publish recommended coefficients by climate and soil (for example USDA NRCS Engineering Field Handbook chapter on drainage, regional extension tables, and ILRI, FAO drainage guidelines). Use the guideline for your region; this skill does not give a universal number.

## Steps
1. Define the criterion from crop and region.
2. Pick q from the regional guide, or compute from a water balance using local rainfall frequency.
3. Check with the capacity of the outlet and of the main drains.

## Verify
- [ ] Source of q and its criterion documented.
- [ ] Performance check: measure water table after a significant rain.
- Regional coefficient values are not given here (gated: unconfirmed, source is paywalled or blocked); use the agency guide for your region.
