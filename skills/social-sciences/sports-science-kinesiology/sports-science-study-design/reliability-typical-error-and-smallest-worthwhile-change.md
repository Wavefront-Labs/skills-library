---
id: social-sciences.sports-science-kinesiology.sports-science-study-design.reliability-typical-error-and-smallest-worthwhile-change
name: reliability-typical-error-and-smallest-worthwhile-change
category: social-sciences
field: sports-science-kinesiology
product: sports-science-study-design
tags: [sports-science-study-design, sports-science, kinesiology, statistics, research-design, small-sample, repeated-measures, crossover-design, washout, randomised-controlled-trial, reliability-study, test-retest, typical-error, tem, coefficient-of-variation, icc, bland-altman, limits-of-agreement, smallest-worthwhile-change, swc, minimal-detectable-change, mdc, magnitude-based-inference, mbi, equivalence-testing, mixed-models, individual-responses, sesoi]
level: practitioner
status: draft
description: "Design and analyse small-sample sports-science studies: repeated-measures and crossover designs, typical error and ICC from reliability trials, and smallest worthwhile change."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reliability, typical error and smallest worthwhile change

**Goal:** get trustworthy answers from the small samples sports science usually has,
by knowing your measurement noise and designing to beat it.

## 1. Start with a reliability study
Before (or within) an intervention, test the measure twice (or more) under identical
conditions, with familiarisation first (first trials often differ — learning effect).
Report:
- **Typical error (TE)** = SD of the difference scores / √2 — the within-subject noise
  in raw units. As a **CV%** for ratio-scale measures (compute on log-transformed data,
  back-transform).
- **ICC** — specify the form (e.g. ICC(3,1) or ICC(2,1); two-way, absolute agreement vs
  consistency). ICC depends on between-subject spread: a homogeneous elite sample gives a
  low ICC even with tiny TE. Always report TE alongside.
- **Systematic bias** (mean change between trials) and **Bland–Altman limits of agreement**
  for method-comparison (validity) studies — correlation is not agreement.

## 2. Smallest worthwhile change (SWC)
The smallest effect that matters — your SESOI.
- Distribution-based default (Hopkins): 0.2 × between-subject SD (small Cohen effect).
- Better when possible: anchor to performance — e.g. for elite athletes, about 0.3 × the
  within-athlete race-to-race CV (Hopkins et al. for individual sports) — or to
  clinical/practical consequences.
- If **TE > SWC**, a single test can't detect a worthwhile change in an individual;
  repeat measurements, improve protocol, or use another measure.
- **Minimal detectable change** (MDC95 = 1.96 × √2 × TE) is the change needed to exceed
  noise for one person with 95% confidence.

## 3. Designs for small samples
- **Crossover** (each participant does all conditions in randomised, counterbalanced
  order) — ideal for acute interventions (supplements, warm-ups, footwear). Needs an
  adequate **washout** and stable performance; analyse with period and sequence effects.
  Not suitable for training adaptations that persist.
- **Parallel-group RCT** for chronic training studies — always with a control group
  (seasonal and familiarisation changes are large).
- **Repeated measures** over time: mixed models with participant random effects; handle
  missing sessions without dropping participants.
- **Blinding**: double-blind placebo where feasible (e.g. caffeine, nitrate); check
  blinding success by asking participants to guess.
- Power for repeated designs depends on TE: required n ≈ proportional to (TE/SWC)²;
  simulate for complex designs.

## 4. Inference
- Report effects with CIs in raw units and relative to SWC.
- **Magnitude-based inference (MBI/"MBD")** was widely used in sports science but was
  criticised for inflated error rates (Sainani 2018; Welsh & Knight 2015); many journals
  no longer accept it. Use frequentist **equivalence/minimal-effects tests** against the
  SWC, or Bayesian estimation with stated priors — both answer the same practical question
  with known properties.
- **Individual responses:** SD of change in the intervention group exceeds control only
  if true individual differences exist: SD_IR = √(SD²_int − SD²_ctrl). Don't label
  "responders" by a single post-test exceeding a threshold — that ignores noise and
  regression to the mean.

## 5. Reporting
Follow CONSORT (with the crossover extension where relevant); report raw data or plots of
individual change (spaghetti plots), TE/CV, SWC rationale, and the full model.

## Gotchas
- Sample of 10 highly trained athletes: high relevance, low precision — say what the CI allows.
- Multiple outcomes × time points × conditions → control error rates or name one primary outcome.
- Uncertain: the 0.2 and 0.3 multipliers are conventions from specific authors; justify for your context.

## Verify
- [ ] Reliability (TE/CV, ICC form, bias) established with familiarisation.
- [ ] SWC defined and justified; TE compared to SWC.
- [ ] Design (crossover vs parallel) fits the intervention's persistence; washout justified.
- [ ] Inference uses equivalence or Bayesian methods, not MBI.
- [ ] Individual-response claims use control-group variability.
