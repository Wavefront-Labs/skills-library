---
id: social-sciences.demography.census-survey-data.ipums-dhs-microdata-quality-checks-and-indirect-estimation
name: ipums-dhs-microdata-quality-checks-and-indirect-estimation
category: social-sciences
field: demography
product: census-survey-data
tags: [census-survey-data, demography, census, microdata, ipums, ipums-international, ipums-usa, ipums-dhs, dhs, demographic-and-health-surveys, mics, survey-weights, perwt, hhwt, data-quality, age-heaping, whipple-index, myers-index, sex-ratio, age-ratio, un-joint-score, post-enumeration-survey, coverage, indirect-estimation, brass-method, children-ever-born, children-surviving, child-mortality, sibling-survival, demotools, model-life-tables]
level: practitioner
status: draft
description: "Work with census and DHS/IPUMS microdata: extract and weight correctly, test data quality (age heaping, sex ratios), and apply Brass indirect estimation where data are thin."
sources:
  - https://github.com/timriffe/DemoTools
  - https://unstats.un.org/unsd/demographic-social/products/dyb/documents/dyb2023/Notes03a.pdf
  - https://dhsprogram.com/data/Guide-to-DHS-Statistics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Census and DHS/IPUMS microdata: quality checks and indirect estimation

**Goal:** get trustworthy demographic estimates from large census and survey
microdata, including settings where registration is incomplete and direct measures fail.

## 1. Getting the data
- **IPUMS** (USA, International, DHS, CPS…) harmonises variables across countries and
  years. Register, build an extract (samples × variables), download with the DDI codebook,
  read with R `ipumsr::read_ipums_micro()` (keeps labels). Cite each sample as required.
- **DHS Program:** request access per country/survey with a short project description;
  datasets come as recode files (IR women, MR men, KR children, BR births, HR/PR household).
  The DHS Guide to Statistics documents how every indicator is computed.
- IPUMS-International samples are usually 10% or less of the census — subnational
  estimates for small areas can be noisy.

## 2. Weights and design
- IPUMS: `PERWT` for person-level, `HHWT` for household-level estimates. Many census
  samples are self-weighting but not all.
- DHS: weight `v005 / 1e6` (women), with `v021` PSU and `v022`/`v023` strata for variance:
```r
des <- survey::svydesign(ids = ~v021, strata = ~v022, weights = ~I(v005/1e6), data = ir, nest = TRUE)
```
- Pooling several DHS surveys: weights are normalised within survey; de-normalise or
  rescale by population if you want population-representative pooled estimates.

## 3. Data-quality assessment
Do these before analysis:
- **Age heaping:** Whipple's index (ages ending in 0 and 5 within ages 23–62, times 5; 100 = no heaping,
  500 = all heaped; UN bands: <105 highly accurate, 105–109.9 fairly accurate, 110–124.9 approximate, 125–174.9 rough, 175+ very rough; `DemoTools` defaults to ages 25–65) and Myers' blended index (all terminal digits; 0 = none).
- **Sex ratios by age:** abrupt swings between adjacent groups signal misreporting or
  differential undercount (young adult men often).
- **Age ratios** and the **UN age–sex accuracy (joint) score**.
- **Coverage:** check post-enumeration survey results; compare cohorts across censuses
  (cohort survival should be smooth, adjusted for migration and mortality).
- DHS: incompleteness of dates (imputed dates flags), displacement of births out of the
  5-year window, interviewer effects. `DemoTools` in R implements many checks and
  smoothing methods (e.g. `check_heaping_whipple`, `check_heaping_myers`, both exported).

## 4. Indirect estimation (Brass family)
Where vital registration is incomplete, census/survey questions yield estimates:
- **Child mortality from children ever born / surviving** by mother's age group (15–19 …
  45–49): proportions dead → q(x) via multipliers (Trussell variant), each age group
  giving q(1), q(2), q(3), q(5)… with a reference date some years before the survey.
  Pick the model life table family (Coale–Demeny West, UN) that fits the population.
- **Fertility:** Brass P/F ratio compares cumulated current fertility (F) with average
  parity (P) to adjust the level of reported recent births.
- **Adult mortality:** orphanhood and sibling-survival methods; incomplete-registration
  methods (growth balance, synthetic extinct generations) to estimate death registration
  completeness.
- Manuals: UN Manual X; IUSSP *Tools for Demographic Estimation* (free online) with spreadsheets.

## 5. Report quality alongside results
State the source, sample fraction, weight, quality indices, and which adjustments were applied.

## Gotchas
- Younger-mother groups (15–19) give biased child-mortality estimates (first births are
  higher-risk) — usually discarded.
- Harmonised IPUMS variables may lose detail; check the unharmonised source variable
  for your question.
- Whipple thresholds above are the UN bands; Myers' index runs 0 (none) to 90 (all ages end in one digit).

## Verify
- [ ] Correct weight and design variables; pooled weights handled.
- [ ] Whipple/Myers, sex and age ratios computed and reported.
- [ ] Coverage and date-imputation issues checked.
- [ ] Indirect estimates use a justified model life table family and reference dates.
- [ ] Results compared with an independent source (UN WPP, previous census).
