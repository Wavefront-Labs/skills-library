---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.mapped-engine-model-from-test-data
name: mapped-engine-model-from-test-data
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [mapped-engine-model, mapped-engine, engine-map, torque-map, fuel-map, lookup-table, powertrain-blockset]
level: practitioner
status: gated
description: "Build a mapped engine model from dyno data: torque and fuel maps, idle and torque-response lag, with extrapolation and gridding pitfalls."
sources:
  - "Heywood, Internal Combustion Engine Fundamentals"
  - "Powertrain Blockset: Mapped SI Engine (https://www.mathworks.com/help/autoblks/ref/mappedsiengine.html)"
  - "Simulink n-D Lookup Table (https://www.mathworks.com/help/simulink/slref/ndlookuptable.html)"
  - "scatteredInterpolant (https://www.mathworks.com/help/matlab/ref/scatteredinterpolant.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Mapped engine model from test data

1. Gather steady-state dyno data on a speed x torque (or speed x throttle) grid; include motoring (negative torque) and idle.
2. Create maps: max torque vs speed (full load curve), fuel mass flow vs (speed, torque), friction/motoring torque. Grid with `griddata` or `scatteredInterpolant`, then resample on a regular grid; check the edges.
3. Use the Powertrain Blockset Mapped SI Engine block (brake torque map vs commanded torque and speed, fuel mass flow map; the CI variant should be checked in your release) or build with 2-D Lookup Tables; set extrapolation to Clip (the lookup block default is Linear), never linear, outside the tested envelope.
4. Dynamics: the Mapped SI Engine block has no general response-time model (only optional turbocharger lag), so add a first-order lag on torque (time constant tens to a few hundred ms depending on engine and boost (gated: unconfirmed, source is paywalled or blocked)); separate rotational inertia.
5. Fuel cut-off in overrun and idle controller (PI to hold target idle speed).
6. Validate on a transient test, not just the maps used to build them.

**Gotchas:** maps measured warm; cold-start fuel and friction are different. Fuel maps in g/s vs BSFC maps: be explicit about units.

## Verify
- [ ] Cycle fuel prediction within a few percent of test on a held-out cycle.
- [ ] Torque never exceeds full-load curve; fuel is zero in cut-off.
