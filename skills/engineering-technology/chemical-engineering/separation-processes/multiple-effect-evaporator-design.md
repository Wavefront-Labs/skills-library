---
id: engineering-technology.chemical-engineering.separation-processes.multiple-effect-evaporator-design
name: multiple-effect-evaporator-design
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-crystallisation-drying-evaporation, multiple-effect-evaporator-design, evaporator, multiple-effect-evaporation, steam-economy, boiling-point-rise, forward-feed, backward-feed, heat-transfer-area, thermal-vapor-recompression]
level: advanced
status: draft
description: "Design multiple-effect evaporators: effects count, steam economy, boiling point rise, feed arrangement (forward, backward, mixed) and area per effect by iterative balances."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations, Mullin Crystallization"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multiple-effect evaporator design

**Goal:** the number of effects, steam use and heat-transfer area for a concentration duty.

## Balances
1. Overall solute balance: F x_F = P x_P; evaporation total W = F - P.
2. Each effect: latent heat of vapour condensing in effect i is used to evaporate water in effect i+1: roughly equal evaporation per effect for similar latent heats.
3. **Steam economy** (kg evaporated per kg steam): about 0.8 to 0.9 times the number of effects as a rule of thumb for well-designed systems with feed near boiling.
4. **Boiling point rise (BPR)** in concentrated solutions reduces the effective temperature difference in each effect (Duhring plots or correlations); include hydrostatic head effects in tall tubes.

## Procedure
1. Choose the number of effects balancing steam cost against capital (area increases roughly with effect count since total temperature difference is split).
2. Assume equal evaporation per effect; estimate the temperature distribution by dividing the available total temperature difference (steam to condenser minus total BPR and losses).
3. Compute heat duty per effect with enthalpy balances (feed sensible heat, concentration change).
4. Compute area per effect A_i = Q_i/(U_i DT_i); adjust DT_i to equalise areas (common for fabrication).
5. Iterate until evaporation per effect and areas converge (use a spreadsheet or simulator).
6. Feed arrangement: **forward** (simple, vapour flows with liquid), **backward** (viscous product at high temperature, needs pumps), **mixed** or parallel.
7. Consider thermal or mechanical vapour recompression as an alternative or addition.

## Gotchas
- U decreases with concentration and viscosity; use the lowest effect values.
- Fouling and scaling set cleaning frequency and cleaning spare capacity.
- Entrainment separation and product degradation at high temperature.

## Verify
- [ ] Overall energy balance and solute balance close.
- [ ] Areas per effect within 10% of one another unless justified.
