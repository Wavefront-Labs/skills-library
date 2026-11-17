---
id: social-sciences.human-geography.urban-geography-research.measuring-gentrification-and-land-use-change
name: measuring-gentrification-and-land-use-change
category: social-sciences
field: human-geography
product: urban-geography-research
tags: [urban-geography-research, urban-geography, gentrification, displacement, neighbourhood-change, gentrification-index, freeman-method, census-tracts, longitudinal-tract-database, ltdb, nhgis, boundary-harmonisation, areal-interpolation, land-use-change, land-cover, parcel-data, assessor-data, building-permits, urban-form, density, morphology, osmnx, street-network, comparative-urbanism, eviction-data, airbnb, rent-data]
level: practitioner
status: draft
description: "Measuring neighbourhood change: census-based gentrification typologies, land-use change from parcels and imagery, boundary harmonisation and displacement evidence."
sources: ["Freeman, 'Displacement or Succession?' Urban Affairs Review (2005)", "Logan, Xu & Stults, 'Interpolating US Decennial Census Tract Data' (Longitudinal Tract Database, 2014)", "IPUMS NHGIS documentation", "Boeing, 'OSMnx' (2017)", "Lees, Slater & Wyly, Gentrification (2008)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Measuring gentrification and land-use change

**Goal:** identify which neighbourhoods changed, how, and with what consequences for
residents — with measures that survive scrutiny over definitions and boundaries.

## 1. Decide what you mean by "gentrification"
Definitions are contested: class upgrading, reinvestment, cultural change, displacement.
Write an operational definition with two parts:
1. **Eligibility** — the tract was low-income at time 1 (e.g. median household income
   below the metro median or a percentile; older housing stock).
2. **Change** — between time 1 and time 2 it shows above-metro growth in, e.g.,
   share with a bachelor's degree, median home value/rent, or professional occupations.
This mirrors approaches such as Freeman (2005); many variants exist and they classify
different tracts. Run at least two definitions and show where they disagree.

## 2. Harmonise boundaries over time
Tract boundaries change each census; comparing raw 2000 and 2020 tracts is wrong.
- US: use the **Longitudinal Tract Database (LTDB)** or **NHGIS** time series that
  interpolate to constant boundaries.
- Elsewhere: build crosswalks with **areal interpolation**, ideally population-weighted
  (using blocks or building footprints) rather than area-weighted.
- Inflation-adjust money values to one year's dollars.
- ACS 5-year estimates overlap in time — don't compare overlapping periods (e.g.
  2015–2019 vs 2017–2021) as if independent.

## 3. Displacement evidence
Census change shows composition, not *who left*. Better evidence:
- Longitudinal individual data (credit-panel, tax, or address-history data where
  accessible under agreement) to track out-movers and where they went.
- Eviction filings, court records, rent registries.
- Interviews with residents, landlords and organisers — qualitative work explains
  mechanisms and lived experience.
Remember that "exclusionary displacement" (people who can no longer move in) is
invisible in out-mover data.

## 4. Land-use and urban-form change
- **Parcel/assessor data:** land-use codes and building years over time; codes differ
  between counties and years — build a crosswalk.
- **Building permits and zoning changes** as leading indicators.
- **Remote sensing:** land-cover change (e.g. impervious surface) from Landsat/
  Sentinel-2 or national land-cover products; validate with sample points.
- **Urban form metrics:** density, building footprint coverage, street connectivity
  (intersection density, OSMnx network stats). OSM completeness varies by city.
- Platform data (short-term rental listings, rents scraped from listing sites) are
  biased samples; describe how collected and respect terms of service.

## 5. Comparative urbanism
Cross-city comparison needs comparable units and definitions; categories like
"gentrification" or "informality" travel imperfectly beyond North American/European
cities. Justify the comparison, or use relational comparison (connections between
cities) instead of variable-based matching.

## Verify
- [ ] Gentrification defined operationally; at least two definitions compared.
- [ ] Time-series data harmonised to constant boundaries; money inflation-adjusted.
- [ ] No overlapping ACS periods compared as independent.
- [ ] Displacement claims backed by mover-level or qualitative evidence, not composition alone.
- [ ] Land-use data crosswalked and imagery classifications validated.
