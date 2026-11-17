---
id: social-sciences.psychology.psychometrics.scale-development-reliability-and-factor-analysis
name: scale-development-reliability-and-factor-analysis
category: social-sciences
field: psychology
product: psychometrics
tags: [psychometrics, psychology, scale-development, questionnaire, likert, item-writing, reliability, cronbachs-alpha, mcdonalds-omega, test-retest, icc, factor-analysis, efa, cfa, parallel-analysis, lavaan, psych-package, jamovi, jasp, mplus, measurement-invariance, construct-validity, convergent-validity, discriminant-validity, irt, item-response-theory, norming]
level: practitioner
status: gated
description: "Build and validate a psychological scale: item writing, pilot, EFA then CFA on separate samples, omega over alpha, measurement invariance and validity evidence."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scale development, reliability and factor analysis

**Goal:** produce a questionnaire whose scores mean what you claim, are consistent,
and work the same way across the groups you will compare.

## 1. Define the construct before writing items
Write a one-paragraph definition: what the construct includes, what it excludes, and
which neighbouring constructs it must be distinguishable from. Decide if it is one
dimension or several facets. Search for an existing validated scale first — a new
scale needs a reason.

## 2. Write and screen items
- Write 2–3× the items you expect to keep. One idea per item; no double-barrels
  ("I am calm and organised"), no double negatives, reading age appropriate to the sample.
- Mix some reverse-keyed items to catch acquiescence — but they often load as a
  separate "method" factor; plan for that.
- Response format: 5- or 7-point Likert with every point labelled is a common default.
- Expert review (content validity) and 5–10 **cognitive interviews** ("what did you
  think this question was asking?") before any quantitative pilot.

## 3. Exploratory factor analysis (sample 1)
- Rough sample guide: 200+ and ≥5–10 per item; more if communalities are low.
- Check factorability: KMO > .6, Bartlett's test significant.
- Decide the number of factors with **parallel analysis** (R `psych::fa.parallel`) —
  not eigenvalues > 1 (Kaiser), which over-extracts (simulated: 20 items, one true factor with loadings .3, n=300 gave 8 eigenvalues > 1 but parallel analysis kept 1).
- Use an oblique rotation (oblimin/promax) — psychological factors usually correlate.
- For Likert items with few categories or skew, factor the **polychoric** correlation matrix.
- Drop items with weak primary loadings (< ~.40) or cross-loadings within ~.20 of the
  primary, then re-run. Keep content coverage in mind, not just numbers.

## 4. Confirmatory factor analysis (new sample 2)
Never confirm on the data you explored. In R `lavaan`:
```r
model <- 'anx =~ i1 + i2 + i3 + i4
          avoid =~ i5 + i6 + i7 + i8'
fit <- cfa(model, data = d, ordered = TRUE, estimator = "WLSMV")
fitMeasures(fit, c("cfi","tli","rmsea","srmr"))
```
Common heuristics (Hu & Bentler 1999) (gated: unconfirmed, source is paywalled or blocked): CFI/TLI ≥ .95, RMSEA ≤ .06, SRMR ≤ .08 — guidelines, not laws, and
they behave differently with ordinal estimators. Adding error covariances from
modification indices to "fix" fit is capitalising on chance unless theoretically justified.

## 5. Reliability
- Report **McDonald's omega** (`semTools::compRelSEM` or `psych::omega`); alpha assumes
  equal loadings (tau-equivalence) and is often a lower bound (computed for loadings .9,.8,.5,.4,.3: alpha .705, omega .734).
- Test–retest over an interval suited to the construct (traits: 2–4 weeks), reported as
  ICC (two-way, absolute agreement), not Pearson r.
- Very high internal consistency (> .95) often signals redundant items.

## 6. Validity and invariance
- **Convergent/discriminant:** correlate with established measures; expect a pattern
  you predicted in advance (multitrait-multimethod logic).
- **Criterion:** does it predict a relevant outcome?
- **Measurement invariance** before comparing groups: configural → metric (loadings)
  → scalar (intercepts/thresholds). Without scalar invariance, mean differences across
  groups are not interpretable.
- **IRT** (R `mirt`) when you need item-level information, adaptive testing, or
  precision across trait levels.

## 7. Norms
If scores will be interpreted against a population, collect a norming sample that
matches it (stratified by age, sex, region) and report percentiles or T-scores.

## Gotchas
- Same-sample EFA→CFA overstates fit.
- Treating 3–4 category items as continuous distorts loadings.
- A scale validated in one language/culture is not validated in another without
  translation, back-translation and invariance testing.
- Uncertain: cut-offs above are conventional heuristics; cite the specific guideline
  you rely on in any write-up.
- Checked 2026-10-19: Python `factor_analyzer` KMO/Bartlett and the simulations above ran; `psych`, `semTools`, `lavaan`, `mirt` exist on CRAN, but the R code (lavaan block, `psych::fa.parallel`, `compRelSEM`) was not run here (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Construct definition written before items.
- [ ] Number of factors justified by parallel analysis, rotation oblique.
- [ ] CFA on an independent sample, fit indices reported in full.
- [ ] Omega (and test–retest ICC where relevant) reported per subscale.
- [ ] Invariance tested before any group mean comparison.
