---
id: engineering-technology.aerospace-engineering.propulsion-engineering.component-efficiencies-polytropic-isentropic
name: component-efficiencies-polytropic-isentropic
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [component-efficiency, polytropic-efficiency, isentropic-efficiency, gas-turbine-cycles, compressor, turbine]
level: practitioner
status: gated
description: "Convert between isentropic and polytropic efficiency for compressors and turbines, and choose component efficiencies and pressure ratios for cycle analysis."
sources:
  - "Mattingly, Elements of Propulsion"
  - "Hill and Peterson, Mechanics and Thermodynamics of Propulsion"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Component efficiencies

**Goal:** consistent efficiency definitions for an engine cycle model.

## Definitions (calorically perfect gas, total quantities)
- Compressor isentropic: `eta_c = (pi_c^((g-1)/g) - 1) / (tau_c - 1)`.
- Compressor polytropic (small-stage): `tau_c = pi_c^((g-1)/(g e_c))`.
- Turbine isentropic: `eta_t = (1 - tau_t) / (1 - pi_t^((g-1)/g))`.
- Turbine polytropic: `tau_t = pi_t^((g-1) e_t / g)`.
- Isentropic efficiency of a compressor falls as `pi_c` rises for fixed `e_c`; polytropic efficiency is the figure that stays comparable across pressure ratios, which is why it is used in cycle decks.
- Burner: efficiency `eta_b` (combustion completeness) and total-pressure ratio `pi_b`. Inlet and nozzle: `pi_d`, `pi_n`. Mechanical: `eta_m`.

## Typical values
Cycle textbooks tabulate component technology levels (polytropic compressor and turbine efficiency around 0.88 to 0.92 for modern machines, burner efficiency close to 0.99, burner pressure ratio about 0.94 to 0.97, nozzle about 0.98 to 0.99) (gated: unconfirmed, source is paywalled or blocked). Treat these as starting values and replace them with the engine maker's data when available.

## Procedure
1. Fix `pi_c` and design-point `Tt4`.
2. Choose `e_c`, `e_t`, `pi_b` and the others; calculate `tau_c`, `tau_t` from the relations above.
3. Compare cycles only at equal technology level and equal polytropic efficiency.
4. Reduce them to off-design maps later (see off-design-engine-matching).

## Gotchas
- Using isentropic efficiency for different pressure ratios in a parametric study biases the optimum.
- Variable specific heat matters at high temperature; the perfect-gas relations above are for preliminary work.
- Cooling-air extraction reduces turbine work and cannot be hidden in the efficiency.

## Verify
- [ ] At `e_c = 1` the compressor temperature ratio equals `pi_c^((g-1)/g)`.
- Worked check (computed, g = 1.4, e_c = 0.9): isentropic efficiency is 0.875 at pi_c = 5, 0.852 at 20 and 0.840 at 40; a turbine with pi_t = 1/10 and e_t = 0.9 has isentropic efficiency 0.927.
