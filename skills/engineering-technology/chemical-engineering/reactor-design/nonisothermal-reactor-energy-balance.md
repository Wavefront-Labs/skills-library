---
id: engineering-technology.chemical-engineering.reactor-design.nonisothermal-reactor-energy-balance
name: nonisothermal-reactor-energy-balance
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-heat-effects-and-stability, nonisothermal-reactor-energy-balance, energy-balance, nonisothermal-reactor, adiabatic-pfr, heat-exchange, xt-plot, reactor-temperature-profile, jacketed-reactor, reaction-enthalpy]
level: advanced
status: verified
description: "Write and solve energy balances for nonisothermal PFR, CSTR and batch reactors, including heat exchange terms and the X-T relationship, with a worked adiabatic CSTR check."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nonisothermal reactor energy balances

**Goal:** temperature and conversion profiles that feed into sizing and safety.

## Equations
- **PFR**: dT/dV = [(-Delta H_r)(-r_A) - U a (T - T_a)] / (sum F_i c_p,i)  (a = heat transfer area per unit volume).
- **CSTR steady state**: sum F_i0 c_p,i (T - T0) = (-Delta H_r) F_A0 X - U A (T - T_a), together with V = F_A0 X/(-r_A(T, X)).
- **Batch**: N c_p dT/dt = (-Delta H_r)(-r_A) V - U A (T - T_a).
- **Adiabatic X-T** (checked: integrating the adiabatic PFR species and energy balances numerically reproduces this relation to 1e-15): X = c_p,mix (T - T0) / (-Delta H_r) per unit of A fed (constant c_p form).

## Procedure
1. Write the species balances and the energy balance; ensure heat of reaction at T is used (Delta H_r(T) = Delta H_r(Tref) + integral of Delta c_p dT).
2. Choose the heat exchange model: adiabatic, constant wall temperature, coolant balance for co- or counter-current coolant.
3. Solve numerically as ODEs (PFR) or nonlinear algebraic equations (CSTR).
4. Plot T, X and rate along the reactor; identify hot spots and approach to equilibrium.
5. Check the maximum temperature against material and catalyst limits.

## Practice
- For reversible exothermic reactions, plot X-T with the equilibrium curve and the rate contours; the optimum temperature trajectory decreases with conversion (interstage cooling).
- For endothermic reactors (reforming), tube-wall heat flux limits.

## Gotchas
- Heat transfer coefficient inside packed beds is much lower than for empty tubes; use bed correlations.
- Sign conventions of Delta H_r.

## Verify
- [ ] Energy closes: heat released equals sensible heat gain plus heat removed.
- [ ] Results compared to adiabatic limit and isothermal limit as bounds.
