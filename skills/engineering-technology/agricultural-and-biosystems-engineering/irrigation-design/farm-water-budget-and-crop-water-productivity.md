---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.farm-water-budget-and-crop-water-productivity
name: farm-water-budget-and-crop-water-productivity
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, water-productivity, water-budget, crop-water-productivity, water-use-efficiency, irrigation-water-use-efficiency, benchmarking]
level: practitioner
status: gated
description: "Build a farm or field water budget and compute crop water productivity: inflows, outflows, storage, ET, yield per cubic metre and per unit of applied water."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Farm water budget and productivity

**Goal:** know where the water went and what it produced, to guide investments.

## Budget
Inflow: irrigation (metered), effective rainfall (`effective-rainfall-estimation`), change in stored soil water, and any shallow groundwater contribution. Outflows: crop ET (`single-and-dual-crop-coefficient-method`), evaporation losses, runoff and tailwater, deep percolation (including intended leaching) and storage at season end. Close the balance and report the residual as an error.

## Productivity metrics
- Crop water productivity (CWP) = yield / seasonal ET (kg/m3), a physical measure of crop efficiency.
- Irrigation water productivity = yield / irrigation applied; this reflects losses as well as crop response.
- Economic water productivity = net income / water volume.
- Use the same units and basis for comparison between fields and years; remember that yield differences also arise from weather.

## Use
Benchmark fields, evaluate deficit schedules (`deficit-irrigation-and-yield-response`), justify measurement equipment and water licences, and report to programs.

## Verify
- [ ] Meters are calibrated and read at season start and end.
- [ ] Residual in the budget is explained or flagged.
- Typical CWP values are not given here; use crop-specific local data. The metric definitions are common usage (gated: unconfirmed, source is paywalled or blocked).
