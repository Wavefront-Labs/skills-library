---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.reliability-prediction
name: reliability-prediction
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [reliability-prediction, failure-rate, mil-hdbk-217, parts-count, reliability-block-diagram, reliability-fdir]
level: practitioner
status: draft
description: "Predict spacecraft reliability from part failure rates and block diagrams, with series and redundant models, and know where handbook predictions mislead."
sources:
  - "MIL-HDBK-217F"
  - "ECSS-Q-ST-30 (dependability)"
  - "Fortescue et al., Spacecraft Systems Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Reliability prediction

**Goal:** a numerical estimate of mission reliability to compare designs and find weak spots.

## Method
1. List units and their parts; take failure rates `lambda` (failures per hour or per billion hours, FIT) from a handbook or supplier data. Handbook options include MIL-HDBK-217F (parts count and parts stress methods; last revised in the 1990s), Telcordia SR-332, FIDES; each has different assumptions.
2. Build a reliability block diagram: series (all must work), parallel (one of N), k-of-N, with standby and cross-strapping.
3. Compute reliability `R(t) = exp(-lambda t)` for constant failure rate; series `R = product(R_i)`.
4. Identify the contributors with highest failure rate; compare architecture options.
5. Combine with FMEA (see fmea-for-spacecraft) to confirm the failure modes and effects.

## Practice
- Use predictions for relative comparison and allocation; absolute numbers are uncertain by a large factor.
- Consider infant mortality and wear-out (mechanisms, batteries, wheels) separately; constant failure rate does not apply to wear-out.
- Include software and operations contributions where the programme requires it.
- Track assumptions: temperature, environment factor, quality level.

## Gotchas
- Handbook failure rates can be pessimistic for modern parts and ignore workmanship.
- Redundancy gains vanish if common-cause failures dominate.

## Verify
- [ ] A hand calculation of a small series-parallel example matches the tool.
