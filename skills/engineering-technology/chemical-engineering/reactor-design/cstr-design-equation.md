---
id: engineering-technology.chemical-engineering.reactor-design.cstr-design-equation
name: cstr-design-equation
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-ideal-reactor-design, cstr-design-equation, cstr, continuous-stirred-tank, design-equation, reactor-sizing, cstr-in-series, residence-time, steady-state-reactor, conversion]
level: practitioner
status: verified
description: "Size CSTRs from the steady-state design equation, including volume change for gases and CSTRs in series, with first-order and general rate worked examples."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSTR sizing and series of CSTRs

**Goal:** reactor volume for a target conversion.

## Design equation
Steady state, perfect mixing: V = F_A0 X / (-r_A) evaluated at the exit concentration (and temperature). The reactor operates at the lowest-rate (exit) conditions, so it needs more volume than a PFR for positive-order reactions.

## First order, constant density liquid
tau = V/v0 = X / (k (1 - X)). Example: k = 0.1 per min and X = 0.9 gives tau = 0.9/(0.1 x 0.1) = 90 min (versus a PFR at tau = -ln(0.1)/0.1 = 23 min). Volume ratio about 3.9 (recomputed: 90/23.03 = 3.91).

## N equal CSTRs in series (first order)
Each stage tau_i: X = 1 - 1/(1 + k tau_i)^N. With N = 3 and the same total volume as above, X reaches about 0.98 for the total tau of 90 min (k tau_i = 3): 1 - 1/4^3 = 0.984 (recomputed). As N increases the performance approaches a PFR.

## General rate laws
Solve algebraically for the exit concentration; use a root finder for nonlinear rate laws. For several steady states (exothermic reactions) see `engineering-technology.chemical-engineering.reactor-design.multiple-steady-states-in-cstr`.

## Gas phase
Volumetric flow changes with moles; use concentrations C_A = C_A0 (1 - X)/(1 + eps X) (isothermal, constant pressure) with eps = y_A0 delta.

## Practice
- Choose the number of stages from cost: each extra stage adds mixers and instruments.
- Check mixing time against residence time (mixing time should be a small fraction).

## Gotchas
- Using the inlet concentration in the rate (a PFR habit).
- Neglecting volume change with gas phase CSTRs or vapour-generating reactors.

## Verify
- [ ] Re-solve with a simple script to confirm V for the target conversion.
- [ ] Residence time and mixing power consistent.
