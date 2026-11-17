---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.mapped-motor-and-inverter-model
name: mapped-motor-and-inverter-model
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [mapped-motor-model, mapped-motor, inverter-efficiency, torque-limit, motor-loss-map, powertrain-blockset]
level: practitioner
status: gated
description: "Build a mapped traction motor and inverter model with torque envelope, loss map, DC power calculation and DC-bus voltage dependence."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "Powertrain Blockset: Mapped Motor (https://www.mathworks.com/help/autoblks/ref/mappedmotor.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Mapped motor and inverter model

1. Torque limit `Tmax(w, Vdc)`: constant torque to base speed, then constant power; reduce with falling DC voltage. Provide a generating (negative) side.
2. Request tracking: first-order or second-order lag on torque (the Powertrain Blockset Mapped Motor block uses a first-order lag with default time constant Tc = 0.02 s; typical drive values 5-20 ms (gated: unconfirmed, source is paywalled or blocked); use bench data).
3. Loss map `Ploss(w, T, Vdc)` from dyno combining motor + inverter; `Pdc = T*w + Ploss` for motoring (T > 0); the same expression with T negative gives the (negative) generated DC power.
4. Current for battery: `Idc = Pdc/Vdc`.
5. Temperature derating: scale Tmax by a function of winding/magnet temperature, or add a simple thermal node.
6. Use the Powertrain Blockset Mapped Motor block (torque-speed envelope, max torque/power pair or torque-speed-voltage envelope; loss or efficiency tables); otherwise 2-D/3-D Lookup Tables with clip extrapolation.

**Gotchas:** efficiency maps vs loss maps; interpolating efficiency near zero torque gives wild power values, so interpolate losses.

## Verify
- [ ] Power at base speed equals Tmax*w_base.
- [ ] Round-trip motoring then generating same point loses a plausible 2*loss amount.
