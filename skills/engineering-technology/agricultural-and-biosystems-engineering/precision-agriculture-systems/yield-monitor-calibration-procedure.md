---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.yield-monitor-calibration-procedure
name: yield-monitor-calibration-procedure
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, yield-monitor-calibration, yield-monitor, yield-mapping, mass-flow-sensor, moisture-sensor, grain-cart-scale, calibration]
level: practitioner
status: draft
description: "Calibrate a combine yield monitor: set-up, mass flow calibration with multiple loads at different flow rates, moisture and test weight checks, and annual routine."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Yield monitor calibration procedure

**Goal:** accurate yield values that are comparable across the field and years.

## Before harvest
1. Check and update the monitor software and crop type settings (test weight, moisture standard, bushel or tonne conversion).
2. Inspect the clean-grain elevator and mass-flow sensor (impact plate or optical or paddle type), grain moisture sensor, and speed sensor.
3. Calibrate the header height switch and header width.

## Mass flow calibration
1. Fill the combine and harvest with the machine at a steady speed and the usual harvest conditions; empty the grain tank into a scale (certified weigh wagon or grain cart scale) to get the true mass.
2. Do several loads (typically at least 4-6, spread across low, medium and high flow rates because the sensor response differs by flow); follow the manufacturer's minimum load size (often 1,000-4,000 kg or more).
3. Enter the weighed values in the calibration routine so the monitor computes a calibration curve; check that the curve covers the flow range in harvest.
4. Repeat for each crop and when conditions change substantially (variety, moisture).

## Moisture and test weight
Calibrate the moisture sensor against a reference meter or oven on samples from each field; enter test weight where used for volume conversion.

## Checks
- Compare total yield with weigh-bridge totals for the field; target error within about 2-3 percent for good practice.
- Record calibration settings and keep the data.

## Gotchas
- Calibrating at only one flow rate causes bias at other rates.
- Changing elevator speed or chain wear changes sensor output.

## Verify
- [ ] Field totals vs scale tickets within 3 percent for at least two fields.
