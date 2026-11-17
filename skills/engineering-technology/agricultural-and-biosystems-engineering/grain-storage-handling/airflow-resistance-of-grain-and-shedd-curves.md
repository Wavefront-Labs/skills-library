---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.airflow-resistance-of-grain-and-shedd-curves
name: airflow-resistance-of-grain-and-shedd-curves
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, airflow-resistance, grain-properties, grain-physical-properties, shedd-curves, hukill-ives, static-pressure, asabe-d272]
level: practitioner
status: verified
description: "Estimate static pressure from airflow resistance of grain using Shedd curves and the Hukill-Ives equation, adjusted for fines, packing and depth, for fan selection."
sources:
  - "Sinha & Muir, Grain Storage: Part of a System"
  - "Navarro & Noyes, The Mechanics and Physics of Modern Grain Aeration Management"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Airflow resistance of grain (Shedd curves)

**Goal:** pressure drop through the grain bed for a chosen airflow, to select a fan.

## Relation
Pressure drop per unit depth rises faster than linearly with superficial air velocity. ASABE D272 (paywalled) tabulates airflow resistance data; the Hukill-Ives form usually quoted for it is (gated: unconfirmed, source is paywalled or blocked):

`dP/L = a Q^2 / ln(1 + b Q)`

with Q the airflow per unit area (m3/s per m2), L the bed depth and `a`, `b` crop-specific constants listed in the standard (for loose-fill conditions for each crop). Older charts present the same data as Shedd curves of pressure per metre (or inch of water per foot) against airflow per area. Take values from the current D272 table; the packing and fines correction factors described below are also from that standard (gated: unconfirmed, source is paywalled or blocked).

## Adjustments
1. **Packing**: grain packed by fall in tall bins has higher resistance than loose fill; the standard gives packing correction factors for depth.
2. **Fines and foreign material**: resistance increases significantly where fines accumulate (centre of the bin); the standard gives multipliers for fine material percentages.
3. **Moisture**: resistance rises as grain wets and swells.
4. **Direction**: air up or down differs slightly.

## Procedure
1. Choose the airflow rate per area (from the design airflow in the aeration or drying skill and bin cross-section).
2. Read dP/L; multiply by depth (including the peak equivalent depth for a peaked pile).
3. Add duct, perforated floor, transition and plenum losses (see fan sizing skill) and design for the worst condition (fines, deepest fill).

## Gotchas
- Using the clean-grain curve for dirty grain under-sizes the fan.
- Check the units of the source: inches of water per foot versus Pa per metre.

## Verify
- [ ] Measured static pressure at the plenum is within about 15 percent of the prediction after filling.
