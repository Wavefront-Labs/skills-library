---
id: health-medicine.public-health.applied-epidemiology.study-design-measures-of-association-and-bias-appraisal
name: study-design-measures-of-association-and-bias-appraisal
category: health-medicine
field: public-health
product: applied-epidemiology
tags: [public-health, applied-epidemiology, epidemiology, study-design, cohort-study, case-control-study, cross-sectional-study, ecological-study, rct, incidence, prevalence, incidence-rate, person-time, risk-ratio, odds-ratio, rate-ratio, risk-difference, attributable-fraction, nnt, confidence-interval, p-value, confounding, selection-bias, information-bias, recall-bias, effect-modification, standardisation, age-standardised-rate, smr, dag, causal-inference, bradford-hill, strobe]
level: practitioner
status: draft
description: "Epidemiologic method in practice: matching question to study design, calculating rates and measures of association, standardisation, and appraising confounding, selection and information bias."
sources: [Rothman Greenland Lash Modern Epidemiology 4th ed, CDC Principles of Epidemiology in Public Health Practice 3rd ed, STROBE statement 2007, Hernan and Robins Causal Inference What If]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Study design, measures of association and bias appraisal

> General professional reference. For anything beyond descriptive work, involve a
> statistician early; the arithmetic below is standard but model choice is not.

**Goal:** answer a population-health question with the right design and the right
number, and say honestly how much that number can be trusted.

## 1. Match question to design
| Question | Design | Gives |
|---|---|---|
| How common is it now? | cross-sectional survey | prevalence, prevalence ratio |
| How often do new cases arise? | cohort / registry | incidence (risk, rate) |
| What causes a rare disease? | case-control | odds ratio |
| Does the intervention work? | RCT (cluster RCT for programmes); quasi-experimental if not feasible | risk ratio/difference |
| Patterns across areas/time | ecological, time series | hypotheses (beware ecological fallacy) |

## 2. The core arithmetic (2×2: exposed a/b, unexposed c/d; cases a, c)
- **Risk** (cumulative incidence) = new cases / population at risk over a period.
- **Rate** = new cases / **person-time** at risk.
- **Prevalence** ≈ incidence × average duration (steady state).
- **Risk ratio** RR = [a/(a+b)] / [c/(c+d)]; **odds ratio** OR = ad/bc (approximates
  RR when outcome is rare, < ~10%).
- **Risk difference** = risk exposed − risk unexposed; **NNT/NNH** = 1/|RD|.
- **Attributable fraction (exposed)** = (RR − 1)/RR; **population attributable
  fraction** = p_e(RR − 1)/[1 + p_e(RR − 1)] where p_e is exposure prevalence in the
  population (the Levin formula; use the case-based formula when confounding is
  present).
- Always report a **95% CI**; a p-value alone says nothing about magnitude.

## 3. Comparing populations fairly
- **Direct standardisation**: apply each population's age-specific rates to a standard
  population (e.g. ESP 2013, WHO world standard) → age-standardised rates. Needs
  stable age-specific rates.
- **Indirect standardisation**: apply standard rates to the local age structure →
  expected counts → **SMR** = observed/expected. Better with small numbers, but SMRs
  for different areas shouldn't be compared directly with each other.

## 4. Bias appraisal — ask these every time
- **Confounding**: a third factor associated with exposure and independently with
  outcome, not on the causal path. Draw a **DAG** before choosing adjustment variables;
  don't adjust for mediators or colliders. Handle by restriction, matching,
  stratification (Mantel–Haenszel), regression, or design (randomisation).
- **Selection bias**: who got into the study (or stayed in) depends on both exposure
  and outcome — healthy worker effect, loss to follow-up, non-response, Berkson's bias,
  inappropriate controls.
- **Information bias**: misclassification of exposure or outcome; differential
  (recall bias in case-control) can bias either way; non-differential usually toward
  the null for binary variables (not guaranteed).
- **Effect modification**: the association differs across strata — report stratified
  estimates, don't average it away.
- **Chance**: power/precision; multiple comparisons.
- **Reverse causation** in cross-sectional data.

## 5. From association to causation
Use structured reasoning: temporality (essential), strength, consistency,
dose–response, plausibility, coherence, experiment, specificity, analogy (Bradford
Hill) — as considerations, not a checklist score. Triangulate across designs.

## 6. Reporting
Follow **STROBE** (observational), CONSORT (trials), RECORD (routinely collected data).
State denominators, missing data handling, and the exact case definition.

## Gotchas
- Reporting an OR as "times more likely" when outcome is common — overstates effect.
- Crude rate comparisons between areas with different age structures.
- Treating absence of significance as evidence of no effect.
- Immortal time bias in cohort analyses of treatments.

## Verify
- [ ] Design matches the question and the measure reported matches the design.
- [ ] Numerator, denominator and time period explicit; CI reported.
- [ ] Age standardisation (or justification) for population comparisons.
- [ ] Confounding addressed with a stated adjustment rationale (DAG).
- [ ] Selection and information biases named with likely direction.
