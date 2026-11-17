---
id: engineering-technology.chemical-engineering.reactor-design.reaction-network-selectivity-analysis
name: reaction-network-selectivity-analysis
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-kinetics-and-rate-laws, reaction-network-selectivity-analysis, selectivity, yield, parallel-reactions, series-reactions, consecutive-reactions, reaction-network, instantaneous-selectivity, reactor-selection]
level: practitioner
status: draft
description: "Analyse parallel and series reaction networks for selectivity and yield, choosing reactor type, concentration and temperature levels that favour the desired product."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reaction network and selectivity analysis

**Goal:** choose reactor type and operating levels to maximise desired product, using the structure of the network.

## Parallel reactions
A -> D (rate k1 C_A^a1) and A -> U (rate k2 C_A^a2). Instantaneous selectivity S = r_D/r_U = (k1/k2) C_A^(a1 - a2).
- If a1 > a2: keep C_A high (PFR or batch; avoid dilution; no recycle of product that dilutes).
- If a1 < a2: keep C_A low (CSTR at high conversion, dilution, semibatch with slow feed of A).
- Temperature: high T favours the reaction with the higher activation energy.

## Series reactions
A -> B -> C (first order, k1 and k2) with B desired. In a PFR or batch reactor, C_B passes through a maximum at tau_opt = ln(k1/k2)/(k1 - k2), with C_B,max = C_A0 (k1/k2)^(k2/(k2 - k1)). Stop the reaction there or recycle. A CSTR gives a lower maximum yield of the intermediate than a PFR.

## Procedure
1. Draw the network with known rate laws and activation energies.
2. Compute S as function of C and T.
3. Pick reactor type and feed policy (for example slow addition of the species whose concentration should stay low).
4. Quantify yield versus conversion curves for PFR and CSTR in a spreadsheet.
5. Add the cost of separating by-products; the best yield point may not be the best economic point.

## Gotchas
- Mixing limitations can change the apparent selectivity at scale-up, especially for fast competing reactions (see `engineering-technology.chemical-engineering.reactor-design.stirred-tank-power-and-mixing-time`).
- Heat removal limits fix temperature windows regardless of selectivity preference.

## Verify
- [ ] Yield versus conversion plot for the chosen reactor.
- [ ] Sensitivity of selectivity to temperature shown.
