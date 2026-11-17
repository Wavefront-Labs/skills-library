---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.tyre-load-sensitivity
name: tyre-load-sensitivity
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [load-sensitivity, tyre-load-sensitivity, friction-coefficient, load-transfer, tyre-behaviour, cornering-stiffness]
level: practitioner
status: draft
description: "Quantify how tyre grip falls with vertical load, and use it to see why load transfer costs axle grip and how it shifts balance."
sources:
  - "Pacejka, Tire and Vehicle Dynamics"
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Tyre load sensitivity

**Goal:** predict axle lateral force from tyre curves and see the effect of load transfer on balance.

- Peak friction falls with load: `mu(Fz) = mu0 - k*(Fz - Fz0)/Fz0`-style; in practice read the peak lateral force `Fy_peak(Fz)` from tyre test data, which is concave (doubling load gives less than double force).
- Axle effect for two tyres with loads `F0 +/- dF`: because Fy(Fz) is concave, `Fy(F0+dF)+Fy(F0-dF) < 2*Fy(F0)`. More lateral load transfer at an axle means less total axle force at the same slip angle.
- Balance rule: the axle that sees the larger load-transfer fraction loses more grip and slides first. Adding front roll stiffness raises front transfer, pushing toward understeer; the reverse for the rear.
- Cornering stiffness `C_alpha` also varies with load, peaking at a tyre-dependent load; stay near the load of the tyre's rated range.
- Use tyre-test data (flat-trac or manufacturer fits) at the operating pressure and camber; do not reuse a different tyre's numbers.

**Gotchas:** friction depends on road surface and temperature, so quote the test surface.

## Verify
- [ ] Plot axle Fy vs slip for several transfer levels; Fy_max drops as transfer rises.
- [ ] Predicted balance change direction agrees with a track test.
