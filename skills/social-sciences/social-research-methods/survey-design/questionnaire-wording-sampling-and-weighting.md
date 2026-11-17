---
id: social-sciences.social-research-methods.survey-design.questionnaire-wording-sampling-and-weighting
name: questionnaire-wording-sampling-and-weighting
category: social-sciences
field: social-research-methods
product: survey-design
tags: [survey-design, survey-methodology, questionnaire-design, question-wording, total-survey-error, tse, sampling, probability-sampling, stratified-sampling, cluster-sampling, design-effect, deff, margin-of-error, nonresponse, nonresponse-bias, response-rate, aapor, weighting, post-stratification, raking, iterative-proportional-fitting, cognitive-interviewing, pretesting, acquiescence, social-desirability, double-barrelled, likert, mode-effects, web-survey, cati]
level: practitioner
status: gated
description: "Design a research survey end to end: question wording and pretesting, a sampling design with its design effect, nonresponse handling, and raking weights you can defend."
sources: ["Groves et al., Survey Methodology (2nd ed., Wiley 2009)", "AAPOR Standard Definitions (current edition)", "Kish, Survey Sampling (1965)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Survey design for research — wording, sampling, nonresponse, weighting

**Goal:** a survey whose numbers mean what you say they mean. Work through the
*total survey error* chain in order: does the question measure the concept, does the
sample represent the population, did the people who answered differ from those who
didn't, and do the weights repair rather than inflate the damage.

## 1. Start from the estimand, not the questionnaire
Write one line per key estimate: *population* (adults 18+ resident in region X on
date D), *quantity* (proportion who…, mean of…), *subgroups* you must report, and the
precision you need (e.g. ±4 points at 95% for each of 3 regions). This fixes sample
size and stratification before anyone drafts a question.

## 2. Question wording — the rules that actually bite
- **One idea per item.** "Is the service fast and friendly?" is double-barrelled; split it.
- **Balanced stems:** "Do you favour or oppose…", not "Do you favour…". Agree/disagree
  batteries invite **acquiescence**; prefer item-specific scales ("How satisfied…").
- **Reference periods** must be explicit and short for frequent events ("in the past 7 days").
- **Sensitive items:** self-completion modes (web, CASI) reduce social-desirability bias
  compared with interviewer modes; normalise the behaviour in the stem.
- **Response options** mutually exclusive and exhaustive; decide deliberately whether to
  offer a midpoint and "don't know" — both change distributions.
- **Order effects:** general-before-specific; randomise long lists to spread primacy
  (visual) / recency (aural) effects, and record the order shown.
- Reuse validated items (e.g. from national surveys) when you want comparability; quote
  them exactly — small edits break comparability.

## 3. Pretest, always
1. Expert review against a checklist.
2. **Cognitive interviews** (5–15 people, think-aloud plus probes: "what does 'household'
   mean to you here?").
3. A soft-launch pilot (~30–100 completes) to check timing, routing, item nonresponse and
   straight-lining. Fix, then freeze the instrument and version it.

## 4. Sampling
- Probability sample when you need population inference with a margin of error;
  opt-in panels need model-based adjustment and you should not quote a classical margin
  of error for them (AAPOR guidance warns against it).
- **Stratify** on variables known for the whole frame (region, size) — it usually lowers
  variance. **Cluster** (e.g. area then household) to cut field cost — it raises variance.
- Effective sample size ≈ n / deff. Kish's approximation for clustering:
  `deff ≈ 1 + (m − 1)·ρ`, where m = average cluster take and ρ the intraclass correlation.
  With m = 20 and ρ = 0.05, deff = 1 + 19 × 0.05 = 1.95: you need roughly double the interviews.
- Unequal weighting adds its own design effect, roughly `1 + CV²` of the weights.

## 5. Nonresponse
- Report response rates with **AAPOR** Standard Definitions (RR1–RR6; the 10th edition is dated 2023) and say which. RR1 counts only completes over all eligible plus unknown-eligibility cases; RR2 adds partials; RR3/RR4 replace unknowns with an estimated eligibility share e; RR5/RR6 assume no unknowns are eligible.
- A low response rate is not itself bias; bias arises where response propensity
  correlates with the outcome. Check by comparing early vs late responders, frame
  variables for respondents vs nonrespondents, and benchmarks (census marginals).
- Reduce it at source: advance letters, multiple contacts, mode switching, incentives
  (unconditional prepaid incentives tend to outperform promised ones).

## 6. Weighting, in three steps
1. **Base weights** = 1 / selection probability.
2. **Nonresponse adjustment** within cells or by modelled propensity.
3. **Calibration** to known totals — post-stratification for a full cross-table, or
   **raking** (iterative proportional fitting) over margins such as age × sex, region,
   education. R: `survey::rake()` / `calibrate()`; Stata: `svyset` plus user-written
   `ipfraking` (check availability for your version).
Then **trim** extreme weights (a common rule caps at ~5× the median, but treat that as a
judgement call) and report the weighting design effect. Analyse with design-aware
software (`svyset`, `survey` package), never as if the data were a simple random sample.

## Gotchas
- Calibrating to a variable you also want to estimate makes that estimate match the
  benchmark by construction.
- Mode change mid-study (phone → web) can shift answers more than real change does.
- Skip logic errors silently create "missing" that is really "not asked"; code them apart.

## Verify
- [ ] Every key estimate has a written population, quantity and precision target.
- [ ] Instrument cognitively tested and piloted; final version frozen and archived.
- [ ] Planned n accounts for the design effect, not just the SRS formula.
- [ ] Response rate reported with the named AAPOR definition.
- [ ] Weights built base → nonresponse → calibration, trimmed, deff reported.
- [ ] Analysis uses survey-design variance estimation.

*Checked 2026-10-19: deff arithmetic and the Kish weighting deff 1+CV^2 (equal to n*sum(w^2)/sum(w)^2 on 10,000 simulated lognormal weights, both 1.859) computed; AAPOR RR definitions from secondary summaries of the Standard Definitions; `ipfraking` exists on SSC/IDEAS. The R `survey` and Stata `svyset` calls and the weight-trimming threshold are practice conventions, not run (gated: unconfirmed, source is paywalled or blocked).*
