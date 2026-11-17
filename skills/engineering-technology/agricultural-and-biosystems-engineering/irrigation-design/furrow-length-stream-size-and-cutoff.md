---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.furrow-length-stream-size-and-cutoff
name: furrow-length-stream-size-and-cutoff
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, furrow-design, furrow-irrigation, stream-size, cutoff-time, tailwater, intake-family, erosion-limit]
level: advanced
status: gated
description: "Design furrow irrigation: soil intake, advance time, non-erosive stream size, cutoff time, furrow length, runoff and uniformity with a volume balance."
sources:
  - "Walker & Skogerboe, Surface Irrigation: Theory and Practice"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Furrow length, stream size and cutoff

**Goal:** a furrow length and inflow that wets the whole furrow to the required depth with limited runoff and no erosion.

## Inputs
Soil intake (infiltration) per furrow wetted perimeter (measure; see `infiltration-measurement-and-models`), furrow slope, spacing, roughness (Manning n), net depth required (soil, crop and management allowed depletion).

## Procedure
1. Maximum non-erosive stream size: a commonly used rule is Qmax = c/S, with Qmax in L/s, slope S in percent and c about 0.6 (gated: unconfirmed, source is paywalled or blocked); confirm locally because soils differ (the rule is an upper bound, test on site).
2. Required intake opportunity time: from the intake function find the time to infiltrate the net depth.
3. Advance and recession: from a volume balance or simulation (WinSRFR from USDA-ARS) compute advance time versus length for the chosen stream; the intake opportunity time at the end is the cutoff time minus advance time to the end plus recession lag.
4. Choose length so the end of the furrow receives the needed time without excessive deep percolation at the head; trade off length (cost, labour) against uniformity.
5. Cutoff: typically when the stream reaches the end or after a set fraction; with cutback or reuse systems use stream-size reduction to limit runoff.

## Practice
- Slope may be flat for blocked-end or short furrows; large streams on steep slopes erode.
- Tailwater should be collected and re-used or managed; compact furrows (wheel rows) carry water more consistently.

## Verify
- [ ] Measured advance matches prediction within a reasonable margin.
- [ ] Distribution uniformity and application efficiency computed from field evaluation (`advance-recession-field-evaluation`).
- Unconfirmed: soil-specific limits; test on site.
