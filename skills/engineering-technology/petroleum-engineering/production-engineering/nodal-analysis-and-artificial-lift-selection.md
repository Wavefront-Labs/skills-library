---
id: engineering-technology.petroleum-engineering.production-engineering.nodal-analysis-and-artificial-lift-selection
name: nodal-analysis-and-artificial-lift-selection
category: engineering-technology
field: petroleum-engineering
product: production-engineering
tags: [nodal-analysis, systems-analysis, ipr, vlp, tpr, vogel, productivity-index, backpressure-equation, beggs-brill, hagedorn-brown, gray-correlation, multiphase-flow, operating-point, liquid-loading, turner-critical-velocity, coleman, artificial-lift, esp, rod-pump, gas-lift, pcp, plunger-lift, prosper, pipesim, tubing-sizing]
level: practitioner
status: gated
description: "Build IPR (PI/Vogel/backpressure) and VLP (Hagedorn-Brown, Beggs-Brill, Gray) curves, find the operating point, check Turner liquid loading and choose ESP, rod, gas lift or PCP."
sources:
  - "Vogel, Inflow Performance Relationships for Solution-Gas Drive Wells (JPT, 1968)"
  - "Hagedorn & Brown (JPT, 1965); Beggs & Brill (JPT, 1973) multiphase-flow correlations"
  - "Turner, Hubbard & Dukler, Analysis and Prediction of Minimum Flow Rate for Continuous Removal of Liquids from Gas Wells (JPT, 1969)"
  - "Economides, Hill, Ehlig-Economides & Zhu, Petroleum Production Systems"
  - "Brown, The Technology of Artificial Lift Methods"
  - "PROSPER User Manual (Petroleum Experts); PIPESIM User Guide (SLB)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nodal analysis and artificial-lift selection — find the operating point, then decide how to lift

**Goal:** predict a well's rate from inflow and outflow curves, diagnose why it under-performs or loads up, and pick an artificial-lift method that fits the rate, depth, fluids and facilities.

## 1. Inflow performance (IPR)
Checked: the composite Vogel curve is continuous at Pb (J = 2, Pr = 3000, Pb = 2000: qb = 2000 stb/d on both sides) and gives qmax = qb + J·Pb/1.8 = 4222 stb/d (computed).

- **Undersaturated oil (Pwf > Pb):** straight line, q = J·(Pr − Pwf); J (PI) in stb/d/psi from a test or Darcy: J = kh / [141.2·Bo·μo·(ln(re/rw) − 0.75 + s)] (field units, pseudo-steady state).
- **Saturated oil:** Vogel, q/qmax = 1 − 0.2·(Pwf/Pr) − 0.8·(Pwf/Pr)². For Pr > Pb use the composite: linear down to Pb (qb = J·(Pr − Pb)), then below Pb q = qb + (J·Pb/1.8)·[1 − 0.2·(Pwf/Pb) − 0.8·(Pwf/Pb)²].
- **Gas:** backpressure q = C·(Pr² − Pwf²)^n, n 0.5 (turbulent) to 1 (laminar), from a multi-rate test; or the Jones/Forchheimer form with a non-Darcy term. Use pseudo-pressure for high pressures.
- **Fractured wells:** use an effective skin or wellbore radius from fracture half-length and FCD (see engineering-technology.petroleum-engineering.well-completion-design.hydraulic-fracture-design).

## 2. Outflow (VLP / TPR)

Total ΔP = hydrostatic (dominant in most oil wells) + friction + acceleration. Pick a correlation and **calibrate it against a flowing-gradient survey or a well test**:

| Correlation | Best for |
|---|---|
| Hagedorn–Brown (modified) | vertical oil wells, moderate GOR |
| Beggs–Brill | deviated/horizontal and pipelines; tends to over-predict ΔP in vertical wells |
| Gray | gas/condensate wells |
| Duns–Ros, Petroleum Experts 2–5 | general; vendor-tuned |
| Mechanistic (Ansari, Hasan–Kabir, OLGAS) | when flow-pattern physics matters |

