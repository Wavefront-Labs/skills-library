---
id: engineering-technology.chemical-engineering.reactor-design.bioreactor-design-fundamentals
name: bioreactor-design-fundamentals
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-special-reactors, bioreactor-design-fundamentals, bioreactor, monod-kinetics, chemostat, oxygen-transfer]
level: practitioner
status: draft
description: "Cover bioreactor fundamentals: Monod growth kinetics, oxygen transfer, chemostat balance and agitation and aeration sizing."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bioreactor design fundamentals

**Goal:** Cover bioreactor fundamentals: Monod growth kinetics, oxygen transfer, chemostat balance and agitation and aeration sizing.

## Steps
1. Monod growth: mu = mu_max S / (Ks + S); the chemostat steady state has mu = D, the dilution rate.
2. Washout occurs when D exceeds mu_max S0 / (Ks + S0) for the feed substrate S0.
3. Oxygen balance: OUR = qO2 X must be less than kLa (C* - C) with the dissolved oxygen above the critical value.
4. Size agitation and aeration for the kLa needed; consider heat removal, since metabolic heat can be large in dense cultures.
5. For regulated products (pharma), design to the applicable good manufacturing practice rules; confirm current requirements.

## Gotchas
- Shear sensitive cells limit agitation.
- Scale-up often keeps kLa or P/V constant, each with trade-offs.

## Verify
- [ ] Steady-state mass balance of substrate and biomass closes.
- [ ] Oxygen supply exceeds the demand with margin.
