---
id: social-sciences.demography.population-projection.cohort-component-projection-and-assumption-setting
name: cohort-component-projection-and-assumption-setting
category: social-sciences
field: demography
product: population-projection
tags: [population-projection, demography, cohort-component-method, ccm, leslie-matrix, base-population, survivorship-ratios, sx, fertility-assumptions, mortality-assumptions, migration-assumptions, net-migration, projection-variants, high-low-variants, probabilistic-projection, bayesian-projection, bayespop, bayestfr, bayeslife, un-wpp, world-population-prospects, small-area-projection, hamilton-perry, cohort-change-ratios, sex-ratio-at-birth, scenario, ons-projections]
level: practitioner
status: draft
description: "Project population by age and sex with the cohort-component method: base population, survival, fertility and migration assumptions, variants and probabilistic projection."
sources:
  - https://arxiv.org/pdf/1405.4708
  - https://archive.ourworldindata.org/20260415-144825/grapher/sex-ratio-at-birth.html
  - https://cran.r-project.org/web/packages/bayesPop/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cohort-component projection and assumption setting

**Goal:** project population size and age–sex structure forward in a way that is
transparent about its assumptions and honest about uncertainty.

## 1. Inputs
- **Base population** by single or 5-year age and sex at the jump-off date, adjusted
  for census undercount and moved to the projection's reference date.
- **Mortality:** age–sex survivorship ratios from a life table — 5Sx = 5L(x+5) / 5Lx
  (for the open interval use T(x+5)/Tx). Newborn survival from births to age 0–4 =
  5L0 / (5·l0).
- **Fertility:** age-specific fertility rates (ASFR) for women 15–49; sex ratio at birth
  (~105 males per 100 females in most populations, the UN WPP expected value, higher where sex selection occurs).
- **Migration:** net migrants (or in- and out-flows) by age and sex — the weakest input
  almost everywhere.

## 2. The projection step (5-year steps, 5-year age groups)
For each sex:
1. **Survive** each cohort forward: P(x+5, t+5) = P(x, t) · 5Sx. Open interval A+:
   P(A+, t+5) = P(A−5, t)·S(A−5) + P(A+, t)·S(A+), with S(A+) = T(A+5)/T(A).
2. **Births** over the step: sum over ages of ASFR × average number of women in that age
   group over the step (mean of start and end female populations) × 5.
3. Split births by sex ratio at birth; survive them into age 0–4.
4. **Add migrants** — commonly half at the start and half at the end of the step (or
   apply mid-period with half-step survival).
In matrix form this is a **Leslie matrix** projection (plus migration vector).
Tools: R `bayesPop` / `demogR` (Leslie matrices), Excel templates (e.g. US Census Bureau's tools; RUP),
Spectrum/DemProj for national planning.

## 3. Setting assumptions
- **Fertility:** extrapolate recent TFR trends towards a long-run target (many offices
  assume ~1.4–1.9 for low-fertility countries); hold the age schedule's shape or shift
  mean age at childbearing gradually.
- **Mortality:** project improvement rates by age (e.g. Lee–Carter, or targeted annual
  improvement such as 1–1.5%) — see social-sciences.demography.mortality-analysis.
- **Migration:** use recent averages, policy scenarios, or model age profiles
  (Rogers–Castro). Expert judgement is unavoidable; document who decided and why.
- Write all assumptions in a single table with sources — users need it more than the outputs.

## 4. Variants and uncertainty
- **Deterministic variants:** high/medium/low fertility, zero migration, constant
  mortality. Simple but no probabilities attached, and low/high combinations aren't
  consistent bounds.
- **Probabilistic projection:** the UN WPP has used Bayesian hierarchical models since
  the 2015 revision (`bayesTFR`, `bayesLife`, `bayesPop`) to produce prediction intervals. Report 80% and
  95% intervals.
- Uncertainty grows fast for small areas and for age groups not yet born.

## 5. Small-area projections
Data on components are often missing locally. **Hamilton–Perry** uses cohort-change
ratios between two censuses (no separate migration estimate) — fast but unstable for
small or rapidly changing areas; constrain sub-areas to an independent total (controlling/raking).

## 6. Evaluate past performance
Compare earlier projections with later counts: mean absolute percentage error by
horizon. Most error historically comes from migration and fertility assumptions.

## Gotchas
- Forgetting to apply survival to migrants during the step, or double-counting them.
- Mixing calendar-period rates with cohort ages (Lexis-diagram mismatch).
- Projections are conditional "if-then" statements, not forecasts — say so in outputs.
- Uncertain: long-run TFR targets vary across agencies and revisions; cite the source.

## Verify
- [ ] Base population adjusted and dated correctly.
- [ ] Survivorship from life table Lx, including births and open interval.
- [ ] Projection reproduces the base-to-next-census change when back-tested.
- [ ] Assumption table with sources and rationale published.
- [ ] Uncertainty shown (variants or probabilistic intervals).
