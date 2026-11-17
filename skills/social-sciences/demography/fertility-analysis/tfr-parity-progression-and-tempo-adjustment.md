---
id: social-sciences.demography.fertility-analysis.tfr-parity-progression-and-tempo-adjustment
name: tfr-parity-progression-and-tempo-adjustment
category: social-sciences
field: demography
product: fertility-analysis
tags: [fertility-analysis, fertility, demography, tfr, total-fertility-rate, asfr, age-specific-fertility-rate, gfr, crude-birth-rate, completed-cohort-fertility, ccf, parity, parity-progression-ratios, ppr, tempo-effect, quantum, tempo-adjustment, bongaarts-feeney, adjusted-tfr, mean-age-at-childbearing, birth-history, dhs, own-children-method, proximate-determinants, human-fertility-database, hfd, birth-interval, event-history-analysis]
level: practitioner
status: draft
description: "Measure fertility properly: ASFRs and TFR from births or birth histories, completed cohort fertility, parity progression ratios and Bongaarts-Feeney tempo adjustment."
sources:
  - https://cran.r-project.org/web/packages/DHS.rates/refman/DHS.rates.html
  - https://ideas.repec.org/c/boc/bocode/s457766.html
  - https://www.demographic-research.org/volumes/vol28/38/28-38.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TFR, parity progression and tempo adjustment

**Goal:** describe fertility levels and change with measures that separate how many
children people have (quantum) from when they have them (tempo).

## 1. Basic period measures
- **ASFR** for age group x to x+5: births to women aged x–x+5 / woman-years lived at those ages.
- **TFR** = 5 × Σ ASFR (5-year groups, 15–49) — average children per woman if she
  experienced the period's rates through her reproductive life. ~2.1 is replacement
  in low-mortality settings (higher where child mortality is high).
- **Mean age at childbearing (MAC)**: ASFR-weighted mean of age-group midpoints.
- Crude birth rate and general fertility rate depend on age structure — avoid for comparisons.

## 2. From birth histories (DHS and similar)
Full birth histories give each woman's children's dates of birth. Compute ASFRs for the
3 or 5 years before the survey by allocating births and exposure (woman-months) to
age groups and periods — the DHS standard TFR uses the 3 years preceding the
interview. In R, `DHS.rates::fert()` implements this (its default fertility period is 36 months, i.e. 3 years); Stata users often use `tfr2` (Schoumaker 2013, `ssc install tfr2`, whose defaults are designed to reproduce DHS reports).
Watch for **displacement of births** (interviewers shifting births out of the window that
triggers the long health module) and omission of dead children in older periods.
Use the survey weights and cluster design for SEs (jackknife in DHS reports).

## 3. Cohort measures
**Completed cohort fertility (CCF):** mean children ever born to women who have
reached ~45–50. Not distorted by timing — but only available for older cohorts.
Human Fertility Database (HFD) provides harmonised period and cohort series for
many countries.

## 4. Parity
- **Parity progression ratios (PPR):** proportion of women at parity i who go on to have
  an (i+1)th birth (a0 = proportion ever having a child, a1 = share of mothers having
  a second, …). Shows where fertility decline happens (more childlessness vs fewer
  third births).
- **Parity-specific, duration-based rates** from event-history models (time since last
  birth) avoid some period distortions.

## 5. Tempo and quantum
When the mean age at birth rises, period TFR falls even if eventual family size is
unchanged (births are postponed out of the period). **Bongaarts–Feeney (1998)**:
- For each birth order i: adjusted TFRᵢ′ = TFRᵢ / (1 − rᵢ), where rᵢ is the annual change
  in mean age at birth of order i (estimated as the difference between successive years,
  often averaged over neighbouring years).
- Adjusted TFR = Σ TFRᵢ′.
Requires birth-order-specific rates. The method assumes the tempo shift affects all
ages equally in a year; results are noisy year to year — smooth or use 3-year
averages. Alternatives: Kohler–Ortega (2002) tempo-adjusted parity progression measures, and simply comparing with
CCF. Tempo-adjusted TFR is an indicator, not a forecast of cohort fertility.

## 6. Proximate determinants
Bongaarts' framework decomposes fertility below its biological maximum into marriage/
union, contraception, postpartum infecundability (breastfeeding) and abortion indices —
useful in high-fertility settings.

## 7. Indirect estimation
Without registration or birth histories: own-children method from census
household rosters; Brass P/F ratio comparing children ever born with recent births.
See social-sciences.demography.census-survey-data.

## Gotchas
- A falling TFR during postponement doesn't necessarily mean smaller families.
- Small samples by single year of age give jumpy ASFRs — aggregate.
- Registration data may record births by mother's residence at birth vs current; align with the denominator.
- DHS TFR window: 3 years by default in `DHS.rates::fert()`; imputation of dates differs by survey phase, so check the DHS Guide to Statistics for yours.

## Verify
- [ ] Numerator births and denominator woman-years cover the same ages and period.
- [ ] Survey TFR uses weights and design-based SEs.
- [ ] Period TFR read alongside MAC trend and CCF where available.
- [ ] Tempo adjustment uses order-specific rates and smoothed change in mean age.
- [ ] Data-quality issues (displacement, omission) checked.
