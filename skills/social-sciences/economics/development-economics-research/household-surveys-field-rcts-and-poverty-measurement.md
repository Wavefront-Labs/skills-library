---
id: social-sciences.economics.development-economics-research.household-surveys-field-rcts-and-poverty-measurement
name: household-surveys-field-rcts-and-poverty-measurement
category: social-sciences
field: economics
product: development-economics-research
tags: [development-economics-research, development-economics, household-surveys, lsms, dhs, consumption-aggregate, poverty-measurement, poverty-line, fgt-indices, headcount-ratio, poverty-gap, ppp, international-poverty-line, field-rct, cluster-randomisation, baseline-survey, enumerators, capi, surveycto, odk, survey-solutions, back-checks, high-frequency-checks, attrition, tracking, j-pal, ipa, spillovers, general-equilibrium-effects, local-partners, pre-analysis-plan]
level: advanced
status: verified
description: "Do development-economics fieldwork: CAPI household surveys with data-quality checks, a consumption aggregate and FGT poverty measures, and field RCTs that handle clusters, spillovers and attrition."
sources: ["Deaton, The Analysis of Household Surveys (World Bank 1997; reissued 2019)", "Foster, Greer & Thorbecke (1984), Econometrica 52(3)", "Glennerster & Takavarasha, Running Randomized Evaluations (Princeton 2013)", "World Bank LSMS and DIME Analytics guidance (DIME Wiki)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Development economics fieldwork — surveys, poverty, field RCTs

**Goal:** data collected in low- and middle-income settings that is accurate enough to
measure welfare, and field experiments that survive real-world implementation.

## 1. Household survey design
- Start from existing instruments: World Bank **LSMS-ISA** modules, **DHS** questionnaires,
  national survey modules — adapt rather than invent, and keep codes comparable.
- Define the **household** (eats from the same pot, sleeps under the same roof for ≥ X of
  the last 12 months) and the respondent for each module (most knowledgeable member).
- Recall periods: food 7 days, frequent non-food 30 days, durables 12 months. Shorter
  recall is more accurate but noisier; changing recall periods breaks comparability with
  earlier rounds.
- Translate and back-translate; cognitive-test in each language.

## 2. Collecting it well
- **CAPI** platforms: SurveyCTO, ODK/KoboToolbox, World Bank Survey Solutions. Program
  constraints (ranges, consistency checks) and GPS/timestamps, with soft checks for
  unusual-but-possible values.
- Train enumerators for several days, including mock interviews and a field pilot;
  test them and drop weak performers.
- **High-frequency checks** daily: duplicates, survey duration outliers, skipped modules,
  enumerator-level distributions (an enumerator with no "don't knows" or very short
  interviews is a red flag). DIME Analytics' `iefieldkit` (github.com/worldbank/iefieldkit) and IPA's `ipacheck` (github.com/PovertyAction/high-frequency-checks) automate many.
- **Back-checks:** re-interview ~10–20% of respondents on stable questions with a separate
  team; compare by enumerator.
- Plan **tracking** for panels: phone numbers of relatives, GPS of the dwelling, landmarks.

## 3. Consumption aggregate and poverty
- Build per-capita (or per-adult-equivalent) consumption: food (purchased + own production
  + gifts, valued at local prices), non-food, **use value** of durables (not purchase price),
  imputed rent. Exclude lumpy one-off spending (weddings, health shocks) per your convention.
- Spatial price deflation (regional price indices) and temporal deflation within the
  fieldwork period.
- **Poverty line:** national cost-of-basic-needs line or the World Bank international line
  in PPP dollars (the international line and PPP base year get revised — check the current
  value before using; the World Bank's June 2025 update set the international line at $3.00 per person per day in 2021 PPPs, replacing $2.15 in 2017 PPPs).
- **FGT measures:** P_α = (1/N) Σ_{poor} ((z − y_i)/z)^α. α = 0 headcount, α = 1 poverty gap,
  α = 2 squared gap (severity). Use survey weights and design-based SEs.
- Consumption is usually preferred to income in agrarian settings (smoother, better reported).

## 4. Field RCT specifics
- Randomise at the level where spillovers stop (village, market) or design for spillovers
  explicitly: randomised saturation (vary share treated across clusters) lets you estimate them.
- Power with ICC from prior surveys; budget is usually dominated by clusters.
- Baseline survey before randomisation; stratify on baseline outcome and geography.
- Work with an implementing partner: write down who does what, how treatment will be
  monitored, and what happens if the partner changes the programme mid-way.
- **Attrition:** compare rates and baseline characteristics by arm; report Lee bounds if differential.
- **General-equilibrium effects** (prices, wages) can make small-scale effects unrepresentative
  of scale-up.
- Pre-analysis plan registered (AEA RCT Registry) before endline data.

## 5. Ethics and community
Community consent from leaders where customary, plus individual consent; respondent burden
(LSMS-style interviews can take hours — compensate time); data protection for GPS and
phone numbers. See social-sciences.social-research-methods.research-ethics-human-subjects.consent-risk-and-ethics-committee-applications.

## Gotchas
- Units: local measurement units (heaps, tins) need conversion factors collected by market surveys.
- Seasonality: comparing rounds in different seasons confounds treatment with harvest timing.
- Enumerator effects correlate with treatment if teams are assigned by area — randomise or cross teams.

## Verify
- [ ] Instruments adapted from standard modules; translated and piloted.
- [ ] Daily high-frequency checks and ≥10% back-checks running.
- [ ] Consumption aggregate documented, deflated spatially and temporally.
- [ ] Poverty line source and PPP vintage stated; FGT with design-based SEs.
- [ ] RCT handles spillovers, attrition and has a registered PAP.

*Checked 2026-10-19: FGT formula computed (y=50,80,100,150,300, z=100 gives P0=0.4, P1=0.14, P2=0.058); poverty line from the World Bank June 2025 factsheet; tool repositories and sites opened. Recall periods and back-check shares are common practice, not universal standards.*
