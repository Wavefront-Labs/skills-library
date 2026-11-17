---
id: sales-marketing.market-research-consumer-insights.survey-design-and-analysis.unbiased-questionnaire-and-significance-reads
name: unbiased-questionnaire-and-significance-reads
category: sales-marketing
field: market-research-consumer-insights
product: survey-design-and-analysis
tags: [survey-design-and-analysis, market-research, consumer-research, questionnaire-design, survey-design, question-wording, leading-questions, response-scales, likert, sampling, quota-sampling, sample-size, margin-of-error, weighting, significance-testing, z-test, chi-square, cross-tabs, banner-tables, data-cleaning, speeders, straightliners, insight-reporting, quantitative-research]
level: practitioner
status: draft
description: "Design an unbiased consumer questionnaire, set sample size and quotas, clean the data, read significance on cross-tabs, and report findings that answer the business question."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unbiased questionnaire design and significance reads

**Goal:** run a quantitative consumer survey whose answer a business can act on:
the right question, asked without bias, of the right people, in enough numbers,
read honestly.

## 1. Start from the decision
Write one line: "We will use this to decide ___." Then list the 3–5 things you
must know to make that decision. Every question must trace to one of them; cut
the rest (each extra minute raises drop-out and lowers attention). Aim for ≤ 12
minutes on mobile.

## 2. Questionnaire flow
1. **Screener** — qualify the target (category user, age, region); terminate
   non-qualifiers early. Hide the sponsor and topic where knowing them biases answers.
2. **Behaviour before attitude** — what they did, then what they think.
3. **Unaided before aided** — "Which brands of X can you think of?" before showing a list.
4. **General before specific**, sensitive questions (income) near the end.
5. **Demographics** at the end (except those needed for quotas).

## 3. Wording rules
- One idea per question — "Is it fast and reliable?" is two questions.
- No leading or loaded words: "How much do you enjoy…" → "How would you rate…".
- Balanced scales: equal positive and negative points, labelled ends; use 5 or 7
  points and keep direction consistent through the survey.
- Mutually exclusive, exhaustive codes, with "Other (specify)" and "Don't know".
- Specific time frames: "in the past 4 weeks", not "recently".
- Randomise option order for lists (not for ordered scales); rotate concept order.
- Pilot with 5–10 real people or a soft launch of ~10% of sample; read open-ends.

## 4. Sample and quotas
- Margin of error at 95% for a proportion near 50%: about ±1/√n — n=400 → ±5,
  n=1,000 → ±3.1 points. **Every subgroup you'll report needs its own base**;
  aim for ≥ 100 per subgroup, flag bases < 50 as indicative.
- Set **quotas** on the variables that drive answers (age, gender, region, user
  type) to match the population (census or category data), then **weight** minor
  imbalances. Report effective sample size after weighting.
- Online panels are non-probability samples — say so; the ± figures are a guide.

## 5. Clean the data
Remove: **speeders** (completion < ~⅓ of median time), **straightliners** on grids,
failed attention checks, gibberish open-ends, duplicates. Typically 5–15% of
completes. Document the rules before looking at results.

## 6. Read significance on cross-tabs
- Run banner tables (columns = key subgroups) with column-proportion tests at 95%.
- Two proportions: z = (p1 − p2) / √(p(1−p)(1/n1 + 1/n2)), p = pooled; |z| > 1.96
  is significant at 95%. Most tab tools (Q, SPSS, Displayr, Qualtrics) letter-flag this.
- Beware **multiple comparisons**: across 200 cells, ~10 will "differ" by chance at
  95%. Prioritise differences that are large, consistent and pre-hypothesised.
- Significant ≠ important: a 3-point difference with n=5,000 may be real but irrelevant.

## 7. Report
Lead with the answer to the decision in one sentence, then 3–5 supporting
findings, each with chart, base size, and "so what". Appendix holds method,
questionnaire, weighting and cleaning rules.

## Gotchas
- Stated purchase intent overstates real purchase; calibrate (see copy-and-concept-testing).
- Scale points mean different things across cultures; avoid cross-country raw comparisons.
- Mobile grids break attention — keep grids short or use card sorts.

## Verify
- [ ] Every question maps to the stated decision.
- [ ] Wording reviewed for double-barrelled, leading and unbalanced items; pilot done.
- [ ] Subgroup bases ≥ 100 (or flagged); quotas and weighting documented.
- [ ] Cleaning rules set before analysis; removals counted.
- [ ] Reported differences are significant *and* meaningful, with bases shown.
