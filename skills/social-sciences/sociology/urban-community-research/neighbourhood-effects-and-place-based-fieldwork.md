---
id: social-sciences.sociology.urban-community-research.neighbourhood-effects-and-place-based-fieldwork
name: neighbourhood-effects-and-place-based-fieldwork
category: social-sciences
field: sociology
product: urban-community-research
tags: [urban-community-research, urban-sociology, community-studies, sociology, neighbourhood-effects, neighborhood-effects, contextual-effects, census-tracts, lsoa, maup, modifiable-areal-unit-problem, selection-bias, moving-to-opportunity, multilevel-models, segregation, dissimilarity-index, isolation-index, collective-efficacy, systematic-social-observation, sso, google-street-view, ethnography, community-case-study, spatial-inequality, gentrification, geocoding, gis, spatial-autocorrelation]
level: practitioner
status: draft
description: "Study neighbourhood effects and communities: define 'neighbourhood', link contextual data, handle selection bias, measure segregation and combine with place-based fieldwork."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Neighbourhood effects and place-based fieldwork

**Goal:** establish whether and how where people live shapes their outcomes, while
taking seriously that people choose (or are sorted into) where they live.

## 1. Define the neighbourhood
- Administrative units: US census tracts/block groups, UK LSOAs/MSOAs, etc. Convenient
  and linkable, but may not match lived neighbourhoods.
- Alternatives: ego-centred buffers (e.g. 400 m / 800 m around the home), resident-drawn
  maps, activity spaces from GPS.
- **MAUP (modifiable areal unit problem):** results change with the scale and boundaries
  chosen. Re-run key models at a second scale and report it.

## 2. Link contextual data
Geocode addresses (securely — addresses are identifying) and attach area measures:
concentrated disadvantage index (poverty, unemployment, single-parent households,
public assistance — Sampson's construct), residential stability, ethnic composition,
crime, amenities. Census data for different years may use different boundaries — use
official boundary crosswalks.

## 3. The selection problem
People with unobserved traits that affect outcomes choose neighbourhoods; naïve
regressions conflate sorting with effects. Strategies:
- **Experiments:** Moving to Opportunity (housing vouchers by lottery). Early results
  showed limited adult economic effects but later work found large gains for children
  who moved young (Chetty, Hendren & Katz 2016).
- **Quasi-experiments:** public-housing demolitions, random housing allocation, movers
  designs comparing siblings by age at move.
- **Fixed effects / sibling comparisons; propensity-score or marginal structural models**
  for time-varying exposure (Wodtke et al.) — duration of exposure matters.
- Be explicit that observational estimates are associations under stated assumptions.

## 4. Multilevel analysis
Individuals nested in neighbourhoods: random-intercept models (`lme4`), report the
intraclass correlation (often small, a few percent — small ICC doesn't mean small
effects of specific contextual variables). Need enough units (dozens+) and enough
people per unit for reliable neighbourhood-level measures; ecometrics (Raudenbush &
Sampson) assesses reliability of neighbourhood measures built from resident reports.

## 5. Segregation
- **Dissimilarity index D:** share of one group that would need to move to equalise
  distribution (0–1). **Isolation index:** exposure to own group. Both depend on unit size.
- Spatial versions and multigroup entropy (Theil's H) for more than two groups.
- R: `segregation` package; Python: `segregation` (PySAL).

## 6. Place-based fieldwork
- **Systematic social observation (SSO):** structured coding of street segments
  (litter, graffiti, people, physical disorder) by trained raters or via Google Street
  View imagery — record image date, test rater reliability.
- **Community case studies / ethnography:** long-term presence, mapping institutions,
  interviews with residents and gatekeepers; attend to how residents themselves
  define boundaries and reputations.
- Combine: quantitative patterns identify places to study; fieldwork explains mechanisms
  (collective efficacy, institutional resources, stigma).

## Gotchas
- Spatial autocorrelation violates independence — check Moran's I on residuals.
- "Neighbourhood effect" may be a school, policing or labour-market effect — specify mechanisms.
- Publishing identifiable small-area details (with quotes) can expose participants.
- Uncertain: effect sizes from MTO and related studies are debated; cite specific estimates.

## Verify
- [ ] Neighbourhood definition justified and a second scale tested.
- [ ] Boundary changes over time handled with crosswalks.
- [ ] Selection addressed by design or assumptions stated explicitly.
- [ ] Segregation measure named with unit of analysis.
- [ ] Fieldwork data protect places and people from identification.
