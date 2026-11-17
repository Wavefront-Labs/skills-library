---
id: engineering-technology.chemical-engineering.separation-processes.psa-tsa-cycle-design
name: psa-tsa-cycle-design
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-adsorption-and-ion-exchange, psa-tsa-cycle-design, pressure-swing-adsorption, temperature-swing-adsorption, adsorption-cycle]
level: practitioner
status: draft
description: "Design pressure swing and temperature swing adsorption cycles: steps, cycle time, bed count and regeneration energy."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Psa tsa cycle design

**Goal:** Design pressure swing and temperature swing adsorption cycles: steps, cycle time, bed count and regeneration energy.

## Steps
1. PSA steps: adsorption at high pressure, depressurisation, purge or blowdown at low pressure, repressurisation; add pressure equalisation to improve recovery.
2. TSA: adsorb at low temperature, regenerate by hot purge gas, then cool; the cycle is longer (hours) than PSA (minutes).
3. Size beds for the adsorption step capacity using working capacity (difference between loading at adsorption and regeneration conditions).
4. Number of beds depends on the continuous feed and step times; check the purge to feed ratio and the product recovery by simulation.
5. Estimate regeneration energy, including the heat to desorb and the heat to warm the bed.

## Gotchas
- Cyclic steady-state simulation is needed; hand calculations are approximate.
- Contaminants (water) can poison the adsorbent.

## Verify
- [ ] Material balance closes over one cycle.
- [ ] Product purity and recovery meet the target at cyclic steady state.
