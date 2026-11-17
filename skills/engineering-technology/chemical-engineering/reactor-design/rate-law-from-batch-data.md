---
id: engineering-technology.chemical-engineering.reactor-design.rate-law-from-batch-data
name: rate-law-from-batch-data
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-kinetics-and-rate-laws, rate-law-from-batch-data, rate-law, reaction-order, batch-data, integral-method, differential-method, initial-rates, method-of-excess, kinetics, half-life]
level: practitioner
status: draft
description: "Derive a reaction rate law and order from batch concentration-time data using integral, differential, initial-rate and excess methods, with fit diagnostics."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deriving a rate law from batch data

**Goal:** a rate expression -r_A = k C_A^a C_B^b supported by data and with stated uncertainty.

## Methods
1. **Integral method**: guess an order, integrate, test linearity. Zero order: C_A vs t linear; first order: ln C_A vs t linear (slope -k); second order (single reactant): 1/C_A vs t linear (slope k).
2. **Differential method**: estimate dC_A/dt from data (smoothed or by fitting a polynomial), plot ln(-dC_A/dt) vs ln C_A, slope = order. Noise amplification is the drawback; use only with good data.
3. **Initial rates**: run several experiments at different initial concentrations, take the initial slope of each, plot ln(rate) vs ln C_0; gives order with respect to each reactant and avoids product inhibition.
4. **Method of excess (isolation)**: make B in large excess so C_B is nearly constant; the observed rate constant is k' = k C_B0^b; repeat at different C_B0 to get b.
5. **Half-life**: for n-th order, t_1/2 scales as C_0^(1-n); the slope of ln t_1/2 vs ln C_0 gives 1-n.

## Practice
- Cover a wide concentration range (a factor of 10 or more) and at least 3 temperatures if Arrhenius parameters will follow.
- Prefer nonlinear least squares on the concentration-time data itself over linearised plots, which distort the error weighting.
- Test a reversible reaction: if conversion plateaus below 100%, include the reverse term.
- Report parameters with confidence intervals and the residual plot.

## Gotchas
- Gas-phase or volume-changing batch systems need the volume change in the concentration.
- Mass transfer or heating-up periods at the start distort early points.
- A good linear fit of one order does not exclude another; compare residual plots.

## Verify
- [ ] Residuals randomly scattered; no trend with time.
- [ ] Predicted conversion at an unused condition checked in a validation run.
