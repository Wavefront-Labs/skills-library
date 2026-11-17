---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.energy-and-water-per-kilogram-benchmarking
name: energy-and-water-per-kilogram-benchmarking
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, energy-per-kilogram, water-per-kilogram, vertical-farm-benchmark, led-efficacy, light-use-efficiency, resource-use-efficiency, vertical-farming]
level: practitioner
status: draft
description: "Benchmark an indoor farm by energy and water per kilogram of harvested produce: define boundaries, LED efficacy, DLI, yield accounting and fair comparison."
sources:
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Energy and water per kilogram benchmarking

**Goal:** comparable and honest resource-use figures for an indoor or greenhouse farm.

## Define the numbers
- Energy intensity = total electrical (and other fuel) energy over a period / fresh mass sold or harvested in that period (kWh per kg). State the boundary: only the grow rooms or the whole building including propagation, packing, cold storage and offices; and whether on-site heating fuel is included (convert to kWh).
- Water intensity = water withdrawn from the supply (litres per kg), and separately the transpired water that is recovered by dehumidifiers and returned (this is why indoor farms use less net water than field crops).
- Yield: marketable fresh mass, trimmed or untrimmed; give the crop, the cycle time and the fraction of the area harvested.
- Use the same period for all inputs and outputs (at least a full crop cycle and ideally a year to capture the seasons).

## Drivers
- Lighting is generally the largest electrical use in a sole-source (no sunlight) farm, followed by HVAC (which is largely removing lighting heat). So kWh/kg depends on photosynthetic photon efficacy (micromol per joule), daily light integral (mol per m2 per day), yield per mol, and HVAC efficiency (`grow-room-hvac-and-dehumidification-load`).
- Light use efficiency = grams of fresh (or dry) mass per mol of light delivered; the best measure of crop performance in the room.
- Crop and cultivar: leafy greens vs fruiting crops differ by large factors.

## Reporting and comparison
Published numbers vary widely and use different boundaries; compare only with the same definition. Report with uncertainty, and avoid quoting values from marketing material. Track monthly and set improvement targets (dimmable LED, better efficacy, better HVAC, better yield per area).

## Verify
- [ ] Meters at sub-system level (lighting, HVAC, pumps) reconcile with the utility bill.
- [ ] Harvest weights from scale records, not estimates.
- Unconfirmed: benchmark values; compile from your own data.
