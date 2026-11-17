---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.thrust-blocks-and-pipe-anchoring
name: thrust-blocks-and-pipe-anchoring
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, thrust-blocks, pipe-anchoring, restrained-joints, thrust-force, bearing-capacity, pvc-pipe-fittings]
level: advanced
status: verified
description: "Design thrust restraint for pressurised pipelines: thrust force at bends, tees and dead ends, soil bearing, block sizing and restrained-joint alternatives."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Thrust blocks and pipe anchoring

**Goal:** prevent joint pull-out at fittings under test and working pressure.

## Forces
Pressure acting on a change of direction or a closure produces thrust. For dead ends and tees: T = P x A (internal pressure times cross-section area based on the pipe outside diameter for the joint). For a bend with deflection angle theta: T = 2 x P x A x sin(theta/2) (computed: a 90 degree bend gives 1.414 PA). A qualified engineer must design thrust restraint; follow the pipe manufacturer's and the governing standard's method. Use the test pressure when it exceeds the working pressure, and consider surge.

## Restraint
- Concrete thrust blocks bear against undisturbed soil: area required = T / allowable soil bearing pressure with a safety factor. Allowable bearing is from a soil investigation or conservative local table values, not guessed.
- Block shape: pour against undisturbed trench wall, cover the fitting back but leave joints and bolts accessible.
- Restrained-joint pipe and fittings (mechanical or push-on with locking features) transfer thrust by friction and are used when blocks are impractical; the restrained length is from the manufacturer's design method.
- Vertical bends need weight or tie-down.
- Do not backfill or pressure test before concrete has cured sufficiently (follow the specification).

## Verify
- [ ] Thrust calculation at test pressure documented.
- [ ] Inspection before covering; leak check at test pressure.
- Unconfirmed: allowable soil bearing for your site; use a geotechnical value.
