---
id: engineering-technology.chemical-engineering.reactor-design.segregation-and-micromixing
name: segregation-and-micromixing
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-nonideal-flow, segregation-and-micromixing, segregation, micromixing, maximum-mixedness]
level: practitioner
status: draft
description: "Bound reactor conversion between complete segregation and maximum mixedness, and judge when micromixing matters."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Segregation and micromixing

**Goal:** Bound reactor conversion between complete segregation and maximum mixedness, and judge when micromixing matters.

## Steps
1. Segregation model: each fluid element is a batch reactor with residence time from E(t); conversion = integral of X_batch(t) E(t) dt.
2. Maximum mixedness model: elements mix at the earliest possible moment; solve the differential equation in life expectancy.
3. For first-order reactions both give the same conversion; the difference appears for non-first-order kinetics.
4. For order greater than 1 segregation gives higher conversion; for order less than 1 maximum mixedness gives higher conversion.
5. Calculate both; if the answers are close, micromixing is unimportant.

## Gotchas
- Real reactors lie between the bounds.
- Fast reactions with poor mixing need computational fluid dynamics or experiments.

## Verify
- [ ] The bounds bracket plant data.
- [ ] First-order case gives equal results.
