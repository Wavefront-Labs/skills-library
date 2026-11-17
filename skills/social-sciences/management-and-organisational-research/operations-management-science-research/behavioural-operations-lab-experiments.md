---
id: social-sciences.management-and-organisational-research.operations-management-science-research.behavioural-operations-lab-experiments
name: behavioural-operations-lab-experiments
category: social-sciences
field: management-and-organisational-research
product: operations-management-science-research
tags: [operations-management-science-research, behavioral-operations, behavioural-operations, newsvendor, pull-to-center, beer-game, bullwhip-effect, otree, z-tree, lab-experiment, incentive-compatible, induced-value, experimental-economics, decision-models, operations-research, supply-chain, inventory-decisions, learning-across-rounds, repeated-measures, mixed-effects, prolific, management-science, msom]
level: practitioner
status: draft
description: "Run behavioural-operations lab experiments (newsvendor, beer game, queueing choices): induced-value incentives, oTree/z-Tree build, repeated rounds, benchmarks vs optimal and panel analysis."
sources:
  - "Schweitzer & Cachon (2000), Decision bias in the newsvendor problem, Management Science"
  - "Sterman (1989), Modeling managerial behavior: misperceptions of feedback, Management Science"
  - "Donohue, Katok & Leider (eds.), The Handbook of Behavioral Operations (2018)"
  - "Chen, Schonger & Wickens (2016), oTree, J. Behavioral and Experimental Finance"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Behavioural operations lab experiments

**Goal:** test how real decision-makers deviate from the normative solution of an
operations model (inventory, capacity, forecasting, queueing) and why — with the
experimental-economics standards that operations journals expect.

## 1. Start from a model with a known optimum
The power of behavioural operations is the benchmark: you know what a rational,
risk-neutral agent should do. Classic paradigms:
- **Newsvendor**: choose an order quantity q against random demand; optimal q* is the
  critical fractile F⁻¹((p − c)/p) for price p and cost c (no salvage). The robust
  finding is **pull-to-centre** — orders sit between q* and mean demand, in both high-
  and low-margin conditions (Schweitzer & Cachon).
- **Beer distribution game**: multi-echelon ordering with delays; subjects under-weight
  the supply line, producing the bullwhip effect (Sterman).
- Others: capacity/queue joining, forecasting from time series, contracting between a
  supplier and retailer (human vs computerised counterpart).
State the normative prediction and the behavioural alternative before you collect data.

## 2. Design rules
- **Induced value / real incentives.** Pay subjects in proportion to profit earned (an
  exchange rate from experimental currency), so the model's objective is their
  objective. Hypothetical play is a reviewer red flag in this field. Show the expected
  earnings range in the protocol; deception is generally not accepted in
  experimental-economics labs.
- **Repeated rounds** (often 30–50+) with feedback, to see learning; randomise demand
  draws but consider giving every subject the *same* demand sequence (common random
  numbers) to reduce noise across treatments.
- **Between-subjects treatments** for the main manipulation (e.g. high vs low margin,
  feedback frequency, order bounds), with within-subject variation only where needed.
- **Comprehension quiz** before paid rounds; practice rounds unpaid.
- Unit of independence: in interactive games (beer game, contracts), the *group or
  matching group* is the independent observation, not the individual or the round.

## 3. Build and run
- **oTree** (Python, browser-based, works online or in the lab) or **z-Tree** (classic
  Windows lab software). Version-control the code and archive the exact version used.
- Lab recruitment via ORSEE or SONA; online via Prolific (shorter sessions, attention
  checks, and be explicit about bonus payment mechanics).
- Pilot for timing, payment calibration and bugs; log every decision with timestamps.

## 4. Analysis
- Plot average decision by round against the optimum and the behavioural benchmark.
- Test treatment effects with mixed-effects regressions (random intercepts by subject,
  round as a covariate) or, conservatively, non-parametric tests on subject- or
  group-level averages (Mann–Whitney, Wilcoxon).
- Fit candidate behavioural models (anchoring-and-adjustment, demand chasing, loss or
  regret aversion, quantal response) and compare by likelihood/AIC; avoid declaring a
  mechanism from means alone.
- Report payments, session count, subject pool and exclusions.

## Gotchas
- Treating 50 rounds × 40 subjects as 2,000 independent observations inflates
  significance — cluster or aggregate.
- Students vs managers: replications often find similar biases among practitioners,
  but reviewers may still ask; a practitioner sample is a strong add-on.
- Displaying the expected-profit curve or a decision-support tool is itself a treatment.
- Uncertain: field-specific norms on online vs lab samples are still shifting.

## Verify
- [ ] Normative optimum and behavioural hypothesis stated before data collection.
- [ ] Earnings tied to in-game profit; no deception; comprehension check passed.
- [ ] Independence unit correctly identified for tests.
- [ ] Decisions plotted vs optimum by round; learning examined.
- [ ] Code, instructions, data and payment details archived.
