---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.damper-valving-design
name: damper-valving-design
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [damper-valving, shim-stack, monotube, twin-tube, digressive, blow-off, adaptive-damper]
level: practitioner
status: gated
description: "Understand damper construction and valving: monotube and twin-tube, shim stacks and orifices, gas pressure, digressive curves and adaptive control."
sources:
  - "Dixon, The Shock Absorber Handbook"
  - "damper supplier technical documents"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Damper valving

1. Types: **twin-tube** (inner working tube, outer reserve tube with base valve) is compact, tolerant of mounting angle, common in passenger cars; **monotube** has a single tube with a floating gas piston, better heat dissipation and larger piston, with higher gas pressure and friction; used in performance cars.
2. Force: roughly `F = c*v^n` in orifice flow (n near 2 for pure orifice, closer to 1 for bleed or pre-load shims); piston valves with shim stacks create digressive curves: low-speed linear bleed, then shims open at higher speed for decreasing slope.
3. Tuning levers: bleed orifice size (low speed), shim stack stiffness/thickness/diameter (mid/high speed), preload, valve area; separate rebound and compression valves (base valve in a twin tube).
4. Gas: monotube gas pressure (often tens of bar (gated: unconfirmed, source is paywalled or blocked)) prevents cavitation and adds a gas spring force (rod area x pressure).
5. Temperature: oil viscosity change and fade at sustained high speed; check the thermal limit.
6. Adaptive dampers: solenoid valves (continuously variable) or magnetorheological fluids vary force in ms; calibrate with ride and handling targets and control logic.
7. Test on a damper dyno at multiple strokes and frequencies, plus noise (cavitation, hiss) listening.

**Gotchas:** cavitation noise, aeration; rod bearing friction.

## Verify
- [ ] Force-velocity curves match spec tolerance bands at several temperatures.
- [ ] Noise and cavitation checks in the rig pass.
