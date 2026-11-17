---
id: social-sciences.human-geography.population-migration-geography.segregation-indices-and-migration-flows
name: segregation-indices-and-migration-flows
category: social-sciences
field: human-geography
product: population-migration-geography
tags: [population-migration-geography, population-geography, migration, migration-flows, origin-destination-matrix, od-matrix, net-migration, migration-efficiency, gravity-model, flow-mapping, flowmap-blue, residential-segregation, index-of-dissimilarity, isolation-index, exposure-index, entropy-index, theil-h, spatial-segregation, checkerboard-problem, maup, segregation-python, oasisr, census-microdata, ipums, internal-migration, international-migration, spatial-demography]
level: practitioner
status: draft
description: "Measuring residential segregation (dissimilarity, isolation, entropy, spatial indices) and analysing origin-destination migration flows and net migration."
sources: ["Massey & Denton, 'The Dimensions of Residential Segregation' (1988)", "Reardon & O'Sullivan, 'Measures of Spatial Segregation' (2004)", "Rogerson, Statistical Methods for Geography", "Abel & Sander, 'Quantifying Global International Migration Flows' Science (2014)", "PySAL segregation package documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Segregation indices and migration flows

**Goal:** quantify how unevenly groups are distributed across a city or region, and
describe how people move between places — with measures whose quirks you understand.

## 1. Segregation: pick the dimension
Massey & Denton identified five dimensions (evenness, exposure, concentration,
centralisation, clustering). The two most used:

**Index of dissimilarity (D), evenness:**
D = ½ Σ | a_i/A − b_i/B | over areal units i.
Interpretation: share of either group that would need to move for an even distribution.
Rough conventions in US literature: <0.3 low, 0.3–0.6 moderate, >0.6 high.

**Isolation / exposure (P\*), exposure:**
Isolation = Σ (a_i/A)(a_i/t_i) — the average share of own-group in the area where a
group member lives. Depends on group size: a small group can be highly uneven yet
have low isolation. Report both D and P\*.

**Multigroup:** entropy-based **Theil's H** handles more than two groups; decomposes
into between/within regions.

## 2. Segregation gotchas
- **Unit dependency/MAUP:** finer units give higher D. Always state the unit (tract,
  block group, LSOA) and compare like with like.
- **Small-unit bias:** D is upwardly biased when unit populations are small, even
  under random allocation. Compare with a randomisation baseline or use bias-corrected
  versions.
- **Checkerboard problem:** aspatial indices ignore whether minority units adjoin
  each other. Use spatial versions (Reardon–O'Sullivan spatial H, or indices over
  egohoods/buffers at several radii).
- Group definitions (race/ethnicity categories, multi-race responses) change between
  censuses.
Tools: Python `segregation` (PySAL), R `OasisR` or `segregation` packages.

## 3. Migration flows
- Sources: census migration questions ("where did you live one/five years ago?"),
  population registers, administrative address changes, international estimates
  (UN DESA stocks; bilateral flow estimates such as Abel & Sander).
- **Transitions vs movements:** census 1- or 5-year questions record transitions;
  people who move and return, or die, are missed. Don't compare 1-year and 5-year
  rates directly.
- Build an **origin–destination (OD) matrix**. Diagonal = stayers or within-unit moves.
- Measures: gross in/out flows, **net migration** (in − out), **migration efficiency**
  (net ÷ gross ×100, how much churn redistributes population), crude migration rates
  per 1,000 population at risk.
- **Gravity/spatial interaction models:** flows ∝ populations, inverse to distance;
  fit as Poisson GLMs (handles zero flows; avoid log-OLS dropping zeros).

## 4. Mapping flows
Show only the largest flows (top N or above a threshold) or net flows; thousands of
lines are unreadable. Use curved, tapered or arrowed lines and order thin over thick.
Tools: flowmap.blue, QGIS (Flow Mapper / geometry generator), kepler.gl.

## 5. Privacy
Small OD cells can identify individuals; follow statistical disclosure control
(suppress or round small counts) before publishing.

## Verify
- [ ] Segregation measures named by dimension, with areal unit stated.
- [ ] Both an evenness and an exposure measure reported (or justified otherwise).
- [ ] Small-unit bias or spatial structure addressed.
- [ ] Migration data type (transition vs event) and interval stated.
- [ ] Flow maps filtered for legibility; small cells suppressed.
