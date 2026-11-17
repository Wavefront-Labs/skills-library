---
id: engineering-technology.automotive-vehicle-engineering.powertrain-design.power-split-ecvt-hybrids
name: power-split-ecvt-hybrids
category: engineering-technology
field: automotive-vehicle-engineering
product: powertrain-design
tags: [power-split, ecvt, planetary-gear, input-split, willis-equation, hybrid-transmission]
level: practitioner
status: gated
description: "Analyse a planetary power-split hybrid: speed relations from the Willis equation, torque relations, electrical power circulation and operating point choice."
sources:
  - "Ehsani et al., Modern Electric, Hybrid Electric and Fuel Cell Vehicles"
  - "Guzzella and Sciarretta, Vehicle Propulsion Systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Power-split eCVT hybrids

1. Layout (input-split, Toyota-style): engine on planet carrier, generator MG1 on sun, motor MG2 and the output on ring (matches the Wikipedia Hybrid Synergy Drive description of generation 1/2, secondary source). Variants differ; use the actual layout.
2. Speed relation (Willis): `Zs*omega_s + Zr*omega_r = (Zs + Zr)*omega_c`. Engine speed is set by choosing generator speed for a given vehicle speed: the CVT action.
3. Torque relation: with carrier torque Tc, `Ts = Tc*Zs/(Zs + Zr)`, `Tr = Tc*Zr/(Zs + Zr)` (ignoring inertia and losses; checked numerically for Zs = 30, Zr = 78: Ts + Tr = Tc, ring share 72%, and engine power equals Ts*omega_s + Tr*omega_r). The ring carries the majority of engine torque to the wheels mechanically; the sun reacts through the generator.
4. Power split: electrical path fraction depends on speed ratio; at high vehicle speed with low engine speed power may circulate (MG2 generating, MG1 motoring: the 'high gear' loop), increasing losses.
5. Operating point: pick engine speed and torque on the optimal operating line for the power request; the generator speed follows from the relation; the motor adds or recovers torque at the ring.
6. Limits: generator speed limit, battery power, MG torque, engine start (via MG1).

**Gotchas:** sign conventions and power circulation; verify with energy balance.

## Verify
- [ ] Speed and torque relations satisfied in simulation at several points.
- [ ] Energy balance: engine fuel power = wheel + electrical + losses.
