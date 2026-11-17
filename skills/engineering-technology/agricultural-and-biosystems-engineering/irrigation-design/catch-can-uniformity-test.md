---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.catch-can-uniformity-test
name: catch-can-uniformity-test
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, catch-can-test, sprinkler-design, sprinkler-irrigation-design, christiansen-uniformity, distribution-uniformity, asabe-s436, heermann-hein, irrigation-evaluation]
level: practitioner
status: gated
description: "Run a catch-can test to measure sprinkler uniformity: can layout, duration, wind check, Christiansen CU and low-quarter DU computation, and pivot weighting."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Catch-can uniformity test

**Goal:** a measured uniformity figure and a map that shows where the system is failing.

## Procedure
1. Choose calm conditions (wind below about 2-3 m/s for tests (gated: unconfirmed, source is paywalled or blocked); record the speed and direction).
2. Place identical cans in a grid between sprinklers (solid set), or in a line along a radius (pivot, per ASABE S436, which gives can spacing and number and the method; the S436.1 (2001) edition is listed inactive and a later field test procedure (2020) is listed as its replacement in a GlobalSpec catalogue entry, so confirm the current ASABE standard). Cans must be level, open at the same height, with open rims.
3. Run long enough to collect a meaningful depth (e.g. at least about 25 mm (gated: unconfirmed, source is paywalled or blocked), or per the standard).
4. Measure volumes in a graduated cylinder; convert to depth.
5. Compute:
   - Christiansen CU = `100 (1 - sum|x_i - x_avg| / (n x_avg))`.
   - Low-quarter DU = average depth of lowest 25 percent of the cans divided by the overall average.
   - For pivots weight cans by their distance (Heermann-Hein CU), since each can represents an annulus of area proportional to distance.
6. Plot the pattern; look for hot or dry zones, tower problems, worn nozzles.

## Interpret
CU values of about 85 percent or higher are typical targets for field crops (gated: unconfirmed, source is paywalled or blocked); lower values mean you are wasting water or under-irrigating areas.

## Gotchas
- Evaporation from cans in hot conditions: empty them promptly.
- Wind spoils the test; check against the wind ranges of the standard.

## Verify
- [ ] Repeat on the same lines for any repair to confirm improvement.
