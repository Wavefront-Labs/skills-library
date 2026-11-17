---
id: engineering-technology.chemical-engineering.piping-instrumentation.fittings-k-values-and-equivalent-length
name: fittings-k-values-and-equivalent-length
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-line-sizing, fittings-k-values-and-equivalent-length, fittings-losses, k-method, equivalent-length, crane-410, 2k-method, minor-losses, valve-loss-coefficient, resistance-coefficient]
level: practitioner
status: gated
description: "Account for fittings and valves with the K method and equivalent length, Crane and 2-K approaches, entrance and exit losses, and when to size for lowest K."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
  - "https://fluids.readthedocs.io/fluids.fittings.html (open-source Crane TP-410 K-value implementation)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fittings K values and equivalent length

**Goal:** total line resistance including bends, valves and entrance and exit losses.

## Methods
- **K method**: dP = K rho v^2/2 for each fitting; K is the resistance coefficient.
- **Equivalent length**: L_eq = K D/f (the pipe length giving the same loss); Crane TP-410 tabulates K as multiples of the fully turbulent friction factor f_T for the pipe size.
- **2-K (Hooper)**: K = K_1/Re + K_inf (1 + 1/ID_in) accounts for Reynolds number and size effects; useful for laminar or small sizes.

## Typical values (turbulent, indicative; confirm in the reference for your size)
- 90 degree standard elbow: K about 30 f_T (about 0.5 to 0.9 for typical sizes) (gated: unconfirmed, source is paywalled or blocked).
- Tee, flow through run: about 20 f_T; through branch: about 60 f_T (gated: unconfirmed, source is paywalled or blocked).
- Gate valve, fully open: about 8 f_T; globe valve: about 340 f_T; ball valve fully open: about 3 f_T (gate 8, globe 340 and ball 3 f_T match the Crane TP-410 implementation in the open-source fluids library); swing check: 50 f_T (straight-through) to 100 f_T (angled) in that implementation, confirm in Crane.
- Pipe entrance (sharp-edged): K = 0.5; exit into a tank: K = 1.0 (standard textbook values (gated: unconfirmed, source is paywalled or blocked)); sudden expansion and contraction use area ratios.

## Procedure
1. Count fittings from the isometric or a preliminary routing; add 10 to 20% for items not yet drawn.
2. Sum K (or L_eq) and add pipe friction: dP_total = (f L/D + sum K) rho v^2/2.
3. Add static head and equipment (exchanger, filter) pressure drops from data sheets.
4. Compare total to the available driving head or pump differential.

## Practice
At early stages use a lumped allowance (for example, equivalent length equal to 50 to 100% of the straight length) and replace it when the layout is available.

## Gotchas
- Control valves, orifices and strainers are not given by K tables; use vendor data.
- Valve K varies with opening; use the fully open value for the maximum flow check only.

## Verify
- [ ] Fittings list reconciles with the P&ID.
- [ ] Pressure-drop summary shows pipe, fittings, equipment and static contributions.
