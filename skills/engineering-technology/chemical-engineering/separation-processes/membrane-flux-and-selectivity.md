---
id: engineering-technology.chemical-engineering.separation-processes.membrane-flux-and-selectivity
name: membrane-flux-and-selectivity
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-membranes, membrane-flux-and-selectivity, membrane-flux, selectivity, permeance, solution-diffusion]
level: practitioner
status: draft
description: "Calculate membrane flux and selectivity: solution-diffusion, permeance, ideal selectivity and the effects of concentration polarisation."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Membrane flux and selectivity

**Goal:** Calculate membrane flux and selectivity: solution-diffusion, permeance, ideal selectivity and the effects of concentration polarisation.

## Steps
1. Permeance (flux per driving force) is the property to quote for a given membrane thickness; permeability is permeance times thickness.
2. Ideal selectivity alpha = P_A / P_B (ratio of permeabilities); real selectivity is lower due to polarisation and non-ideal effects.
3. Gas membranes: flux J_i = (P_i / l)(p_feed x_i - p_perm y_i); the driving force is a partial pressure difference.
4. Liquid membranes (RO, UF): flux depends on the applied pressure minus the osmotic pressure and on the membrane resistance and the polarisation layer.
5. Check concentration polarisation: C_m / C_b = exp(J / k) for a fully rejecting membrane, where k is the mass transfer coefficient.

## Gotchas
- Permeances vary with temperature and pressure and are measured data; use vendor values.
- Reporting units differ (GPU, barrer, L/m2h).

## Verify
- [ ] Flux units are consistent.
- [ ] Polarisation modulus is below the design limit.
