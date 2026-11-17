---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.sprinkler-application-rate-vs-soil-intake
name: sprinkler-application-rate-vs-soil-intake
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, application-rate-intake, sprinkler-design, sprinkler-irrigation-design, infiltration, runoff-control, set-time, cycle-and-soak]
level: practitioner
status: verified
description: "Keep sprinkler average application rate below soil intake: pick nozzle, spacing and set time, assess runoff risk, and fix problems with cycle-and-soak and storage."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
  - "NRCS Conservation Practice Standard 442, Sprinkler System, Vermont 2017 (https://efotg.sc.egov.usda.gov/api/CPSFile/21967/442_VT_CPS_Sprinkler_System_2017)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sprinkler application rate versus soil intake

**Goal:** apply the desired depth without runoff or ponding.

## Method
1. Establish soil intake: basic intake rate or the intake of the crusted surface at the end of the set (see the infiltration skill), reduced for slope and for residue or plant cover.
2. Compute the system's average application rate `Ia` (see the spacing skill).
3. Require `Ia <= soil intake at the set duration` (allowing for surface storage in tilled soil, residue or basins).
4. **Set time** = gross depth / Ia.
5. If `Ia` exceeds intake: use smaller nozzles at wider spacing (lower rate), longer sets with lower flow, or shorter cycles with multiple passes (cycle and soak) for slow soils.
6. Slope: lower the acceptable rate on sloping ground; NRCS Conservation Practice Standard 442 requires the design application rate to be consistent with soil intake rate, slope and conservation practices, and gives its own slope limits for pivots (check the current state standard). Very steep terrain needs low-rate micro sprinklers or drip.

## Moving systems
Center pivots apply high instantaneous rates at the outer end because of the shape of the wetted pattern; use nozzle packages with larger wetted diameter at the tail, low pressure spray plates and surface storage practices (e.g. basin tillage or reservoirs) to prevent runoff.

## Gotchas
- Soil crusting from droplet impact lowers intake; reduce pressure and droplet energy where required.
- Soil moisture at the start changes the infiltration rate.

## Verify
- [ ] Observe the field after a typical event: no ponding or runoff pattern.
