---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.field-efficiency-and-effective-capacity
name: field-efficiency-and-effective-capacity
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, field-efficiency, field-capacity, machinery-management, effective-field-capacity, time-study, turning-loss]
level: practitioner
status: verified
description: "Compute theoretical and effective field capacity with S x W x E, break field efficiency into turning, overlap and handling losses, and time-study a real field."
sources:
  - "ASABE D497 Agricultural Machinery Management Data (paywalled; index at https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Field efficiency and effective field capacity

**Goal:** a realistic hectares-per-hour number for planning and costing.

## Formulas
- Theoretical field capacity (ha/h) = `S x W / 10` (S km/h, W m).
- Effective field capacity `C_e = S x W x E / 10`, E = field efficiency (decimal).
- US units: acres/h = `S (mph) x W (ft) x E / 8.25`.
- Material capacity (t/h) = `C_e x yield (t/ha)` for harvesters; this can be the true limit.

## Where efficiency goes
Time efficiency (turning, filling, unloading, adjustments, breakdowns) and width efficiency (overlap, guidance error). ASABE D497 lists typical field efficiency ranges and speed ranges per machine (values not reproduced here: gated: unconfirmed, source is paywalled or blocked); use them as first estimates and replace them with measured values.

## Field time study
1. Log, for a full field, timed elements: working, headland turns, loading/unloading, stops.
2. `E = working time at nominal speed / total field time` adjusted for measured width efficiency (measure actual swath overlap).
Worked check (computed): 10 km/h x 12 m / 10 = 12 ha/h theoretical; 5 mph x 40 ft / 8.25 = 24.2 acres/h, equal to 5280 x 40 x 5 / 43560.
3. Repeat in fields of different shape; efficiency rises with longer rows and falls with small, irregular fields.

## Gotchas
- Field efficiency is not mechanical efficiency; do not confuse them.
- Autoguidance reduces overlap and raises width efficiency; update E when it is adopted.
- Speed range is limited by quality of work (seed spacing, spray drift, loss), not just power.

## Verify
- [ ] Area worked / total time reproduces the C_e used in planning.
- [ ] A material-capacity check (t/h) does not cap the machine below the area capacity.
