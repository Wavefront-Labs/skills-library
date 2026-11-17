---
id: social-sciences.demography.demographic-rates-life-tables.building-period-life-tables-and-standardising-rates
name: building-period-life-tables-and-standardising-rates
category: social-sciences
field: demography
product: demographic-rates-life-tables
tags: [demographic-rates-life-tables, demography, life-table, period-life-table, abridged-life-table, life-expectancy, e0, mx, qx, lx, dx, nlx, tx, ax, person-years, exposure, occurrence-exposure-rate, crude-death-rate, age-specific-rates, direct-standardisation, indirect-standardisation, smr, standard-population, kitagawa-decomposition, arriaga-decomposition, chiang, demogr, demotools, human-mortality-database, hmd]
level: practitioner
status: gated
description: "Compute occurrence-exposure rates, build an abridged period life table from mx to e0, age-standardise rates and decompose differences (Kitagawa, Arriaga)."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building period life tables and standardising rates

**Goal:** turn deaths and population counts into age-specific rates, life expectancy
and comparisons that aren't distorted by differing age structures.

## 1. Rates: events over person-years
- Age-specific death rate: nMx = deaths aged x to x+n / person-years lived at x to x+n.
- Person-years ≈ mid-year population × years in the period (or average of start/end
  populations). For a 3-year average, use 3 × mid-period population.
- Numerator and denominator must cover the **same population, ages and period** —
  e.g. registered deaths of residents vs a census that counts by usual residence.
- Crude rates mix rate and age structure; never compare crude death rates across
  populations with different ages.

## 2. Abridged period life table (ages 0, 1–4, 5–9, … 85+)
Columns, for each age group [x, x+n):
1. **nax** — average years lived in the interval by those dying in it. Use n/2 for most
   ages (gated: unconfirmed, source is paywalled or blocked); for age 0 and 1–4 use Coale–Demeny or Andreev–Kingkade formulas (infant ax is
   much less than 0.5, often ~0.1–0.3 depending on mortality level (gated: unconfirmed, source is paywalled or blocked)).
2. **nqx** = n·nMx / (1 + (n − nax)·nMx) — probability of dying in the interval (algebraically inverted from nLx and checked numerically on 1,000 random cases). Set the
   open interval q = 1.
3. **lx** — survivors from radix l0 = 100,000: l(x+n) = lx·(1 − nqx).
4. **ndx** = lx − l(x+n).
5. **nLx** = n·l(x+n) + nax·ndx; open interval: L(∞) = l(x)/M(∞).
6. **Tx** = sum of nLx from x upward.
7. **ex** = Tx / lx. e0 is period life expectancy at birth.
Tools: R `demography`, `DemoTools` (lt_abridged), `LifeTables`; spreadsheet works for learning.

**Interpretation:** period e0 is the mean age at death of a hypothetical cohort
experiencing this year's rates throughout life — not a forecast for anyone born now.

## 3. Standardisation
- **Direct:** apply each population's age-specific rates to a common standard
  population (e.g. WHO World Standard Population 2000–2025 (Ahmad et al. 2001, confirmed); WHO has since published a revised standard population in a Global Health Estimates note, seen only in search results here, so check the current one; European Standard Population 2013 (Eurostat, confirmed); or one of the
  populations compared). Report the standard — results depend on it.
- **Indirect:** apply standard rates to the study population's age structure to get
  expected deaths; SMR = observed / expected. Use when age-specific rates in the study
  population are unstable (small numbers). SMRs from different study populations
  shouldn't be compared with each other directly.

## 4. Decomposition
- **Kitagawa:** splits a difference in crude rates into a rate effect and a composition
  (age-structure) effect.
- **Arriaga:** splits a difference in e0 into contributions from each age group (and
  by cause, if cause-specific rates are allocated proportionally). Contributions sum
  exactly to the gap. Implementations exist in `DemoDecomp` (R) or straightforward to code.

## 5. Data sources
Human Mortality Database (HMD) for high-quality national series; UN World Population
Prospects for estimates; national statistical offices for small areas.

## Gotchas
- Small populations: rates at older ages jump around — aggregate years or smooth, and
  give CIs (Chiang's variance formula (gated: unconfirmed, source is paywalled or blocked), or simulation).
- Age heaping and age misreporting at old ages inflate e85+; check data quality.
- The open age interval choice (85+ vs 100+) changes e0 slightly and older-age ex more.
- Uncertain: nax rules of thumb differ by source; state which you used.

## Verify
- [ ] Numerator and denominator cover identical populations and periods.
- [ ] Infant/child nax set from a named rule, open interval closed with 1/M.
- [ ] lx starts at the radix and declines monotonically; ex reasonable vs published HMD/UN values.
- [ ] Standard population named; SMRs not cross-compared.
- [ ] Decomposition contributions sum to the total difference.
