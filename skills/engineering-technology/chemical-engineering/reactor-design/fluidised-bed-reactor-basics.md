---
id: engineering-technology.chemical-engineering.reactor-design.fluidised-bed-reactor-basics
name: fluidised-bed-reactor-basics
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-multiphase-reactors, fluidised-bed-reactor-basics, fluidised-bed, minimum-fluidisation, umf]
level: practitioner
status: draft
description: "Estimate minimum fluidisation velocity, bed expansion and regime for a fluidised bed reactor, and check the main design issues."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fluidised bed reactor basics

**Goal:** Estimate minimum fluidisation velocity, bed expansion and regime for a fluidised bed reactor, and check the main design issues.

## Steps
1. Minimum fluidisation: pressure drop equals bed weight per area, delta P = (1 - eps_mf)(rho_p - rho_f) g L_mf; solve for u_mf from the Ergun equation.
2. For small particles a Wen-Yu type correlation is common: Re_mf = sqrt(33.7^2 + 0.0408 Ar) - 33.7, with Ar the Archimedes number.
3. Choose operating velocity as a multiple of u_mf and below the terminal velocity of the fines; identify the regime (bubbling, turbulent, fast fluidisation).
4. Design the distributor (pressure drop as a fraction of the bed drop) and cyclones for fines.
5. Check attrition, heat transfer and the two-phase bubble model for conversion.

## Gotchas
- Correlations for u_mf can be off by tens of percent; test with the actual solids.
- Group A, B, C, D classification (Geldart) matters.

## Verify
- [ ] Bed pressure drop equals the bed weight.
- [ ] Operating velocity is between u_mf and the entrainment limit.
