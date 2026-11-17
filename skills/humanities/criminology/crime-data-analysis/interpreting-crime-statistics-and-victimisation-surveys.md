---
id: humanities.criminology.crime-data-analysis.interpreting-crime-statistics-and-victimisation-surveys
name: interpreting-crime-statistics-and-victimisation-surveys
category: humanities
field: criminology
product: crime-data-analysis
tags: [criminology, crime-data, crime-statistics, crime-trends, police-recorded-crime, official-statistics, ucr, nibrs, fbi-crime-data, ncvs, crime-survey-for-england-and-wales, csew, victimisation-survey, victimization-survey, dark-figure-of-crime, underreporting, recording-practices, crime-rate, per-100000, population-denominator, trend-analysis, regression-to-the-mean, homicide-data, seasonality, confidence-intervals, survey-weights, data-limitations, quantitative-criminology, crime-drop]
level: practitioner
status: draft
description: "Interpret crime trends for research: police-recorded data vs victimisation surveys, the dark figure, recording-rule changes, rates per population, and honest trend claims."
sources:
  - "Biderman, A. & Reiss, A. 'On exploring the dark figure of crime' (1967)"
  - "Office for National Statistics, user guide to crime statistics for England and Wales"
  - "US Bureau of Justice Statistics, NCVS methodology documentation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interpreting crime statistics and victimisation surveys

**Goal:** make defensible claims about how much crime there is and how it is changing —
for a paper, thesis or policy brief — knowing what each data source measures and where
it misleads.

## 1. Know your two main source types
- **Police-recorded (official) data** — offences reported to and recorded by police. US:
  the FBI's UCR, replaced by NIBRS as the national standard from 2021; England and Wales:
  police recorded crime published by ONS. Strong for serious, well-reported offences
  (homicide, vehicle theft) and for local detail; weak for anything people don't report.
- **Victimisation surveys** — household samples asked about crimes they experienced,
  reported or not. US: NCVS (BJS); England and Wales: the Crime Survey for England and
  Wales (CSEW). They capture the **dark figure** (unreported crime) but miss crimes
  without an individual victim (drug offences, fraud against businesses in some designs),
  homicide, and people outside households (homeless, institutions).
Use both: they triangulate. When they diverge, explain why rather than picking the one
that suits your argument.

## 2. Check for artefacts before claiming a trend
- **Recording-rule changes** — new counting rules, audits, or definitional changes create
  jumps that aren't real (e.g. ONS has flagged police recording improvements as inflating
  recorded violence in some years). *Specific year-by-year breaks: check the publisher's
  user guide.*
- **System transitions** — the UCR→NIBRS switch left gaps in US national estimates
  because many agencies didn't report in the transition year.
- **Reporting behaviour** — awareness campaigns (e.g. on domestic abuse or sexual
  offences) can raise reports while victimisation is flat or falling.
- **Enforcement-driven offences** — drug and weapons-possession counts mostly reflect
  police activity.
- **Coverage** — how many agencies or areas reported in each year?

## 3. Use rates, not counts
Convert to rates per 100,000 population (or per 1,000 households for surveys). Use the
right denominator: residents, but sometimes daytime population, vehicles, or households.
Small areas produce unstable rates — combine years or use confidence intervals.

## 4. Treat survey estimates as estimates
Surveys have sampling error. Report confidence intervals; check whether a change is
statistically significant (publishers usually mark this). Use the survey weights and
the design variables provided; unweighted counts are wrong.

## 5. Make honest trend claims
- Look at long runs (10+ years) before short ones; one year's change is noise for many
  offence types, especially rare ones like homicide in small areas.
- Watch **regression to the mean**: an area chosen because last year was unusually high
  will often fall regardless of policy.
- Account for seasonality in monthly data.
- Compare with similar places (synthetic or matched comparisons) before attributing
  changes to a policy.
- Separate "crime fell" from "reported crime fell".

## 6. International comparison
Legal definitions differ (what counts as burglary or assault), as do recording practices.
Prefer homicide (most comparable, though still imperfect) or standardised instruments such
as the International Crime Victims Survey, and say how comparable your figures are.

## Gotchas
- Media figures often mix counts and rates or quote preliminary data later revised.
- "Crimes" vs "incidents" vs "victims" are different units — check which one a table uses.
- Clearance/detection rates measure police outcomes, not crime levels.
- Ethics: aggregated public data rarely raise consent issues, but microdata access
  carries usage conditions; follow the licence.

## Verify
- [ ] Both recorded and survey data were considered, with divergences explained.
- [ ] Recording changes, transitions and coverage were checked for each year used.
- [ ] Figures are rates with stated denominators.
- [ ] Survey estimates carry confidence intervals and use weights.
- [ ] Trend claims use long runs and comparisons, and consider regression to the mean.
- [ ] Units (crimes/incidents/victims) are consistent and stated.
