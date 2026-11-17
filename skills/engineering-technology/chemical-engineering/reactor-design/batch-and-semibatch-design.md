---
id: engineering-technology.chemical-engineering.reactor-design.batch-and-semibatch-design
name: batch-and-semibatch-design
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-ideal-reactor-design, batch-and-semibatch-design, batch-reactor, semibatch-reactor, fed-batch, cycle-time, batch-time, feed-rate, accumulation, heat-removal, pharmaceutical-fine-chemicals]
level: practitioner
status: draft
description: "Design batch and semibatch reactors: batch time from the rate law, cycle time including charge and discharge, and feed-rate limits for semibatch heat and accumulation control."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Batch and semibatch reactor design

**Goal:** batch size, reaction time and feed profile that meet production and heat-removal limits.

## Batch
t = N_A0 integral dX/(-r_A V). For constant volume: t = C_A0 integral from 0 to X dX/(-r_A). Cycle time = reaction time + charging + heating + cooling + discharge + cleaning. Annual output = batch size x number of batches (operating hours per year / cycle time).

## Semibatch (fed-batch)
Mole balance: dN_A/dt = F_A,in + r_A V. Feeding one reactant slowly controls concentration and heat release. Design the feed profile so that heat release rate never exceeds the cooling capacity: Q_max = U A (T - T_jacket).

## Accumulation check
If a fed reactant is not consumed as fast as it is added (cold start, wrong temperature, catalyst absent, mixing failure), unreacted reactant accumulates; a later temperature rise can release the stored heat quickly. Calculate the accumulated fraction and the adiabatic temperature rise from accumulated reactant; keep it within the safety limit set by the process hazard review (see `engineering-technology.chemical-engineering.process-safety.reactive-hazard-screening`).

## Procedure
1. Fit kinetics to isothermal data.
2. Compute batch time versus conversion; choose a target conversion that balances time and yield.
3. Compute heat release profile and compare with jacket capability (see jacket-scale-up skill).
4. Optimise cycle time (heat-up and cool-down are often the largest part).

## Gotchas
- A reaction that is fast in the laboratory may be heat-removal-limited at scale because surface-to-volume ratio falls.
- Stop-feed and cooling failure scenarios must be considered during design.

## Verify
- [ ] Heat release versus time never exceeds cooling capacity at design margin.
- [ ] Accumulation limit and action on loss of cooling documented.
