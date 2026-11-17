---
id: engineering-technology.chemical-engineering.process-safety.two-phase-relief-sizing
name: two-phase-relief-sizing
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-relief-sizing, two-phase-relief-sizing, two-phase-relief, omega-method, diers, flashing-flow, leung, api-520-annex-c, runaway-relief, vent-sizing, subcooled-liquid]
level: advanced
status: verified
description: "Size relief devices for two-phase and flashing flow with the omega method of API 520 Annex C (DIERS), noting when to engage specialists and use calorimetry data."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Two-phase relief sizing

**Goal:** a relief area for flashing or two-phase venting, using a recognised method. Two-phase relief (especially for runaway reactions) is a specialist task; engage engineers experienced with DIERS methods and use properly obtained calorimetry data.

## Why single-phase formulas fail
Boiling liquids and foamy systems swell and discharge two-phase mixtures; the mass flux is lower than for vapour alone, so vapour-only sizing under-sizes the device. The DIERS (Design Institute for Emergency Relief Systems) programme developed the methods.

## Omega method (Leung; as presented in API 520)
1. The compressibility parameter omega from two-point density data (isenthalpic flash): omega = 9 (rho_0/rho_9 - 1) (gated: unconfirmed, source is paywalled or blocked), where rho_0 is the fluid density at the relief pressure P_0 and rho_9 the density at 90% of P_0 after an isenthalpic flash.
2. Compare the back-pressure ratio with the critical pressure ratio computed from omega to determine whether the flow is choked; the mass flux G follows from closed-form equations (omega method) or from numerical integration.
3. Required area A = W/(K_d K_b K_c G) with W the total mass relief rate.
4. Subcooled and saturated liquid inlet cases use modified equations (subcooling parameter); follow API 520.

## Inputs
- **Relief rate W** from the energy balance: for vented runaways, heat-release rate at set pressure from adiabatic calorimetry (for example vent sizing package or ARC type tests) and the flow regime (churn-turbulent, bubbly, foamy).
- **Physical properties**: density, enthalpy of vaporisation, heat capacity at relieving conditions.
- **Disengagement**: vessel two-phase hold-up and the discharge fraction of liquid.

## Practice
1. Use the simplified methods (API 520 Annex C, DIERS short-cut equations) as screening; verify with a specialised software tool.
2. Add the discharge piping pressure drop with a two-phase model; check against the set pressure and back pressure assumption.
3. Plan containment: catch tank or separator for the two-phase discharge and flare or scrubber; fast vent disposal cannot just open to atmosphere.

## Gotchas
- Using a foamy-versus-nonfoamy assumption wrongly changes the area by a large factor.
- Reaction relief needs testing, not literature guesses.

## Verify
- [ ] Method, data and the key assumptions are reviewed by a qualified relief engineer.
- [ ] Discharge handling system designed for the relief load.
