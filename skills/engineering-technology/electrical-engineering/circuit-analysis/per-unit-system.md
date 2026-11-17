---
id: engineering-technology.electrical-engineering.circuit-analysis.per-unit-system
name: per-unit-system
category: engineering-technology
field: electrical-engineering
product: circuit-analysis
tags: [base-change, base-conversion, circuit-analysis, electrical-engineering, per-unit, per-unit-system, transformer-per-unit-referral, zbase]
level: intro
status: draft
description: "Set up and convert per-unit bases across transformers and base changes so network data from different ratings can be combined."
sources:
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Per-unit system

1. Choose one three-phase MVA base `Sb` for the whole study (100 MVA is common) and a line-to-line voltage base `Vb` per voltage level.
2. Derive: `Zb = Vb^2/Sb` (kV, MVA gives ohm), `Ib = Sb/(sqrt(3) Vb)`.
3. Across a transformer set the voltage bases in the ratio of the rated voltages, then per-unit impedance is the same referred to either side.
4. Convert nameplate data: `Z_new = Z_old (Sb_new/Sb_old)(Vb_old/Vb_new)^2`.
5. Example: 10 MVA 13.8/69 kV transformer, Z = 8 %. On a 100 MVA base: `0.08 x 100/10 = 0.80` pu.
6. Source of short-circuit MVA: `Z1 = Sb / Ssc` pu.

**Failure modes:** using phase-to-neutral bases with three-phase MVA; ignoring a delta-wye phase shift; not updating the base for cable data given in ohm.

**Verify:** check that a transformer's impedance referred through its ratio matches in ohm on both sides.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
