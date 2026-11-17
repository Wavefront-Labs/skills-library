---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.cold-room-load-calculation
name: cold-room-load-calculation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, cold-room-load, food-refrigeration, cold-chain, refrigeration-load, product-load, respiration-heat, infiltration-load]
level: practitioner
status: verified
description: "Calculate the cooling load of a cold room: transmission, product, respiration, infiltration and internal loads, sizing the evaporator and compressor with run-time factor."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cold room load calculation

**Goal:** refrigeration capacity that meets the peak load with a sensible margin.

## Loads (kW, then add)
1. **Transmission**: `Q = U A (T_out - T_room)` for walls, roof, floor (insulated panels, typical U for 100-150 mm polyurethane or PIR panel around 0.15-0.25 W/m2 K (U = k/thickness: k 0.022-0.025 W/m K gives 0.15-0.25 for 100-150 mm); use the panel maker's data). Include solar effect on exposed roofs.
2. **Product load**: cooling `m c (T_in - T_out) / t`; above-freezing specific heat from the food composition; freezing includes latent heat and sub-freezing sensible heat. Allow for packaging and pallets.
3. **Respiration heat** for fresh produce (varies with temperature and species; use published postharvest data).
4. **Infiltration** from door openings and air leakage: `Q = flow x (h_out - h_in)`, using air change data or a door-factor method; vestibules, air curtains and strip curtains cut this.
5. **Internal loads**: lighting, people, forklifts, evaporator fans, defrost heaters (defrost adds a load and affects the run-time).
6. Sum and add a safety factor of about 10 percent (gated: unconfirmed, source is paywalled or blocked).

## Equipment sizing
Compressor run time is commonly assumed at 16-18 hours per day (gated: unconfirmed, source is paywalled or blocked), so size capacity as `Q_total x 24 / run hours`. Match evaporator TD (coil temperature difference, say 5-8 K for high-humidity rooms (gated: unconfirmed, source is paywalled or blocked)) to the humidity requirement: a low TD reduces product dehydration.

## Gotchas
- Pull-down load at loading is the peak; stage deliveries or size for it.
- Underestimating infiltration in busy dock doors.

## Verify
- [ ] Measured room temperature recovery after loading matches the design pull-down time.
