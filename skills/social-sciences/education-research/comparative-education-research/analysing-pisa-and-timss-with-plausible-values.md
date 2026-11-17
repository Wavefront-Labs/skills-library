---
id: social-sciences.education-research.comparative-education-research.analysing-pisa-and-timss-with-plausible-values
name: analysing-pisa-and-timss-with-plausible-values
category: social-sciences
field: education-research
product: comparative-education-research
tags: [comparative-education-research, comparative-education, international-education, pisa, timss, pirls, talis, iea, oecd, international-large-scale-assessment, ilsa, plausible-values, replicate-weights, brr, fay-adjustment, jackknife, sampling-weights, idb-analyzer, intsvy, edsurvey, repest, bifiesurvey, rubins-rules, measurement-invariance, cross-cultural-validity, attitude-achievement-paradox, response-styles, anchoring-vignettes, multilevel]
level: advanced
status: draft
description: "Analyse PISA/TIMSS/PIRLS data correctly: plausible values, final and replicate weights, proper software, invariance checks for questionnaire scales, limits of causal claims."
sources:
  - "OECD, PISA Data Analysis Manual (SPSS/SAS, 2nd ed., 2009) and current PISA Technical Reports"
  - "IEA, TIMSS/PIRLS User Guides for the International Database (per cycle)"
  - "Rutkowski, Gonzalez, Joncas & von Davier (2010), International large-scale assessment data, Educational Researcher"
  - "Kyllonen & Bertling (2014), on the attitude-achievement paradox and anchoring vignettes"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Analysing PISA and TIMSS with plausible values

**Goal:** use international large-scale assessment (ILSA) data to compare education
systems or study within-country relationships, *without* the technical errors that make
many secondary analyses wrong — and with appropriate caution about cross-cultural
comparability.

## 1. Know the data structure
- **Complex samples**: schools sampled with probability proportional to size, then
  students (PISA: 15-year-olds; TIMSS: grades 4 and 8 intact classes; PIRLS: grade 4).
  You must use the **final student weight** (PISA `W_FSTUWT`; TIMSS `TOTWGT` or a
  rescaled version — check the cycle's user guide).
- **Replicate weights** for standard errors: PISA uses 80 balanced repeated replication
  weights with Fay's adjustment (k = 0.5); TIMSS/PIRLS use jackknife repeated
  replication. Ordinary SEs from SPSS/Stata defaults are too small.
- **Plausible values (PVs)**: students answer only part of the item pool (rotated
  booklets), so achievement is given as several random draws from each student's
  posterior ability distribution — 10 PVs per domain in PISA since 2015 (5 earlier),
  5 in TIMSS/PIRLS. **Never average the PVs first** and never use just PV1 for SEs.

## 2. The correct computation
For any statistic (mean, regression coefficient, percentage):
1. Compute it with the final weight for each PV separately; the estimate is the
   average across PVs.
2. Sampling variance: for each PV, recompute with each replicate weight, apply the
   BRR/jackknife formula; average across PVs.
3. Imputation variance: variance of the estimate across PVs × (1 + 1/M).
4. Total SE = √(sampling + imputation variance) — Rubin's rules.

**Use software that does this:** IEA IDB Analyzer (free, generates SPSS/SAS code), R
`intsvy`, `EdSurvey` (NCES; handles PVs and weights for many ILSAs), `BIFIEsurvey`,
Stata `repest` or `pv`. Verify one published table (e.g. a country mean and SE in the
international report) before going further.

## 3. Multilevel and causal analysis
- Multilevel models need weights scaled at both levels (student and school) — supported
  in Mplus, `WeMix` (R), `BIFIEsurvey`; run per PV and combine.
- ILSAs are **cross-sectional and observational**: country-level correlations
  ("countries with more homework score higher") are ecological and confounded. For
  causal questions use within-country designs (age/grade discontinuities in TIMSS,
  policy changes across cycles in difference-in-differences, country fixed effects
  across multiple cycles) and say what assumptions you make.
- Trend comparisons need the official **link/trend** scales; mode change (paper → computer
  in PISA 2015) is a known break to discuss.

## 4. Cross-cultural validity of measures
- Achievement scales are linked internationally by design, but **questionnaire scales**
  (motivation, self-efficacy, teacher support) may not be comparable across countries.
  Test **measurement invariance** (multi-group CFA: configural → metric → scalar, or
  alignment optimisation for many groups) before comparing means.
- **Attitude–achievement paradox**: within countries, liking maths correlates positively
  with scores; across countries, high-scoring systems often report lower liking — partly
  response styles and reference-group effects. Anchoring vignettes and forced-choice items
  have been used to address this.
- Check translations and national adaptations in the technical report.

## Gotchas
- Excluded/ineligible populations differ by country (special schools, out-of-school
  15-year-olds); coverage indices are in the technical report.
- Country rankings: differences between neighbours are often not significant; report SEs.
- Merging student, school and teacher files: TIMSS teacher data link via class and are
  not a teacher sample — use student-weighted analyses.
- Uncertain: weight variable names and replicate methods change between cycles; always
  read the user guide for the specific cycle.

## Verify
- [ ] Final weights used; SEs from replicate weights.
- [ ] All PVs used with Rubin's rules; no PV averaging.
- [ ] One published estimate reproduced exactly (mean and SE).
- [ ] Measurement invariance tested before cross-country questionnaire comparisons.
- [ ] Causal language matches the design; ecological inferences flagged.
