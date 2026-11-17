---
id: engineering-technology.chemical-engineering.separation-processes.cyclone-design
name: cyclone-design
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-solid-liquid-and-gas-solid, cyclone-design, cyclone, gas-solid-separation, cut-diameter, lapple]
level: practitioner
status: gated
description: "Size a gas cyclone: inlet velocity, cut diameter, pressure drop and collection efficiency, using the Lapple or Barth models."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cyclone design

**Goal:** Size a gas cyclone: inlet velocity, cut diameter, pressure drop and collection efficiency, using the Lapple or Barth models.

## Steps
1. Choose the inlet velocity (commonly around 15 to 25 m/s for a conventional cyclone (gated: unconfirmed, source is paywalled or blocked)) and compute the inlet area from the gas flow.
2. Lapple cut diameter d50 = sqrt(9 mu W / (2 pi N_e v_i (rho_p - rho_g))), with W the inlet width and N_e the number of effective turns (about 5 for standard designs (gated: unconfirmed, source is paywalled or blocked)).
3. Efficiency versus particle size follows the Lapple curve (eta = 1/(1 + (d50/d)^2)) as a first estimate (Lapple's form (gated: unconfirmed, source is paywalled or blocked)).
4. Pressure drop is estimated as a number of inlet velocity heads (for the standard Lapple design about 8 = 16 a b / De^2 with a = D/2, b = D/4, De = D/2 (computed from recalled standard dimensions (gated: unconfirmed, source is paywalled or blocked))).
5. Use multiple small cyclones in parallel to get a smaller cut size, and check erosion and re-entrainment.

## Gotchas
- Efficiency curves from vendors are more reliable than models.
- Mass loading changes the efficiency (higher loading raises it).

## Verify
- [ ] Cut size meets the requirement.
- [ ] Pressure drop is acceptable for the blower.
