---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.hybrid-supervisor-mode-logic
name: hybrid-supervisor-mode-logic
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [hybrid-supervisor, hybrid-mode-logic, ev-mode, engine-start-stop, torque-split, stateflow]
level: practitioner
status: draft
description: "Structure a hybrid supervisor in Stateflow with EV, hybrid and engine-only modes, start-stop transitions, anti-chatter guards and torque-split outputs."
sources:
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
  - "Stateflow documentation (mathworks.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Hybrid supervisor mode logic

1. Modes: `EV`, `Series/Charge`, `Parallel`, `EngineOnly`, `Regen`, plus `Starting` and `Stopping` transitional states.
2. Mode requests from power demand and SOC with **hysteresis** (engine on above X kW or SOC below low, off only after demand below Y and SOC above a higher value).
3. Minimum engine on-time and off-time (a few seconds to tens of seconds) to prevent start/stop chatter and emissions penalty.
4. Starting: motor cranks, fuel enabled after speed threshold; torque filler from motor while engine ramps.
5. Torque split outputs: engine torque request, motor torque request, brake request, each clipped to component limits and summing to driver request.
6. Fault degradation: lose motor -> engine only; lose engine -> EV-limited limp.

**Gotchas:** logic that fights the energy-management strategy; implement a clear interface (mode, torque targets) and keep optimisation in a separate block.

## Verify
- [ ] Drive-cycle run shows no on/off cycles shorter than the minimum time.
- [ ] Sum of component torques equals driver demand within a stated tolerance in every mode.
