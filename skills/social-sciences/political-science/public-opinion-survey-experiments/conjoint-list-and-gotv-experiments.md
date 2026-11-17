---
id: social-sciences.political-science.public-opinion-survey-experiments.conjoint-list-and-gotv-experiments
name: conjoint-list-and-gotv-experiments
category: social-sciences
field: political-science
product: public-opinion-survey-experiments
tags: [public-opinion-survey-experiments, survey-experiment, vignette-experiment, conjoint-analysis, choice-based-conjoint, amce, marginal-means, cregg, cjoint, list-experiment, item-count-technique, randomized-response, sensitive-questions, social-desirability-bias, gotv, get-out-the-vote, field-experiment, itt, cace, complier-average-causal-effect, noncompliance, pre-registration, egap, osf, power-analysis, manipulation-check, attention-check, qualtrics]
level: advanced
status: draft
description: "Designing political experiments: vignette and conjoint designs (AMCE), list experiments for sensitive items, and GOTV field experiments with ITT/CACE."
sources: ["Hainmueller, Hopkins & Yamamoto, 'Causal Inference in Conjoint Analysis' (2014)", "Leeper, Hobolt & Tilley, 'Measuring Subgroup Preferences in Conjoint Experiments' (2020)", "Blair & Imai, 'Statistical Analysis of List Experiments' (2012)", "Gerber & Green, Field Experiments: Design, Analysis, and Interpretation (2012)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conjoint, list and GOTV experiments

**Goal:** get causal estimates of what moves political attitudes and behaviour, using
the three designs political scientists use most — and avoid their known traps.

## 0. Common to all designs
- **Pre-register** hypotheses, outcomes and analysis (OSF, EGAP/AsPredicted).
- **Power analysis** before fielding; survey experiments commonly need 1,000+
  respondents to detect small effects (d ≈ 0.1–0.2).
- Randomise in the survey platform (e.g. Qualtrics randomiser) and store the assigned
  condition as a variable — reconstructing it later is error-prone.
- Attention checks: place *before* treatment; dropping people based on post-treatment
  checks can bias estimates.

## 1. Vignette and conjoint designs
- **Vignette:** one hypothetical scenario with a manipulated attribute (candidate's
  gender, policy framing).
- **Conjoint:** respondents choose between profiles (e.g. two candidates) whose
  attributes are randomised independently; typically 5–8 attributes, 5–10 tasks per
  respondent.
- Estimand: **AMCE** (average marginal component effect) via OLS on choice with
  respondent-clustered SEs. R: `cregg` or `cjoint`.
- **Gotcha:** comparing AMCEs between subgroups can mislead because AMCEs depend on
  the reference category; compare **marginal means** instead (Leeper et al.).
- Randomise attribute order across respondents (fixed within respondent); block
  implausible combinations (e.g. a 25-year-old with 30 years' experience) and document
  restrictions.
- For pricing-style conjoint in marketing, see
  sales-marketing.market-research-consumer-insights.pricing-research.van-westendorp-gabor-granger-and-conjoint.

## 2. List experiments (item count technique)
Control group sees J non-sensitive items and reports *how many* apply; treatment
group sees the same plus the sensitive item. Difference in means estimates prevalence
of the sensitive item.
- Avoid **ceiling/floor effects:** if all or none of the controls apply, the
  respondent's answer reveals the sensitive item. Choose negatively correlated control
  items so few people sit at 0 or J.
- Use 3–5 controls. Variance is high — needs larger samples than direct questions.
- Analyse with `list` package (Blair & Imai) for multivariate models and design-effect tests.

## 3. GOTV field experiments
Randomise households/individuals on a voter file to door-knocking, phone, mail or
texts; outcome is validated turnout from the official record.
- Report **ITT** (effect of assignment). With non-contact (one-sided non-compliance),
  estimate **CACE** = ITT ÷ contact rate, i.e. the effect on those actually reached.
- Randomise at the household level if multiple voters share an address (spillover).
- Check balance on past turnout; use it as a covariate for precision.
- Partner organisations may want to "help" by contacting control people — agree
  protocols in writing.
- Rough literature benchmarks: canvassing yields a few percentage points; impersonal
  mail and robocalls near zero (*benchmark magnitudes vary by election salience*).

## 4. Ethics
Deception and real-election interventions need explicit ethics review; consider
effects on election outcomes in close races and debrief survey respondents.

## Verify
- [ ] Pre-registration and power analysis done before fielding.
- [ ] Assigned condition stored in data; balance table checked.
- [ ] Conjoint subgroup comparisons use marginal means; SEs clustered by respondent.
- [ ] List-experiment ceiling/floor rates reported.
- [ ] GOTV reports ITT and CACE with the contact rate.
