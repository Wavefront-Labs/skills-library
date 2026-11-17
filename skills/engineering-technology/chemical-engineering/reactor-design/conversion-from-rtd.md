---
id: engineering-technology.chemical-engineering.reactor-design.conversion-from-rtd
name: conversion-from-rtd
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-nonideal-flow, conversion-from-rtd, conversion-from-rtd, segregation-model, non-ideal-reactor]
level: practitioner
status: verified
description: "Predict conversion from a measured RTD using the segregation model and compare with ideal CSTR and PFR limits."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conversion from rtd

**Goal:** Predict conversion from a measured RTD using the segregation model and compare with ideal CSTR and PFR limits.

## Steps
1. Measure and normalise E(t) as in the RTD skill.
2. Compute the batch conversion curve X(t) from the rate law at the reactor temperature.
3. Segregation model: X = sum of X(t_i) E(t_i) Delta t; integrate numerically.
4. Compare with the PFR (X at tau) and CSTR (X from the steady-state balance) values. The PFR value is an upper bound for positive-order kinetics (Jensen: X(t) is concave in t); the ideal CSTR is not a guaranteed lower bound, because bypassing plus dead volume can do worse (first order, k tau = 2: PFR 0.865, CSTR 0.667, but half the flow bypassing with the other half at 2 tau gives 0.491; computed).
5. Report the conversion with an uncertainty from the RTD and kinetic data.

## Gotchas
- Use consistent time units.
- Assumes isothermal operation and constant density.

## Verify
- [ ] Result does not exceed the ideal PFR value for positive-order kinetics, and is compared with the ideal CSTR value.
- [ ] Numerical integration is converged.
