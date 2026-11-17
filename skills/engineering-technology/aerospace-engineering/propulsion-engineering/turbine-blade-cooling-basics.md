---
id: engineering-technology.aerospace-engineering.propulsion-engineering.turbine-blade-cooling-basics
name: turbine-blade-cooling-basics
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [blade-cooling, turbine-cooling, film-cooling, impingement-cooling, thermal-barrier-coating, turbomachinery]
level: practitioner
status: draft
description: "Understand turbine blade cooling methods, cooling effectiveness and film blowing ratio, and account for the cycle penalty of cooling air."
sources:
  - "Mattingly, Elements of Propulsion"
  - "Han, Dutta and Ekkad, Gas Turbine Heat Transfer and Cooling Technology"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Turbine blade cooling basics

**Goal:** keep blade metal below its limit when the gas is hotter than the metal can survive.

## Methods
- **Internal convection**: serpentine passages with rib turbulators and pin fins.
- **Impingement**: jets onto the inside of the leading edge and walls.
- **Film cooling**: air ejected through holes forms a protective layer.
- **Thermal barrier coatings** (ceramic, e.g. yttria-stabilised zirconia) on the surface add a temperature drop across the coating, of the order of 100 K in good conditions.
- Material: single-crystal nickel superalloys carry higher metal temperatures.

## Metrics
- Overall cooling effectiveness `phi = (T_gas - T_metal) / (T_gas - T_coolant)`.
- Film effectiveness `eta = (T_gas - T_aw) / (T_gas - T_coolant)`, with adiabatic wall temperature `T_aw`.
- Blowing ratio `M = (rho_c U_c) / (rho_g U_g)`; low `M` holds the film, high `M` lifts the jet off the wall for cylindrical holes. Shaped holes tolerate larger `M`.

## Cycle impact
- Cooling air is bled from the compressor and bypasses the combustor, losing work; mixing it into the main stream costs total pressure.
- Raising turbine entry temperature with cooling can raise specific thrust but may lower efficiency if cooling flow is too large; a cycle model with cooling-flow fractions shows the trade.

## Gotchas
- Hot spots from combustor pattern factor, not the mean temperature, set the cooling design.
- Hole blockage by dust and oxidation reduces film cooling in service.
- Rotating blades see different internal heat transfer from stationary rigs.

## Verify
- [ ] Metal temperature predicted at the critical points stays below the life-limiting value with margin at hot-day take-off.
