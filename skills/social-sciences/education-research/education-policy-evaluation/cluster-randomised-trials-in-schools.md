---
id: social-sciences.education-research.education-policy-evaluation.cluster-randomised-trials-in-schools
name: cluster-randomised-trials-in-schools
category: social-sciences
field: education-research
product: education-policy-evaluation
tags: [education-policy-evaluation, programme-evaluation, program-evaluation, cluster-randomised-trial, cluster-rct, school-based-rct, randomised-controlled-trial, icc, intraclass-correlation, mdes, power-analysis, powerup, optimal-design, blocking, stratified-randomisation, attrition, wwc-standards, what-works-clearinghouse, eef, education-endowment-foundation, itt, cace, implementation-fidelity, multilevel-model, effect-size, hedges-g, cost-effectiveness, ingredients-method, preregistration]
level: advanced
status: draft
description: "Design and analyse cluster-randomised trials of school interventions: ICC-based power and MDES, blocked randomisation, attrition standards, ITT multilevel analysis, fidelity and cost-effectiveness."
sources:
  - "Hedges & Hedberg (2007), Intraclass correlation values for planning group-randomized trials in education, EEPA"
  - "Dong & Maynard (2013), PowerUp!, J. Research on Educational Effectiveness"
  - "What Works Clearinghouse Procedures and Standards Handbook (current version)"
  - "Levin, McEwan, Belfield, Bowden & Shand, Economic Evaluation in Education (3rd ed.)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cluster-randomised trials in schools

**Goal:** estimate the causal effect of an education programme (a tutoring model, a
curriculum, teacher coaching) by randomising schools or classes, with enough power and
rigour to meet clearinghouse standards (WWC, EEF) and inform policy.

## 1. Choose the unit of randomisation
- Randomise at the level the intervention operates: **school** for whole-school
  programmes or teacher training (avoids contamination between teachers sharing a
  staffroom); **class** or **pupil** only if spillover is implausible.
- Clustering means effective sample size is driven by the **number of clusters**, not pupils.

## 2. Power and MDES
- Inputs: ICC (share of outcome variance between schools), clusters, pupils per cluster,
  covariate R² at each level, alpha, power.
- Typical unconditional attainment ICCs in US schools are roughly .10–.25 (Hedges &
  Hedberg); a **strong pre-test** can cut the school-level variance dramatically and
  shrink the minimum detectable effect size (MDES).
- Tools: PowerUp! (spreadsheet/R `PowerUpR`), Optimal Design, or simulation.
- Be realistic about effects: many rigorous education RCTs find effects around 0.1 SD or
  less on standardised tests; designing to detect 0.4 SD is wishful.
- Example sense-check: with ~40 schools, 25 pupils each, ICC .15 and a good pre-test,
  MDES is often in the 0.15–0.25 range — compute yours, don't trust this.

## 3. Randomisation and recruitment
- Recruit and consent schools *before* randomising; collect baseline data before
  allocation where possible.
- **Block/stratify** on prior attainment, size, disadvantage or region (pairs or small
  blocks); randomise with documented code and seed, done by someone independent of
  delivery.
- Offer control schools something (wait-list, delayed access, a payment) to keep them in.
- Preregister (e.g. on the Registry of Efficacy and Effectiveness Studies, OSF) with the
  primary outcome and analysis plan.

## 4. Fieldwork threats
- **Attrition**: both overall and differential attrition count; WWC sets boundaries
  combining the two — check the current handbook. School drop-out after allocation is
  especially damaging; keep collecting outcome data from schools that stop delivering.
- **Contamination**: control teachers acquiring materials.
- **Outcome testing**: administered blind to allocation where possible; prefer
  independent standardised tests over developer-made measures (which inflate effects).
- **Implementation fidelity**: dosage, adherence, quality — measured in both arms
  (what did "business as usual" look like?).

## 5. Analysis
- **Intention-to-treat** as primary: everyone analysed in their allocated arm.
- Multilevel model (pupils in schools) or OLS with cluster-robust SEs, adjusting for
  pre-test and blocking variables:
  ```r
  lmer(post ~ treat + pre + block + (1 | school), data = d)
  ```
  With few clusters (< ~40), use small-sample corrections (e.g. Kenward–Roger, CR2).
- Report standardised effect size (Hedges' g with the total SD), CIs, and the ICC observed.
- **CACE / complier analysis** (instrumental variables) as secondary for take-up questions.
- Pre-specified subgroup analyses only (e.g. disadvantaged pupils), with interaction tests.

## 6. Cost-effectiveness
Use the **ingredients method**: list every resource (staff time, training, materials,
facilities, including donated or volunteer inputs) at market prices, compute cost per
pupil, then cost per unit of effect (e.g. per 0.1 SD). Tools such as CostOut help; report
costs to schools separately from total societal cost.

## Gotchas
- Analysing pupils as independent ignores clustering and gives false significance.
- Declaring "no effect" from an underpowered trial — report the CI and MDES.
- Uncertain: attrition thresholds and ICC values differ by country and outcome; use local
  estimates (e.g. EEF/UK datasets) where available.

## Verify
- [ ] Unit of randomisation matches the intervention level.
- [ ] Power computed from realistic ICC, covariate R² and plausible effect size.
- [ ] Blocked randomisation by an independent person; preregistration dated before allocation.
- [ ] Attrition (overall and differential) reported against standards.
- [ ] ITT multilevel analysis with pre-test; effect size, CIs, fidelity and cost per pupil reported.
