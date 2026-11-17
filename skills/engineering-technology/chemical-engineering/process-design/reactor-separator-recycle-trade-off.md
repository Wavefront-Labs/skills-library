---
id: engineering-technology.chemical-engineering.process-design.reactor-separator-recycle-trade-off
name: reactor-separator-recycle-trade-off
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-flowsheet-synthesis, reactor-separator-recycle-trade-off, conversion-optimisation, recycle-economics, reactor-separator-trade-off, per-pass-conversion, annualised-cost, optimum, process-economics]
level: advanced
status: draft
description: "Quantify the reactor-separator-recycle trade-off: conversion per pass versus reactor size, separation load and recycle cost, and find the economic optimum."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reactor-separator-recycle economic trade-off

**Goal:** choose conversion per pass from total annualised cost, not from reactor performance alone.

## Cost components as conversion X rises
- Reactor cost rises (more volume or catalyst; sharply as X approaches equilibrium).
- Recycle flow and separation load fall (recycle ~ F (1 - X)/X for complete recycle).
- Raw material loss in purge or by-product selectivity may change.
- Compressor and pump costs fall with recycle rate.

## Procedure
1. Build a spreadsheet for the loop: for each X in a range (say 20 to 95% of equilibrium conversion), compute recycle flow, reactor size from kinetics, column or flash load, utilities.
2. Use shortcut costing (see `engineering-technology.chemical-engineering.process-design.equipment-cost-correlations-and-indexing`) and annualise with a capital charge factor (for example 0.2 to 0.3 per year, depending on hurdle rate; state yours).
3. Plot total annualised cost against X; identify the optimum; test sensitivity to feed cost, energy cost and catalyst price.
4. Verify with the rigorous simulation at the optimum and two neighbours.

## Gotchas
- The curve is usually flat near the optimum, so favour the lower-risk, lower-conversion side.
- Selectivity often falls with conversion; include it.
- Equipment bounds (maximum temperature, pressure) cap X before economics does.

## Verify
- [ ] Optimum insensitive (within a few percent of cost) to plausible price changes, or the sensitivity is recorded.
- [ ] Rigorous model reproduces the spreadsheet loop to within a few percent.
