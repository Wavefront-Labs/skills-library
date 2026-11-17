---
id: engineering-technology.aerospace-engineering.propulsion-engineering.liquid-rocket-feed-cycles
name: liquid-rocket-feed-cycles
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [feed-cycles, gas-generator-cycle, staged-combustion, expander-cycle, pressure-fed, rocket-engines]
level: practitioner
status: draft
description: "Compare pressure-fed, gas-generator, expander and staged-combustion liquid rocket feed cycles by performance, complexity and where each fits in civil launch."
sources:
  - "Sutton and Biblarz, Rocket Propulsion Elements"
  - "Huzel and Huang, Design of Liquid Propellant Rocket Engines"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Liquid engine feed cycles

**Goal:** choose a cycle that fits the mission, thrust level and reliability goal.

## Cycles
- **Pressure-fed**: tanks pressurised by gas; no turbopumps. Simple and reliable, but tank pressure raises tank mass, limiting chamber pressure and size. Used for spacecraft thrusters and some small stages.
- **Gas generator**: a small combustor drives the turbine; the exhaust is dumped overboard or into the nozzle. Mature and robust; the dumped turbine flow costs specific impulse. Merlin is a well-known example.
- **Expander**: propellant (usually hydrogen) is heated in the chamber walls and drives the turbine; no burnt gas goes through the turbine, giving good efficiency, but chamber heat limits power so it suits smaller engines (RL10 is a classic example).
- **Staged combustion**: preburner gas passes through the turbine and then into the main chamber, so no propellant is wasted; chamber pressure can be high. Fuel-rich versions (RS-25) and oxidiser-rich versions (RD-180 family) exist; full-flow staged combustion uses both preburners (Raptor).
- **Electric pump-fed**: battery-driven motors drive the pumps (Rutherford); good for small engines where battery mass is acceptable.

## Selection
1. Required thrust and chamber pressure; pressure-fed above a size becomes heavy.
2. Specific impulse and cost targets, and reusability: cycles without dumped gas and with lower turbine temperature suit reuse.
3. Development risk: oxidiser-rich staged combustion needs materials that tolerate hot oxygen-rich gas.
4. Throttle, restart and engine-out behaviour.

## Gotchas
- Cycle names are not a ranking; the best choice depends on mission.
- Turbopump start transients and combustion stability drive development cost.

## Verify
- [ ] The cycle choice is justified with delta-v or mass impact from the rocket equation (see rocket-equation-and-staging).
