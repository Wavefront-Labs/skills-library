---
id: engineering-technology.chemical-engineering.reactor-design.jacket-and-coil-heat-transfer-scale-up
name: jacket-and-coil-heat-transfer-scale-up
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-scale-up-and-mixing, jacket-and-coil-heat-transfer-scale-up, jacket-heat-transfer, heat-removal, scale-up]
level: practitioner
status: draft
description: "Check jacket and coil heat removal on scale-up where area per volume falls, and decide on internals or external exchangers."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jacket and coil heat transfer scale up

**Goal:** Check jacket and coil heat removal on scale-up where area per volume falls, and decide on internals or external exchangers.

## Steps
1. Heat transfer area per volume of a vessel scales roughly as 1/L; a tenfold volume increase cuts the jacket area per volume by about a factor of 2 (area scales as V^(2/3)).
2. Calculate required heat removal Q from the reaction enthalpy and rate at the scaled batch time.
3. Calculate available Q = U A delta T with the inner film coefficient from the agitator correlation and the jacket side; consider fouling.
4. If short, add coils or baffles, use an external pumped-loop exchanger, lengthen the dose time in semibatch, or lower the coolant temperature.
5. Check the worst case (cooling failure) and the adiabatic temperature rise for safety.

## Gotchas
- A reaction that is fine at lab scale can be heat-limited at plant scale.
- Safety studies should confirm the cooling margin.

## Verify
- [ ] Heat removal capacity exceeds the peak heat generation with margin.
- [ ] Cooling-failure scenario was reviewed.
