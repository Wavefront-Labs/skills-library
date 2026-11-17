---
id: engineering-technology.chemical-engineering.process-design.debottlenecking-study-method
name: debottlenecking-study-method
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-debottlenecking-and-optimisation, debottlenecking-study-method, debottlenecking, capacity-increase, revamp]
level: practitioner
status: draft
description: "Run a debottlenecking study: define the target, find the limiting equipment, test fixes and rank them by cost and benefit."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debottlenecking study method

**Goal:** Run a debottlenecking study: define the target, find the limiting equipment, test fixes and rank them by cost and benefit.

## Steps
1. Define the goal (for example plus 10 to 20 percent throughput) and the performance basis from reconciled plant data and a calibrated simulation.
2. Rate every major equipment item at the target throughput against its design limits (hydraulics, duty, motor and relief limits); list those over about 90 to 100 percent.
3. Find the first bottleneck, propose the cheapest fix (operating change, internals, retube, impeller trim), re-run, and repeat until the goal is met.
4. Check the utilities, relief and flare, instruments and product quality for the new case.
5. Cost each option and rank by incremental benefit per cost; present with uncertainty.

## Gotchas
- Bottlenecks shift as each is removed; iterate.
- Check mechanical and relief limits, not only process ones.

## Verify
- [ ] The calibrated model matches plant data before the study.
- [ ] All equipment lies within limits at the target.
