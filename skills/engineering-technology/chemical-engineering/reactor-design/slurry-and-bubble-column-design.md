---
id: engineering-technology.chemical-engineering.reactor-design.slurry-and-bubble-column-design
name: slurry-and-bubble-column-design
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-multiphase-reactors, slurry-and-bubble-column-design, bubble-column, slurry-reactor, gas-holdup, kla]
level: practitioner
status: draft
description: "Size slurry and bubble column reactors from gas holdup, kLa, solids suspension and heat removal."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slurry and bubble column design

**Goal:** Size slurry and bubble column reactors from gas holdup, kLa, solids suspension and heat removal.

## Steps
1. Gas holdup rises with superficial gas velocity; use correlations valid for the liquid (coalescing or non-coalescing) and column diameter.
2. Estimate kLa from a correlation and check mass transfer against the kinetic rate to see the controlling step.
3. For slurries, ensure solids suspension (catalyst settling versus gas-induced mixing) and check the effect of solids loading on viscosity and holdup.
4. Size the column for liquid volume plus gas holdup; add internals (cooling tubes) for heat removal.
5. Scale up using the heterogeneous flow regime; large columns have strong liquid back-mixing.

## Gotchas
- Small lab columns can behave differently from large ones (wall effects).
- Foaming limits operating velocity.

## Verify
- [ ] Required kLa is below the available value with margin.
- [ ] Solids are fully suspended at the design gas rate.
