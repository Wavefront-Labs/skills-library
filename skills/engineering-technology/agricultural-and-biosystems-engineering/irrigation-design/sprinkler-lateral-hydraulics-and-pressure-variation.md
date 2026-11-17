---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.sprinkler-lateral-hydraulics-and-pressure-variation
name: sprinkler-lateral-hydraulics-and-pressure-variation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, sprinkler-lateral-hydraulics, sprinkler-design, sprinkler-irrigation-design, friction-loss, hazen-williams, pressure-variation, aluminum-pipe]
level: practitioner
status: gated
description: "Size sprinkler laterals so pressure variation along the lateral is under 20 percent of nozzle pressure, using friction with the outlet factor and elevation corrections."
sources:
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "NRCS Conservation Practice Standard 442, Sprinkler System, Vermont 2017 (https://efotg.sc.egov.usda.gov/api/CPSFile/21967/442_VT_CPS_Sprinkler_System_2017)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sprinkler lateral hydraulics and pressure variation

**Goal:** all sprinklers on a lateral run within an acceptable pressure range, so flow varies by no more than about 10 percent.

## Rule of thumb
Pressure difference along the lateral (friction plus elevation) is limited to about 20 percent of the design nozzle pressure (NRCS Standard 442, Vermont 2017: 20 percent of average design operating pressure, or 10 percent of design flow); at x = 0.5 this gives about 10 percent flow variation.

## Steps
1. Choose the lateral diameter from the standard pipe sizes (irrigation aluminium, PVC).
2. Friction loss over the length: Hazen-Williams with C near 130-150 (aluminium with couplers is lower, about 120-130) (gated: unconfirmed, source is paywalled or blocked) or a vendor chart; reduce by the multiple-outlet factor F (Christiansen), which depends on the number of outlets and whether the first outlet is at half spacing or full spacing. Take F from tables.
3. Elevation: downhill laterals gain head; uphill laterals lose.
4. Operating pressure at the lateral's inlet: `P_in = P_nozzle + 0.75 hf + riser height +/- elevation effect` (the 0.75 factor (gated: unconfirmed, source is paywalled or blocked) is the textbook estimate that places the average pressure at the 'average' sprinkler for level laterals); revise by calculation.
5. For laterals with riser connections and valves, add minor losses.
6. For long laterals use telescoped diameters or pressure-regulating valves.

## Gotchas
- High pressure variation changes the application depth by section.
- Water hammer on valve closure (see surge skill) can burst aluminium pipe.

## Verify
- [ ] Gauge at the first and last sprinkler within design variation.
