---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.thin-layer-drying-equations-and-emc
name: thin-layer-drying-equations-and-emc
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, thin-layer-drying, grain-drying, grain-dryer-design, page-equation, equilibrium-moisture, moisture-ratio, drying-simulation]
level: practitioner
status: verified
description: "Model grain drying with thin-layer equations (Lewis, Page), find equilibrium moisture with Henderson or Chung-Pfost, and fit constants to experiment for simulation."
sources:
  - "Brooker, Bakker-Arkema & Hall, Drying and Storage of Grains and Oilseeds"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Thin-layer drying equations and EMC

**Goal:** predict how fast one layer of kernels dries at given air conditions, the building block for dryer simulation.

## Equations
- Moisture ratio `MR = (M - Me) / (M0 - Me)`, where Me is equilibrium moisture content at the air temperature and relative humidity.
- **Lewis (Newton)**: `MR = exp(-k t)`.
- **Page**: `MR = exp(-k t^n)`; the extra exponent n captures non-exponential behaviour. Common for cereals and oilseeds.
- Rate constant `k` depends on air temperature via Arrhenius form, `k = A exp(-E/RT)`.
- Me from published EMC equations (modified Henderson, Chung-Pfost, modified Halsey and others in ASABE D245 (gated: unconfirmed, source is paywalled or blocked)), with grain-specific constants.

## Fit from experiment
1. Dry a thin layer (a few kernels deep) at constant temperature and humidity; record weight at intervals.
2. Compute MR, regress ln(-ln MR) on ln t for Page to get n (slope) and ln k (intercept), since ln(-ln MR) = ln k + n ln t (algebra from MR = exp(-k t^n)), repeat at several temperatures.
3. Validate on a separate run.

## Use
Combine thin-layer equations with heat and mass balances in a deep-bed or dryer model (Brooker, Bakker-Arkema and Hall describe the framework), or use a validated simulation program.

## Gotchas
- Equations are for the range tested; extrapolating to higher temperatures can mislead and over-heating harms quality.
- Kernel size, variety, history (field-dried versus wet harvested) change constants.

## Verify
- [ ] Model predicts the final moisture of a trial within about 0.5 point.
