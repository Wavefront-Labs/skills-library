---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.checkbook-water-balance-scheduling
name: checkbook-water-balance-scheduling
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, checkbook-scheduling, irrigation-scheduling, soil-water, water-balance, depletion, ks, refill-point]
level: practitioner
status: verified
description: "Run a daily root-zone water balance (checkbook) to schedule irrigation: inputs, depletion bookkeeping, refill rule, and corrections with soil moisture readings."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Checkbook water balance scheduling

**Goal:** a simple record that tells when to irrigate and how much.

## Daily bookkeeping (FAO-56)
`Dr,i = Dr,i-1 - (P - RO)i - Ii - CRi + ETc,i + DPi`
- Dr = root-zone depletion (mm), P rainfall, RO runoff, I net irrigation, CR capillary rise, ETc crop ET, DP deep percolation (when Dr would go negative, DP = excess).
- Bounds: 0 (field capacity) to TAW (wilting).
- Irrigate when Dr reaches RAW (or earlier if lead time or delivery limits require); apply Dr (net) divided by application efficiency.
- If Dr > RAW, apply stress coefficient `Ks = (TAW - Dr) / (TAW - RAW)`.

## Procedure
1. Start the season at a known state (after a full irrigation or measured field capacity).
2. Each day record ET0 (local weather), the Kc, rainfall and irrigation.
3. Plan ahead using the forecast ET0 and rainfall for lead time of the delivery schedule.
4. **Calibrate**: every week or two compare Dr with soil moisture sensors or feel method; correct the bookkeeping for drift.

## Gotchas
- Rooting depth increases through the season; update TAW.
- Irrigation efficiency of the system sets gross depth; do not forget it.
- With drip, the active volume is smaller, so RAW is smaller; the interval is shorter.

## Verify
- [ ] Soil moisture check at irrigation time shows near-refill-point status.
