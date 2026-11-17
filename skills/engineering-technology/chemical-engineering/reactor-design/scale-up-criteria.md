---
id: engineering-technology.chemical-engineering.reactor-design.scale-up-criteria
name: scale-up-criteria
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-scale-up-and-mixing, scale-up-criteria, scale-up, power-per-volume, tip-speed, geometric-similarity]
level: practitioner
status: draft
description: "Choose scale-up criteria for stirred vessels (constant power per volume, tip speed, Reynolds, mixing time) and see what each sacrifices."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scale up criteria

**Goal:** Choose scale-up criteria for stirred vessels (constant power per volume, tip speed, Reynolds, mixing time) and see what each sacrifices.

## Steps
1. Under geometric similarity, with scale factor S = D2/D1 in diameter: constant P/V gives N2 = N1 S^(-2/3); constant tip speed gives N2 = N1 / S; constant Re gives N2 = N1 S^(-2).
2. Constant P/V keeps turbulence roughly similar but mixing time rises with scale; constant tip speed lowers P/V and shear; constant Re is rarely practical.
3. Identify the sensitive phenomenon (mass transfer, shear, mixing time, heat transfer) and match that.
4. Calculate the other quantities at the new scale and check they stay acceptable.
5. Plan pilot work to test the controlling phenomenon.

## Gotchas
- No single criterion preserves everything.
- Heat transfer area per volume falls on scale-up, which often limits.

## Verify
- [ ] Exponents reproduce the stated scale factor.
- [ ] Non-matched quantities are within acceptable limits.