In PROSPER or PIPESIM, run a correlation comparison against measured BHP, choose the one with the least error, then tune holdup/friction multipliers only within modest bounds (~±10–20% (gated: unconfirmed, source is paywalled or blocked)).

## 3. Operating point and sensitivities

The intersection of IPR and VLP at the solution node (usually mid-perforations) gives the rate and Pwf. The VLP must intersect on its **right-hand (stable) side** of the minimum; an intersection left of the VLP minimum is unstable (heading/loading). Run sensitivities: tubing ID (e.g. 2⅜ vs 2⅞ vs 3½ in.), wellhead pressure, water cut, GOR, skin, reservoir pressure depletion. Larger tubing cuts friction but lowers velocity and loads earlier.

## 4. Liquid loading (gas wells)

Turner critical velocity for droplets (field units): v_t = 1.593·σ^0.25·(ρL − ρg)^0.25 / ρg^0.5 ft/s (σ dyne/cm, ρ lbm/ft³); Turner applied a +20% adjustment (coefficient ~1.912; 1.593 x 1.2 = 1.912 computed). Coleman found the unadjusted value fits low-pressure (< ~1000 psi wellhead) wells (gated: unconfirmed, source is paywalled or blocked). Critical rate: q_c (MMscf/d) = 3.067·p·A·v_t / (T·z) (constant recomputed as 86400 x 520 / 14.65 / 1e6 = 3.067, i.e. a 14.65 psia, 520 °R base; 3.056 at 14.7 psia), with p psia, A ft² tubing flow area, T °R, evaluated at wellhead (and at bottom for deep wells). Symptoms: erratic rate, rising casing–tubing differential, slugging. Remedies: smaller tubing / velocity string, plunger lift, foamers, compression to lower wellhead pressure, gas lift.

## 5. Artificial-lift selection (screening ranges, indicative)
All ranges in this table are rules of thumb (gated: unconfirmed, source is paywalled or blocked); the vendor and Brown/Economides texts give the working envelopes.

| Method | Rate | Depth | Strengths | Limits |
|---|---|---|---|---|
| Rod pump (beam) | < ~1,000–2,000 bpd | to ~10,000 ft (rate falls with depth) | simple, low Pwf, cheap | deviation, sand, gas interference, offshore |
| ESP | ~200 to > 30,000 bpd | deep OK | highest rate, efficient | free gas (> ~10–15% at intake without handling), sand, temperature, workover cost, power |
| Gas lift | 100 to > 30,000 bpd | deep OK | robust to sand/gas/deviation, offshore friendly | needs gas and compression; can't reach very low Pwf |
| PCP | < ~2,000–4,000 bpd | shallow–medium (< ~6,000 ft typical) | viscous/heavy and sandy oil | elastomer temperature (~120–150 °C) and aromatic/H2S compatibility |
| Plunger lift | low liquid | deep OK | cheap gas-well deliquification | needs GLR, wellbore without restrictions |
| Jet pump | 100s–10,000s bpd | deep | no moving downhole parts | low efficiency, high power fluid volume |

Screen with these, then compare lifecycle cost (capex, power, workovers, deferred production) and model each candidate's uplift.

## Gotchas

- An uncalibrated correlation can be off by 20–30% in BHP — the operating point means little until matched.
- Vogel applied to an undersaturated well above Pb understates rate.
- Free gas at the pump intake kills ESP/rod efficiency; use the gas separator/handler or deepen the pump.
- Turner at bottom vs top: check both; the governing point is where velocity is lowest relative to critical.

## Verify

- [ ] IPR model and parameters stated with the test they came from.
- [ ] VLP correlation chosen by comparison with measured data, error reported.
- [ ] Operating point on the stable side of the VLP curve.
- [ ] Gas wells: actual rate vs Turner/Coleman critical rate checked at wellhead and bottom.
- [ ] Lift choice justified on rate, depth, GLR, sand, temperature, deviation and lifecycle cost.

Forecast inputs (reservoir pressure, water cut trends) come from engineering-technology.petroleum-engineering.reservoir-engineering.decline-curve-analysis-and-reserves or simulation VFP tables in engineering-technology.petroleum-engineering.petrel-eclipse.building-an-eclipse-simulation-deck.
