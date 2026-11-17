---
id: social-sciences.demography.migration-studies.estimating-migration-flows-stocks-and-residual-net-migration
name: estimating-migration-flows-stocks-and-residual-net-migration
category: social-sciences
field: demography
product: migration-studies
tags: [migration-studies, migration, demography, international-migration, internal-migration, migration-flows, migrant-stocks, net-migration, residual-method, demographic-balancing-equation, vital-statistics-method, census-survival-ratio, place-of-birth, previous-residence, one-year-migration, five-year-migration, transition-data, movement-data, un-desa-migrant-stock, imem, bilateral-flows, flow-from-stocks, rogers-castro, model-migration-schedule, migration-surveys, administrative-data, definitions, usual-residence]
level: practitioner
status: draft
description: "Measure migration: distinguish flows from stocks, reconcile sending and receiving data, estimate net migration by residual methods and use Rogers-Castro age schedules."
sources:
  - https://unstats.un.org/unsd/demographic-social/meetings/2025/migration-wk-sadc-20250317/02.UNSD-RecommendationsOverview.pdf
  - https://www.cpc.ac.uk/projects/13/Integrated_Modelling_of_European_Migration_IMEM_
  - https://cran.r-project.org/web/packages/rcbayes/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Estimating migration flows, stocks and residual net migration

**Goal:** produce migration numbers that are consistent in definition, time window
and population, and know which of several imperfect sources to trust for what.

## 1. Stocks vs flows, and definitions
- **Stock:** people at a point in time with a migrant attribute — foreign-born (place of
  birth) or foreign citizens. The two differ (naturalisation, births abroad to citizens).
- **Flow:** moves during a period. UN recommendations (1998) define a long-term international
  migrant by change of usual residence for at least 12 months (short-term: 3 to under 12 months; a revision is under way), but countries use
  different durations (some 3 months, some intention-based) — so country A's
  emigration rarely matches country B's recorded immigration.
- Internal migration: moves across a defined boundary (region, municipality). Rates
  depend on the size and shape of units — not comparable across systems without care.

## 2. Sources and what they capture
| Source | Gives | Pitfalls |
|---|---|---|
| Census place of birth | Lifetime migrant stock | No timing; return migrants invisible |
| Census residence 1 or 5 years ago | **Transitions** (where then vs now) | Misses multiple moves, deaths, children born in window |
| Population registers | **Movement** events | Under-registration of emigration (people don't deregister) |
| Border/admin data (visas, permits) | Entries by category | Flows of non-migrants; duration unknown |
| Surveys (LFS, DHS, specialist) | Characteristics, intentions | Small n for flows; emigrants absent by design |
Transition (5-year) counts are much smaller than movement counts — don't mix them.

## 3. Residual (indirect) methods
**Demographic balancing equation:** P(t+n) = P(t) + B − D + I − E
→ net migration = P(t+n) − P(t) − (B − D).
- Works at national or regional level when births/deaths are well registered.
- The residual absorbs **all errors**: census coverage changes between counts appear as
  migration. Adjust both censuses for coverage first.
**Census survival ratio method** (by age): expected population at t+n = population at t
× national census survival ratio (assumes the nation is closed or nearly so); net
migration by age = observed − expected. Good for subnational age profiles of net
migration; sensitive to differential coverage by age.

## 4. Estimating bilateral flows
Where flows aren't measured: estimate from changes in bilateral stock tables (Abel &
Sander's (Science 2014) flow-from-stock methods); harmonise sending and receiving country reports with
models such as the Integrated Modelling of European Migration (IMEM, Bayesian).
Outputs are estimates with wide uncertainty — present ranges.

## 5. Age patterns
Migration peaks in young adulthood (early–mid 20s), has a child component tied to
parents, sometimes a retirement peak. The **Rogers–Castro model migration schedule**
(7–13 parameters) smooths and fills age profiles when data are sparse; fitting tools
exist in R (e.g. `rcbayes`, `DemoTools`). Use it for projections' migration age distribution.

## 6. Analysis
Rates need a population at risk: out-migration rate uses origin population; in-migration
"rates" over destination population are not true rates. Gravity models and Poisson/
negative-binomial regressions on origin–destination counts (with origin and destination
fixed effects) for determinants.

## Gotchas
- Net migration of zero can hide large gross flows in both directions.
- Emigration is the hardest component everywhere — use receiving-country data ("mirror
  statistics") where possible.
- Irregular migrants are under-covered by most sources; say what your figures exclude.
- IMEM (2009-12 project, Raymer, Wiśniowski, Bijak, Forster, Smith, Abel) produced EU/EFTA flow estimates for 2002-2008; `rcbayes` is a CRAN package for Bayesian Rogers-Castro schedules. Check current releases.

## Verify
- [ ] Migrant definition (birth vs citizenship; duration rule) stated.
- [ ] Flow type (transition vs movement) and time window explicit.
- [ ] Residual estimates use coverage-adjusted censuses; errors acknowledged.
- [ ] Bilateral or modelled estimates come with uncertainty ranges.
- [ ] Rates use an appropriate population at risk.
