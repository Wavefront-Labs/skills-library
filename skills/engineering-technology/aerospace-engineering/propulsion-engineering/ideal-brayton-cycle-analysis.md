---
id: engineering-technology.aerospace-engineering.propulsion-engineering.ideal-brayton-cycle-analysis
name: ideal-brayton-cycle-analysis
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, gas-turbine, brayton-cycle, ideal-brayton, thermal-efficiency, specific-work, pressure-ratio, turbine-inlet-temperature]
level: practitioner
status: verified
description: "Analyse the ideal Brayton cycle for gas turbines: thermal efficiency, specific work, the optimum pressure ratio, and why real cycles depart from it."
sources:
  - "Mattingly, Elements of Propulsion: Gas Turbines and Rockets"
  - "Hill and Peterson, Mechanics and Thermodynamics of Propulsion"
  - "Saravanamuttoo et al., Gas Turbine Theory"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Ideal Brayton cycle

**Goal:** cycle-level intuition and first numbers for a gas turbine.

## Relations (cold-air standard, constant specific heats)
- Thermal efficiency: `eta_th = 1 - pi_c^(-(gamma-1)/gamma)` where `pi_c` is the compressor pressure ratio. Efficiency rises with pressure ratio only.
- Specific work, in terms of `theta = T3/T1`: `w_net/(cp T1) = theta (1 - 1/x) - (x - 1)` with `x = pi_c^((gamma-1)/gamma)`.
- Pressure ratio for maximum specific work: `x_opt = sqrt(theta)`, i.e. `pi_opt = theta^(gamma/(2(gamma-1)))`.
- Efficiency and work optimise at different pressure ratios: engines for efficiency (airliners) use high `pi_c`; engines for compactness or power-to-weight use lower `pi_c` near the work optimum.

## Real cycle departures
Component efficiencies below 1, pressure losses in intake, combustor (about 4-6% (gated: unconfirmed, source is paywalled or blocked)) and nozzle, cooling air bleed, variable specific heats (cp rises, gamma falls with temperature). Use a cycle program (GasTurb, a custom script or NPSS) for real numbers.

## Procedure
1. Choose `T3` (turbine inlet) and `pi_c`.
2. Compute ideal efficiency and work; compare to real engine data (turbofan overall pressure ratio 30-50 in modern high-bypass engines (gated: unconfirmed, source is paywalled or blocked)).
3. Add component efficiencies (see that skill) to get a realistic estimate.

## Verify
- [ ] The work optimum `x_opt = sqrt(theta)` was confirmed by numerical scan (theta 6 gives 2.449). Ideal efficiency at `pi_c = 10`, `gamma = 1.4` is about 48% (`1 - 10^-0.2857`).
