---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.series-hybrid-and-range-extender
name: series-hybrid-and-range-extender
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [series-hybrid, range-extender, rex, engine-generator, genset, hybrid-architecture]
level: practitioner
status: draft
description: "Size a series hybrid or range-extender: motor and battery for performance, genset for sustained load, operating strategy and NVH from decoupled engine speed."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Series hybrid and range extender

1. Architecture: engine drives a generator producing electrical power for the battery/motor; no mechanical path to the wheels.
2. Size the motor for the performance targets (as for an EV). Size the battery for EV range and peak power; for a REx the genset only sustains average power.
3. Genset power: from continuous requirement, e.g. highway cruise power at maximum speed/grade plus auxiliaries, divided by generator and inverter efficiency; typically smaller than the motor peak.
4. Operating strategy: thermostat (on/off) or power-following; run the engine at the best-efficiency point or along an optimal line; hold SOC in a band.
5. NVH: engine speed decoupled from vehicle speed can annoy (engine "droning"); tie engine speed loosely to vehicle speed or load.
6. Efficiency: series path has double conversion losses; best for stop-go duty; high-speed efficiency lower than parallel.
7. Regulation: range extender rules vary (battery electric vehicle definitions, emissions, charging).

**Gotchas:** thermal limits of the generator and inverter at sustained power.

## Verify
- [ ] Sustained-speed and grade requirement met without battery depletion.
- [ ] Fuel use simulated over a cycle with the chosen strategy.
