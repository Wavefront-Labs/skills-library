---
id: engineering-technology.chemical-engineering.reactor-design.reactor-comparison-levenspiel-plots
name: reactor-comparison-levenspiel-plots
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-ideal-reactor-design, reactor-comparison-levenspiel-plots, levenspiel-plot, reactor-comparison, pfr-vs-cstr, reactor-volume, autocatalytic, reactor-sequencing, graphical-design]
level: practitioner
status: draft
description: "Compare PFR, CSTR and series arrangements graphically with Levenspiel plots of F_A0/(-r_A) versus X, including autocatalytic and equilibrium-limited cases."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Comparing reactors with Levenspiel plots

**Goal:** choose and size reactor combinations quickly and see why.

## The plot
Plot F_A0/(-r_A) (or 1/(-r_A) for constant density) versus conversion X.
- PFR volume = area under the curve from 0 to X.
- CSTR volume = rectangle: height at exit X times X.
- CSTRs in series = sum of rectangles stepped under the curve.

## Rules read from the plot
- For rates that decrease monotonically with conversion (typical positive order), PFR needs less volume than a single CSTR.
- For rates that rise first then fall (autocatalytic, or exothermic adiabatic runaway), a CSTR first then a PFR is better; a recycle PFR approximates it.
- Equilibrium-limited: the curve goes to infinity at X_eq; do not design near it.

## Procedure
1. Compute -r_A over conversion using the rate law and the energy balance (use adiabatic or controlled T).
2. Plot; calculate areas numerically.
3. Compare options: single PFR, single CSTR, CSTR plus PFR, and series CSTRs.
4. Choose by volume and by practical issues: heat removal, catalyst handling, mixing.

## Gotchas
- Different temperatures in different units shift the curve; plot each with its own T.
- Do not compare reactors at different conversions.

## Verify
- [ ] Numerically computed areas match closed forms for first-order tests.
- [ ] The choice explained in terms of the shape of the curve.
