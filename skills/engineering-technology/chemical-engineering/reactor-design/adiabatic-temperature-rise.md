---
id: engineering-technology.chemical-engineering.reactor-design.adiabatic-temperature-rise
name: adiabatic-temperature-rise
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-heat-effects-and-stability, adiabatic-temperature-rise, delta-t-ad, heat-of-reaction, thermal-hazard, exothermic-reaction, dilution, heat-capacity, reaction-severity]
level: practitioner
status: verified
description: "Calculate adiabatic temperature rise from heat of reaction, concentration and heat capacity, and use it to judge reactor type, dilution needs and runaway severity."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adiabatic temperature rise

**Goal:** the maximum temperature rise if no heat is removed, as a first screen of thermal severity.

## Formula
For a liquid reaction at full conversion of limiting reactant A:
Delta T_ad = (-Delta H_r) C_A0 / (rho c_p) = (-Delta H_r) w_A0 / c_p (mass basis),
with Delta H_r per mole of A, C_A0 in mol per m3, rho c_p the volumetric heat capacity of the mixture. At partial conversion X multiply by X.
Worked example: -Delta H_r = 100 kJ/mol, C_A0 = 2000 mol/m3, rho c_p = 4.0 MJ/m3/K gives Delta T_ad = 100e3 x 2000 / 4.0e6 = 50 K (recomputed).

## Gas-phase and variable heat capacity
Use the mean heat capacity of the stream and the enthalpy balance X-T relation: T = T0 + (-Delta H_r) X / (sum theta_i c_p,i + X Delta c_p).

## Use
1. Rank reactions: Delta T_ad of tens of K is manageable with a jacket; hundreds of K needs careful design (gated: unconfirmed, source is paywalled or blocked) (dilution, staged feed, quench, heat-exchange reactor).
2. Compare Delta T_ad to the difference between the operating temperature and the temperature at which a secondary decomposition starts: if the sum exceeds it, the secondary event is possible after loss of cooling; refer to calorimetry and the hazard study.
3. Set the semibatch feed policy (see `engineering-technology.chemical-engineering.reactor-design.batch-and-semibatch-design`).

## Gotchas
- Use the heat of reaction at the actual temperature and phase, and include heat of mixing or vaporisation of solvent if relevant.
- A solvent that boils absorbs heat; this limits temperature but raises pressure.

## Verify
- [ ] Hand calculation compared to the simulator or calorimetry.
- [ ] Units checked (kJ/mol, mol/m3, J/m3/K).
