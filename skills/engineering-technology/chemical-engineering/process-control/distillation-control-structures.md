---
id: engineering-technology.chemical-engineering.process-control.distillation-control-structures
name: distillation-control-structures
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-unit-operation-control, distillation-control-structures, distillation-control, temperature-control, lv-configuration]
level: practitioner
status: draft
description: "Choose a distillation control structure: level, pressure, temperature and composition loops, and the LV or DV configuration."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio, Luyben, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.isa.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Distillation control structures

**Goal:** Choose a distillation control structure: level, pressure, temperature and composition loops, and the LV or DV configuration.

## Steps
1. Set the pressure control first (condenser duty or vent), then the levels (reflux drum and bottoms) so that the material balance is closed.
2. Use the LV configuration (reflux and boilup as the composition handles) in many columns; use D/V or ratio schemes when the reflux ratio is large, with level control by the distillate.
3. Control a tray temperature as an inferential for composition, located where the temperature profile is steep; use a cascade to the analyzer if one exists.
4. Add feedforward on feed flow and the feed composition if the disturbances are large.
5. Check interactions with the relative gain array and use decoupling if necessary.

## Gotchas
- The temperature and composition relation varies with pressure; compensate or hold the pressure.
- Dual-composition control is difficult for high purity columns.

## Verify
- [ ] Material balance is controlled by levels.
- [ ] Temperature sensor location is justified.
