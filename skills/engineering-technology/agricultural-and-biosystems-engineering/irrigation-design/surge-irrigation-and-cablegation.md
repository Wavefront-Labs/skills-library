---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.surge-irrigation-and-cablegation
name: surge-irrigation-and-cablegation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, surge-irrigation, cablegation, intermittent-flow, surge-valve, cycle-time, advance-phase]
level: advanced
status: gated
description: "Apply surge flow or cablegation to furrows: cycle times, ratios, soil conditions where it helps, valve controller setup and how to evaluate the gain."
sources:
  - "Walker & Skogerboe, Surface Irrigation: Theory and Practice"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Surge irrigation and cablegation

**Goal:** improve furrow advance and uniformity, or save water, by delivering the stream in pulses instead of continuously.

## How it works
Alternate on and off cycles to alternate sets of furrows. Wetting and drying consolidates the surface so the intake rate of the wetted portion drops, which speeds the next advance and lets water reach the end with less deep percolation at the head. The benefit varies by soil: cracking and highly structured soils may respond more strongly, and benefit is smaller or absent on some soils. Do not assume gains; test.

## Setup
- A surge valve (automatic two-way gated pipe valve with a controller) alternates between two outlet sides. Controller settings include cycle on-time, number of cycles for the advance phase, and then a cutback or continuous flow phase to finish.
- Common planning approach: choose the cycle time so each cycle advances a fixed distance and gradually raise the advance; the controller can use a time-based or distance ratio. Follow the vendor guide and local extension or NRCS practice standard for the settings.
- Cablegation uses a plug pulled through gated pipe by a cable at a controlled speed to shift flow gradually to successive outlets, a low-cost automation for graded furrows.

## Evaluate
Run an irrigation evaluation with and without surge (`advance-recession-field-evaluation`) and compare application efficiency and uniformity; the gain varies with soil and slope.

## Verify
- [ ] Controller cycle log recorded.
- [ ] Measured advance per cycle compared to plan.
- Expected savings depend on soil and are unconfirmed here (gated: unconfirmed, source is paywalled or blocked); use field trials.
