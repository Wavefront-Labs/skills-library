---
id: engineering-technology.chemical-engineering.separation-processes.batch-distillation-design
name: batch-distillation-design
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-special-distillation, batch-distillation-design, batch-distillation, rayleigh-equation, batch-reflux]
level: practitioner
status: draft
description: "Design a batch distillation: Rayleigh equation, operating modes (constant reflux or constant distillate composition) and time and energy."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Batch distillation design

**Goal:** Design a batch distillation: Rayleigh equation, operating modes (constant reflux or constant distillate composition) and time and energy.

## Steps
1. Rayleigh equation for simple distillation: ln(W0/W) = integral of dx / (y - x) from x_W to x_W0.
2. For a column, choose constant reflux (distillate composition drifts) or variable reflux (constant distillate composition); use McCabe-Thiele per step or a rigorous batch model.
3. Specify the cuts: first cut (light impurities), main cut and slop recycle for the heel.
4. Compute batch time from the vapour boilup rate, which is limited by the reboiler duty and column flooding.
5. Compare with continuous operation for the throughput and flexibility needs.

## Gotchas
- Holdup in the column and condenser affects the cut purity.
- Vessel heat and thermal stability for long batch times.

## Verify
- [ ] Overall material balance closes.
- [ ] Product specs are met in each cut.
