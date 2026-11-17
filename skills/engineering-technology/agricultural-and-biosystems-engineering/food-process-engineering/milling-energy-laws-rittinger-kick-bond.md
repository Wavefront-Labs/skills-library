---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.milling-energy-laws-rittinger-kick-bond
name: milling-energy-laws-rittinger-kick-bond
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, bond-work-index, rittinger, kick, size-reduction, milling-energy, hammer-mill, roller-mill, grinding-power]
level: advanced
status: draft
description: "Estimate size reduction energy for milling food and feed: Rittinger, Kick and Bond laws, work index use, mill selection and power checks from measurements."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Singh & Heldman, Introduction to Food Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Milling energy laws: Rittinger, Kick and Bond

**Goal:** a first estimate of mill power, and a way to compare mill performance, for grinding grain, spices, sugar and similar solids.

## Laws
- Rittinger: energy proportional to new surface produced: E = Kr x (1/x2 - 1/x1). Best for fine grinding.
- Kick: energy proportional to size reduction ratio: E = Kk x ln(x1/x2). Best for coarse crushing.
- Bond: E = 10 x Wi x (1/sqrt(P80) - 1/sqrt(F80)), the empirical middle-ground law, where F80 and P80 are the sieve sizes (in micrometres) passing 80 percent of the feed and product, Wi the Bond work index (kWh per short ton) and E in kWh per short ton. Convert units carefully (1 short ton is about 907 kg).
- The general form dE/dx = -C x x^-n; n = 1, 2 and 1.5 give Kick, Rittinger and Bond.

## Practice
- Work indices for food materials are measured, not tabulated reliably; for feed grain the specific energy depends on mill type, screen size and moisture; the best guide is the mill maker's data and measured kWh/t at your product.
- Mills: hammer mills (impact, with screen) for grain; roller mills (compression, shear) for wheat, with corrugated rolls and gradual reduction; pin and disc mills for fine grinding; jet mills for ultra-fine.
- Power check: measured net power (gross minus no-load) divided by throughput gives the specific energy; use it to compare screens and settings.

## Safety
Milling dust is explosive: see `grain-dust-explosion-hazard-and-housekeeping`; use explosion protection and magnets to keep metal out.

## Verify
- [ ] Specific energy (kWh/t) measured at two screen sizes.
- [ ] Particle-size distribution measured (`particle-size-analysis-and-sieving`).
- Unconfirmed: Wi values for your product.
