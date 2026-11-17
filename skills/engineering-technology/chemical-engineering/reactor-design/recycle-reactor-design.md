---
id: engineering-technology.chemical-engineering.reactor-design.recycle-reactor-design
name: recycle-reactor-design
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-ideal-reactor-design, recycle-reactor-design, recycle-reactor, recycle-ratio, autocatalytic-reaction, loop-reactor, reactor-recycle, purge, differential-reactor, plug-flow-with-recycle]
level: practitioner
status: draft
description: "Design a PFR with recycle: recycle ratio, effective conversion, autocatalytic optimum recycle, and gas loop considerations such as purge and compressor duty."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recycle reactor design

**Goal:** the size and recycle ratio for a recycle PFR or loop reactor.

## Design equation
With recycle ratio R = recycle flow / product flow, the volume of a PFR with recycle:
V / F_A0 = (R + 1) integral from R X_Af/(R + 1) to X_Af of dX/(-r_A).
R = 0 gives an ordinary PFR; R -> infinity approaches a CSTR (the loop is well mixed).

## When it is useful
- Autocatalytic reactions: the product accelerates the rate, so some recycle (optimum R) minimises volume.
- To dilute exothermic feed or limit temperature rise.
- Gas loops where per-pass conversion is limited by equilibrium (see `engineering-technology.chemical-engineering.process-design.reactor-separator-recycle-trade-off`).
- Laboratory differential reactors: high recycle gives near-uniform composition (gradientless).

## Procedure
1. Compute rate versus conversion; choose R values (0, 1, 3, 10).
2. Integrate for each R; find the minimum V for autocatalytic systems.
3. Add recycle pump or compressor cost and energy.
4. For gas loops: compute purge and make-up with inert balances.

## Gotchas
- Recycle pumps and compressors add cost that can exceed the saving in reactor volume.
- Residence-time distribution broadens with R; if selectivity relies on plug flow, high R hurts.

## Verify
- [ ] Known limits reproduced: R = 0 gives PFR, large R gives CSTR volume.
- [ ] Optimum R (if any) is shallow; operation robust to flow changes.
