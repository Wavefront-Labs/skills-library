---
id: social-sciences.psychology.experimental-design.power-analysis-counterbalancing-and-preregistration
name: power-analysis-counterbalancing-and-preregistration
category: social-sciences
field: psychology
product: experimental-design
tags: [experimental-design, psychology, research-methods, within-subjects, between-subjects, repeated-measures, factorial-design, counterbalancing, latin-square, order-effects, carryover, power-analysis, sample-size, gpower, g-power, simr, pwr, effect-size, sesoi, preregistration, osf, aspredicted, randomisation, manipulation-check, confounds]
level: practitioner
status: verified
description: "Plan a psychology experiment end to end: pick within/between design, counterbalance order, run a power analysis for the real effect size, and preregister it."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Planning a psychology experiment: design, counterbalancing, power, preregistration

**Goal:** turn a hypothesis into a design that can actually detect the effect, with
order and stimulus confounds controlled, and a time-stamped plan that separates
confirmatory from exploratory analysis.

## 1. Write the hypothesis as a contrast
State the exact comparison: "RT is slower in incongruent than congruent trials" — not
"congruency affects RT". Name the dependent variable, its unit, the trial-level
exclusion rule, and the single test that confirms or refutes it. If you can't name
that test now, you will be choosing it after seeing the data.

## 2. Within or between?
- **Within-subjects** (everyone does every condition): far more power per participant
  because individual differences cancel. Risks: practice, fatigue, carryover, and
  participants guessing the hypothesis.
- **Between-subjects:** needed when exposure is irreversible (a deception, a learning
  manipulation, a mood induction that lingers). Typically needs several times more people.
- **Mixed / factorial:** e.g. 2 (group, between) × 3 (load, within). Every extra factor
  multiplies cells and interactions need far more power than main effects — an
  an attenuated interaction (effect halves in one condition) can need roughly 4× or more
  the sample of the main effect. Computed for a 2×2 between design with d = 0.4 in one row and 0.2 in the other: main effect needs about 88 per cell, the interaction about 786 (roughly 9×), so 4× is a floor; check your own pattern by simulation.

## 3. Counterbalancing
- **Full counterbalancing:** all k! orders — fine for 2–3 conditions (2 or 6 orders).
- **Balanced Latin square:** for k conditions, k orders where each condition appears
  once in each position and (for even k) each condition precedes each other once.
  For odd k you need 2k orders to balance first-order carryover (checked in code: the 5-order cyclic square built from the sequence 0,1,4,2,3 plus its reversals gives all 20 ordered pairs, each exactly twice; the 5-order square alone covers only 10 of 20).
- **Randomise within blocks** when conditions are trial-level and intermixed.
- Counterbalance **stimulus-to-condition assignment** too (list A/B): otherwise the
  "condition" effect may be a word-set effect.
- Recruit in multiples of the number of orders so each order has equal n; keep the
  order as a variable so you can test it.

## 4. Power analysis — honestly
1. Choose the effect size from the **smallest effect of interest (SESOI)** or a
   bias-corrected meta-analytic estimate — not a single published study (published
   effects are inflated by publication bias).
2. Simple designs: G*Power or R `pwr`. For a paired t-test the input is d_z (mean
   difference / SD of differences), not the between-groups d — confusing them is the
   classic error. (statsmodels: d=0.5 at 80% power needs 34 pairs with a paired test, 64 per group between subjects.)
3. Mixed models / many trials per person: simulate (R `simr`, or write your own
   generate-fit-repeat loop). Number of participants *and* trials both matter.
4. Target 80–95% power at α = .05; add an attrition/exclusion margin (often 10–20%).
5. If the n is infeasible, say so and change the design (within-subjects, more trials,
   stronger manipulation) rather than running an underpowered study.

## 5. Build in checks
- **Manipulation check** — did the induction work? Measure it, ideally after the DV
  so it doesn't contaminate it.
- **Attention checks** for online samples, with the exclusion rule fixed in advance.
- **Random assignment** by software, logged with the seed.
- **Blind** experimenters to condition where they interact with participants.

## 6. Preregister
On OSF Registries or AsPredicted, before data collection: hypotheses, design, planned
n and stopping rule, all exclusion criteria, the exact model (formula, covariates,
one- or two-tailed), and how you'll handle deviations. Label anything not in it as
exploratory in the paper. Registered Reports go further — see
social-sciences.psychology.replication-open-science.

## Gotchas
- Sequential peeking ("run 20 more and test again") inflates false positives unless you
  pre-specify a sequential design with corrected alpha.
- Rounding n down to the nearest counterbalancing multiple quietly lowers power.
- Demand characteristics are worst in within-subjects designs with obvious contrasts.
- Uncertain: specific power multipliers for interactions depend heavily on the
  pattern; treat any rule of thumb as a prompt to simulate.

## Verify
- [ ] Hypothesis maps to exactly one confirmatory test.
- [ ] Order and stimulus lists are counterbalanced and recorded per participant.
- [ ] Effect size for power is justified (SESOI or bias-corrected), correct d type used.
- [ ] Exclusion rules and stopping rule are written before data exist.
- [ ] Preregistration is time-stamped and linked from the analysis code.
