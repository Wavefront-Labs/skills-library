---
id: engineering-technology.aerospace-engineering.propulsion-engineering.off-design-engine-matching
name: off-design-engine-matching
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, gas-turbine, brayton-cycle, off-design, component-matching, running-line, choked-flow, cycle-deck]
level: advanced
status: draft
description: "Match gas turbine components off design: choked turbine nozzle flow, compressor running line, shaft power balance and the iteration scheme behind cycle decks."
sources:
  - "Saravanamuttoo, Rogers and Cohen, Gas Turbine Theory"
  - "Walsh and Fletcher, Gas Turbine Performance"
  - "Mattingly, Aircraft Engine Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Off-design engine matching

**Goal:** engine performance when speed, altitude or throttle differ from the design point.

## Principles
- Each component has a map: compressor pressure ratio and efficiency vs corrected flow and corrected speed; turbine flow capacity vs pressure ratio and efficiency.
- Constraints: mass-flow continuity (accounting for fuel and bleeds), shaft power balance (turbine work = compressor work + losses), and nozzle flow compatibility. With a choked turbine nozzle guide vane, turbine corrected flow is fixed, which fixes the compressor operating line (running line).

## Procedure (single-spool turbojet example)
1. Guess compressor corrected speed and a beta line position on the map; read pressure ratio and efficiency and corrected flow.
2. Compute compressor exit conditions and the work.
3. Choose the turbine entry temperature (fuel flow) consistent with the throttle setting; compute combustor exit conditions with pressure loss.
4. Check the flow-capacity match with the turbine; iterate on the beta line until the turbine flow equals the compressor flow plus fuel, and work balances.
5. Calculate nozzle conditions and thrust; step through throttle settings to build the running line.
6. Check surge margin along the line at acceleration (transient fuel schedules).

## Practice
- Commercial tools (GasTurb, NPSS, GSP) solve this with Newton iteration of the independent variables (beta, corrected speed, TET) and the error terms (flow, work, nozzle); use tool defaults with generic maps unless real maps are available.
- Scale generic maps to the design point.

## Gotchas
- Using a generic map gives believable but not engine-specific numbers.
- Altitude and Mach effects enter through corrected parameters; check the reference conditions.

## Verify
- [ ] The design point of the off-design model reproduces the cycle design point.
