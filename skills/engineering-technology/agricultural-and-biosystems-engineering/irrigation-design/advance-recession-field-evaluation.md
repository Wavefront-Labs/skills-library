---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.advance-recession-field-evaluation
name: advance-recession-field-evaluation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, advance-recession, irrigation-evaluation, surface-irrigation-evaluation, two-point-method, winsrfr, intake-estimation]
level: advanced
status: gated
description: "Evaluate surface irrigation in the field: station layout, advance and recession timing, inflow and runoff measurement, intake estimate and efficiency calculation."
sources:
  - "Walker & Skogerboe, Surface Irrigation: Theory and Practice"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Field evaluation of advance and recession

**Goal:** measure what a surface irrigation does, estimate soil intake, and calculate efficiency and uniformity.

## Procedure
1. Choose representative furrows or border strips (several, to cover variability) and stake stations at regular intervals (commonly about 30 m or 100 ft (gated: unconfirmed, source is paywalled or blocked)).
2. Measure inflow with a flume, weir or flow meter, and runoff (tailwater) at the end.
3. Record advance time at each station (water arrival) and recession time (water leaves the surface). Record the cutoff time.
4. Measure the furrow or border cross-section and slope at several points, and soil moisture before and some days after.
5. Estimate infiltration from the volume balance (inflow minus surface storage minus runoff gives infiltrated volume) using a two-point or multi-point method; software such as WinSRFR (USDA-ARS) performs this.
6. Compute distribution uniformity (low-quarter), application efficiency, deep percolation and runoff fractions, and requirement efficiency.

## Using results
Adjust inflow, cutoff time or length to improve; re-evaluate. The same data calibrate a simulation for design options.

## Pitfalls
Single furrow sampling hides variability; soil cracking makes intake time-varying; unmeasured tailwater. Check flow measurement and repeat.

## Verify
- [ ] Volume balance closes within a few percent (gated: unconfirmed, source is paywalled or blocked).
- [ ] Efficiency terms defined as in `application-and-project-efficiency-definitions`.
