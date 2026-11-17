---
id: social-sciences.management-and-organisational-research.survey-scale-development-management.developing-and-validating-a-management-scale
name: developing-and-validating-a-management-scale
category: social-sciences
field: management-and-organisational-research
product: survey-scale-development-management
tags: [survey-scale-development-management, scale-development, construct-validation, hinkin, mackenzie-podsakoff, content-validity, item-generation, efa, cfa, sem, lavaan, mplus, amos, measurement-invariance, discriminant-validity, htmt, ave, fornell-larcker, cronbachs-alpha, omega, common-method-bias, common-method-variance, harman-single-factor, marker-variable, nomological-network, formative-vs-reflective]
level: advanced
status: draft
description: "Develop and validate a new organisational construct scale: definition, item generation, content validity, EFA then CFA, reliability, HTMT discriminant validity, invariance and common-method bias."
sources:
  - "Hinkin (1998), A brief tutorial on the development of measures for use in survey questionnaires, Organizational Research Methods"
  - "MacKenzie, Podsakoff & Podsakoff (2011), Construct measurement and validation procedures, MIS Quarterly"
  - "Podsakoff, MacKenzie & Podsakoff (2012), Sources of method bias, Annual Review of Psychology"
  - "Henseler, Ringle & Sarstedt (2015), A new criterion for assessing discriminant validity, JAMS"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Developing and validating a management scale

**Goal:** create a new measure of an organisational construct (e.g. "leader
inclusiveness", "algorithmic control") that reviewers accept as reliable, valid and
distinct from the dozens of similar scales that already exist.

## 1. Justify a new scale
Search existing measures first (construct proliferation is a major critique). Write a
**construct definition**: what it is, what it is not, its dimensions, and whether it is
**reflective** (items are interchangeable manifestations) or **formative** (items
define it, e.g. a composite of practices). This choice changes the whole validation path;
the steps below assume reflective.

## 2. Item generation and content validity
- Generate items deductively (from the definition and literature) and inductively
  (interviews/critical incidents with target respondents). Start with roughly 2–3× the
  items you want to keep (e.g. 4–6 retained per dimension).
- Simple wording, one idea per item, no double-barrels, consistent referent (self vs
  team vs organisation) and time frame.
- **Content validity**: have subject-matter experts or naive judges sort items into
  construct definitions (including rival constructs). Quantify with Anderson & Gerbing's
  proportion of substantive agreement or Hinkin & Tracey's ANOVA approach; drop poorly
  matched items.

## 3. Factor structure — separate samples
1. **Sample 1: EFA** (principal axis or ML, oblique rotation). Use parallel analysis
   to choose factor count; drop items with low loadings (< ~.40–.50) or cross-loadings.
2. **Sample 2: CFA** (lavaan, Mplus, AMOS). Report χ², CFI, TLI, RMSEA, SRMR; common
   heuristic cut-offs (CFI/TLI ≥ .95, RMSEA ≤ .06, SRMR ≤ .08 — Hu & Bentler) are
   guidelines, not tests. Compare against plausible alternative models (one-factor,
   merged dimensions).
   ```r
   library(lavaan)
   m <- 'incl =~ i1 + i2 + i3 + i4
         voice =~ v1 + v2 + v3 + v4'
   fit <- cfa(m, data = d2, estimator = "MLR"); summary(fit, fit.measures = TRUE, standardized = TRUE)
   ```
3. Use ordinal estimators (WLSMV) for 4-point or skewed items.

## 4. Reliability and validity evidence
- **Reliability**: coefficient omega (preferred) and alpha; composite reliability ≥ .70.
- **Convergent**: AVE ≥ .50, correlations with related measures.
- **Discriminant**: **HTMT** < .85 (or .90) against the closest rival constructs; the
  Fornell–Larcker test is weaker. Include those rivals in your validation survey on
  purpose.
- **Nomological / criterion**: predicts theoretically linked outcomes, ideally from a
  different source or time (supervisor ratings, archival performance), and shows
  incremental validity over existing scales.
- **Measurement invariance** (configural → metric → scalar) across groups you will
  compare (countries, genders, languages) before comparing means.

## 5. Common-method bias (CMB)
Prevention beats statistical repair (Podsakoff et al. 2012):
- Separate predictor and outcome by **source** (employee vs supervisor) or **time**
  (two or three waves).
- Protect anonymity, counterbalance order, vary scale anchors.
- Statistical: a marker variable or an unmeasured latent method factor in CFA as a
  check. **Harman's single-factor test is widely regarded as insufficient** — don't
  rely on it alone.

## Gotchas
- Using the same sample for EFA and CFA is circular; reviewers notice.
- Modification indices that free error covariances across items "until it fits" — only
  with a substantive reason, and report them.
- Translated scales need back-translation and invariance testing.
- Uncertain: fit cut-offs and HTMT thresholds are debated; cite the ones you use.

## Verify
- [ ] Written construct definition with reflective/formative decision.
- [ ] Content-validity judging quantified; weak items removed.
- [ ] EFA and CFA on independent samples; alternative models compared.
- [ ] Omega, AVE, HTMT vs nearest rivals and incremental validity reported.
- [ ] CMB addressed by design (source/time separation), not only Harman's test.
