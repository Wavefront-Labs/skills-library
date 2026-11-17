---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.flow-delay-and-header-position-settings
name: flow-delay-and-header-position-settings
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, flow-delay, yield-monitor, yield-mapping, grain-transport-delay, gps-lag, header-switch, test-pass]
level: practitioner
status: draft
description: "Set and test yield monitor flow delay and header position offsets so that yield is assigned to the correct location, and diagnose lagged or smeared maps."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Flow delay and header position settings

**Goal:** place each yield value where the grain was actually cut.

## Concepts
Grain takes time to travel from the header through the threshing system and clean-grain elevator to the flow sensor, typically around 10-15 seconds, depending on machine, crop and speed. Without correcting for this delay, yield values are placed behind the combine in the wrong location and yield maps appear shifted or smeared. GPS latency adds a small offset.

## Delay test
1. Choose a field area with a sharp boundary (for example the edge of a strip or a cut/uncut transition).
2. Harvest across the boundary at normal speed, then repeat in the opposite direction.
3. Plot the yield profile for each direction; the delay that aligns the two opposite-direction profiles is the correct flow delay value (the profiles separate by twice the delay times speed if wrong).
4. Enter the delay (and header delay, i.e. the time between header lift/lower and the flow signal ceasing or starting) in the monitor.
5. Re-test when you change crop, machine, or setup.

## Header position
Set the header height sensor threshold so that the monitor records zero when the header is lifted; set the start-of-pass and end-of-pass delays accordingly (see cleaning skill).

## Gotchas
- A different crop or combine speed changes the transport time; set per crop.
- Variation of flow delay with throughput exists but is usually minor within normal flow range.

## Verify
- [ ] Opposite-direction passes over the same feature overlay after the new delay setting.
