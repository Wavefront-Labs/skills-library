---
id: engineering-technology.chemical-engineering.reactor-design.catalyst-deactivation-and-regeneration
name: catalyst-deactivation-and-regeneration
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-catalytic-reactors, catalyst-deactivation-and-regeneration, catalyst-deactivation, coking, sintering, poisoning, regeneration, activity-decay, end-of-run, catalyst-life, swing-reactor]
level: advanced
status: draft
description: "Model catalyst deactivation (poisoning, coking, sintering), plan temperature ramps and regeneration cycles, and size for end-of-run activity."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Catalyst deactivation and regeneration

**Goal:** a reactor design that meets production over the whole catalyst cycle, with a regeneration or replacement plan.

## Mechanisms
- **Poisoning**: strong chemisorption of impurities (sulphur, arsenic, chloride) blocks sites; often irreversible; guard beds protect.
- **Coking (fouling)**: carbon deposits block pores and sites; often reversible by controlled burn-off.
- **Sintering**: loss of active surface at high temperature; irreversible.
- **Others**: leaching, phase change, attrition, mechanical crushing.

## Kinetic description
Activity a(t) = rate / fresh rate. Common form: da/dt = -k_d a^m (first-order decay a = exp(-k_d t)). k_d follows Arrhenius in T. Decay can depend on concentration of poison or coke precursor.

## Design approaches
1. **Temperature compensation**: raise T over the cycle to hold conversion; the end of run is set by the maximum allowable temperature or selectivity loss.
2. **Oversized bed** with a margin so the end-of-run activity still meets the target.
3. **Swing reactors** (one in regeneration while another operates), **moving bed** or **fluidised bed with a regenerator** (for fast deactivation as in catalytic cracking).
4. **Guard beds** for poisons.

## Regeneration
Controlled coke burn with diluted oxygen, staged temperature (to avoid hot spots and sintering), monitor outlet CO2/O2; follow the supplier procedure. Plan start-up sequences, gas purging and safety for flammable and toxic atmospheres.

## Gotchas
- Activity profiles along the bed: guard zone deactivates first.
- Regeneration exotherm can exceed the metal or support limit; limit oxygen.

## Verify
- [ ] End-of-run conversion meets spec with defined maximum temperature.
- [ ] Regeneration procedure has a temperature limit and a monitored endpoint.
