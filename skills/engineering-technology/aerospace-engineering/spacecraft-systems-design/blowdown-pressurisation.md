---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.blowdown-pressurisation
name: blowdown-pressurisation
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [blowdown, pressure-regulation, pressurant, blowdown-ratio, propulsion-subsystem, ullage]
level: practitioner
status: verified
description: "Size a blowdown propulsion tank, relating blowdown ratio to initial gas volume, and see how pressure and thrust fall during the mission."
sources:
  - "Sutton and Biblarz, Rocket Propulsion Elements"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Blowdown pressurisation

**Goal:** a simple, regulator-free feed system with predictable pressure decay.

## Relations
The tank holds propellant of volume `V_p` and an initial gas volume `V_g0`; tank volume `V_T = V_p + V_g0`. At end of life nearly all propellant is gone, so the final gas volume is about `V_T`.
- Pressure after expansion: `P_f = P_0 * (V_g0/V_T)^n`, with `n = 1` for slow isothermal expansion and `n = gamma` for adiabatic expansion; real tanks lie between (often use n between 1 and about 1.2 for helium with slow firing, check by analysis).
- Blowdown ratio `B = P_0 / P_f = (V_T/V_g0)^n`.
- So `V_g0 = V_T * B^(-1/n)` and `V_p = V_T * (1 - B^(-1/n))`.

## Effects
- Thrust and specific impulse fall with chamber pressure over life, roughly with feed pressure; flow rate and mixture ratio shift for bipropellant systems.
- A larger blowdown ratio lets you use more of the tank volume for propellant (a smaller gas volume) at the cost of a wider pressure range.
- Typical monopropellant blowdown ratios are in the range of about 3 to 4:1 (gated: unconfirmed, source is paywalled or blocked); confirm for the thruster's allowed inlet pressure range.

## Procedure
1. Get the thruster's inlet-pressure range (min and max) and the propellant volume needed.
2. Choose `B` to fit the range and compute `V_g0`, `V_T`.
3. Size the tank wall for maximum expected operating pressure (see propellant-tank-sizing).
4. Simulate the thrust history over the mission, including temperature effects.

## Gotchas
- Pressurant solubility in some propellants changes pressure behaviour.
- Thermal state changes pressure; include a margin for the temperature range.

## Verify
- [ ] The algebra was checked: `B = (V_T/V_g0)^n` gives `V_g0 = V_T B^(-1/n)`. The initial and final pressures from the formula match a tank-thermodynamics simulation within a few percent.
