---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.substrate-irrigation-and-drain-to-waste-control
name: substrate-irrigation-and-drain-to-waste-control
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, substrate-irrigation, drain-to-waste, rockwool, coconut-coir, drain-fraction, irrigation-steering, substrate-moisture, hydroponics]
level: advanced
status: draft
description: "Control irrigation of substrate crops: rockwool and coco, radiation-sum triggers, drain fraction targets, substrate EC and moisture steering, and runoff management."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Substrate irrigation and drain-to-waste control

**Goal:** keep the root zone at the right water content and EC for the crop's balance of vegetative and generative growth, with controlled runoff.

## Principles
- Substrate crops (rockwool slabs, coir, perlite, peat) are irrigated by drippers; each irrigation event is a short shot of solution. The drain is the solution that runs out of the substrate, measured as a percentage of the applied volume (drain fraction).
- Timing is commonly triggered by the accumulated solar radiation since the last irrigation (so irrigation tracks crop demand), with start and stop times in the day and a minimum interval; plus a maximum interval and a low substrate water-content trigger.

## Steering
- Typical drain fractions on tomato and similar crops are in the range of about 20-40 percent in the active season, set by the grower to flush salts and keep EC uniform; the right value depends on the water quality and the crop.
- The substrate water content and EC (measured by in-slab sensors or weighed slabs) steer the plant: drier, higher EC conditions push generative growth (flowering and fruit), wetter, lower EC conditions push vegetative growth. Make changes gradually, within the limits given by the crop adviser.
- Overnight: allow the substrate to dry down by a set amount before the first irrigation in the morning and avoid late irrigation.
- Compare the EC and pH of the drain with those of the feed; a drain EC much higher than the feed indicates salt build-up, requiring more drain or lower feed EC.

## Runoff management
- Free drain-to-waste systems lose water and nutrients; many regions require collection and reuse or treatment because of nitrate and phosphate regulation. Recycle the drain through disinfection (`recirculating-solution-disinfection`) where permitted.

## Verify
- [ ] Drain fraction, drain EC and pH measured daily from a set of reference slabs.
- [ ] Sensor readings checked against slab weights.
- Unconfirmed: target drain fractions and EC by crop and region.
