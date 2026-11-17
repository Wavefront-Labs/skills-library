---
id: engineering-technology.chemical-engineering.process-safety.source-term-discharge-modelling
name: source-term-discharge-modelling
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-consequence-modelling, source-term-discharge-modelling, source-term, discharge-rate, orifice-flow, choked-flow, flashing-release, pool-evaporation, loss-of-containment, consequence-modelling]
level: advanced
status: gated
description: "Model release source terms for process hazard studies: liquid and gas discharge rates, flashing flow, pool evaporation, with orifice equations and assumptions to document."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Source term and discharge modelling

**Goal:** release rate and phase for the consequence models used in hazard studies, facility siting and emergency planning (accident prevention, not hazard creation). Consequence modelling should be done by trained practitioners with validated software and reviewed assumptions.

## Liquid discharge through a hole
Mass flow = C_d A rho sqrt( 2 (P - P_a)/rho + 2 g h ), with C_d about 0.6 to 0.65 for sharp-edged orifices (gated: unconfirmed, source is paywalled or blocked), A the hole area, P the upstream absolute pressure, h the liquid head above the hole. For a decreasing inventory integrate over time.

## Gas discharge
- Choked if P/P_a exceeds ((k + 1)/2)^(k/(k - 1)) (1.893 for k = 1.4, computed).
- Choked mass flux: G = C_d P sqrt( (k M/(R T)) (2/(k + 1))^((k + 1)/(k - 1)) ).
- Subsonic: isentropic expansion equations.
- Pipe rupture: add friction in the line (Fanno flow) and transient depressurisation.

## Flashing liquids
Liquids stored above their normal boiling point flash as they leave; a first estimate treats the flow as two-phase (omega method or HEM, see the `two-phase-relief-sizing` skill) with flash fraction = c_p (T - T_b)/lambda; aerosols and rainout reduce the vapour cloud.

## Pool formation and evaporation
Pool area from the bund or spreading model; evaporation rate from heat (ground, solar, convection) and mass transfer (wind speed); volatile liquids evaporate quickly, cryogenics boil by ground conduction.

## Practice
1. Define hole sizes (for example small leak, medium, large, and full-bore rupture) with frequencies from generic data (as in CCPS or HSE data sets, per the organisation's choice).
2. Compute rates and durations for each, considering isolation (detection and shutdown time).
3. State the release conditions (temperature, pressure, direction, height) for the dispersion model.
4. Document the assumptions: inventory isolated, release phase, rainout fraction.

## Gotchas
- The hole size choice dominates the results more than the model.
- Release direction (horizontal jet, downward impinging, vertical) changes dispersion drastically.

## Verify
- [ ] A hand calculation of one case matches the software result.
- [ ] Assumptions listed for the review team.
