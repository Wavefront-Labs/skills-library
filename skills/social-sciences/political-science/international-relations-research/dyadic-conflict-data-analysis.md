---
id: social-sciences.political-science.international-relations-research.dyadic-conflict-data-analysis
name: dyadic-conflict-data-analysis
category: social-sciences
field: political-science
product: international-relations-research
tags: [international-relations-research, international-relations, ir, conflict-data, correlates-of-war, cow, mid, militarized-interstate-disputes, ucdp, ucdp-prio, acled, gdelt, dyad-year, directed-dyads, politically-relevant-dyads, democratic-peace, peace-years, cubic-splines, rare-events, logit, alliances, atop, trade-data, cow-trade, peacesciencer, eugene, ir-theory-testing, clustered-standard-errors]
level: advanced
status: draft
description: "Building and analysing dyad-year conflict data: COW/MID vs UCDP/ACLED, politically relevant dyads, peace-years splines, and interdependence pitfalls."
sources: ["Beck, Katz & Tucker, 'Taking Time Seriously' (1998)", "Carter & Signorino, 'Back to the Future: Modeling Time Dependence in Binary Data' (2010)", "Correlates of War Project documentation", "UCDP definitions and codebooks", "Miller, peacesciencer R package documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dyadic conflict data analysis

**Goal:** test an IR hypothesis (e.g. democratic peace, alliance deterrence, trade and
conflict) on country-pair data without the classic dyadic mistakes.

## 1. Pick the right conflict data — they measure different things
- **COW Militarized Interstate Disputes (MID):** threats, displays and uses of force
  between states, with hostility levels 1–5. Interstate, 1816 onward.
- **COW War data:** ≥1,000 battle deaths threshold.
- **UCDP/PRIO Armed Conflict:** ≥25 battle-related deaths per year with a state as a
  party; includes intrastate. UCDP GED gives geocoded events.
- **ACLED:** event-level political violence and protest, recent decades, uneven
  country coverage start dates.
- **GDELT/ICEWS** machine-coded events: huge, noisy, duplicate-prone.
Match the dataset definition to your concept; "conflict" in MIDs ≠ "conflict" in UCDP.

## 2. Build the dyad-year frame
- **Non-directed** dyads (A–B once per year) for "do they fight?"; **directed** dyads
  (A→B and B→A) for initiation questions.
- All-dyads data are overwhelmingly zero (e.g. Bolivia–Mongolia). Common restriction:
  **politically relevant dyads** (contiguous or including a major power). It changes
  results — report both.
- Tools: the `peacesciencer` R package assembles dyad-years with COW/MID, alliances
  (ATOP/COW), capabilities (CINC), democracy and distance; older work used EUGene.
- Code **onset**, not ongoing years, if the theory is about starting conflict; drop or
  flag continuation years.

## 3. Temporal dependence
Conflict is more likely in dyads that fought recently. Include **peace years** (years
since last dispute) with cubic splines (Beck-Katz-Tucker) or simply t, t², t³
(Carter–Signorino). Omitting this inflates confidence in slowly-changing variables.

## 4. Covariates and lags
Lag time-varying predictors (trade, regime type) by a year to reduce simultaneity.
Trade data (COW trade, IMF DOTS) have missing values that are not random — small/poor
states missing; never silently set missing trade to zero.

## 5. Estimation and inference
- Logit/probit with peace-year terms is standard; **rare-events** corrections
  (King–Zeng) when events are very scarce.
- Dyads are not independent: the same state appears in many dyads. Cluster standard
  errors on the dyad at minimum; consider multi-way clustering on both states.
- Report substantive effects (predicted probabilities) — a significant odds ratio on
  a 0.2% baseline may mean little.

## 6. Classic pitfalls
- Joint democracy vs "either democracy" codings give different answers; state your
  measure (often weak-link: the less democratic partner's score).
- Reverse causation: alliances form *because* of threats.
- Post-1990 coverage differences can drive trends.

*Uncertainty:* thresholds and coverage years as commonly documented; check the current
codebook versions you download.

## Verify
- [ ] Conflict dataset's definition matches the concept being tested.
- [ ] Dyad type (directed/non-directed) and sample restriction justified; robustness to all dyads shown.
- [ ] Onset vs ongoing coded explicitly.
- [ ] Peace-years splines or cubic polynomial included.
- [ ] Standard errors clustered; predicted probabilities reported.
