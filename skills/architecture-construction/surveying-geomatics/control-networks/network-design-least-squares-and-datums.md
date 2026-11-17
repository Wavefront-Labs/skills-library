---
id: architecture-construction.surveying-geomatics.control-networks.network-design-least-squares-and-datums
name: network-design-least-squares-and-datums
category: architecture-construction
field: surveying-geomatics
product: control-networks
tags: [control-networks, survey-control, control-survey, network-design, least-squares, least-squares-adjustment, network-adjustment, redundancy, degrees-of-freedom, standard-error, error-ellipse, chi-square-test, variance-factor, outliers, blunder-detection, minimally-constrained, fully-constrained, datum, projection, scale-factor, combined-scale-factor, ground-grid, traverse, star-net, geomatics, surveying]
level: advanced
status: draft
description: "Design a survey control network with redundancy, run a minimally then fully constrained least-squares adjustment, read the statistics, and handle datum, projection and scale factor correctly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Control networks — design, least squares and datums

**Goal:** a set of control marks with known coordinates and **known uncertainty**, so
every later survey and setting-out task inherits a defensible framework.

## 1. Network design
- **Geometry:** marks spread around and through the site, intervisible where total
  stations will use them, out of the construction footprint, on stable ground.
- **Redundancy:** observe more than the minimum. Closed traverses, braced quadrilaterals,
  cross-ties, and GNSS baselines forming loops. Redundancy is what lets you find
  blunders; an open traverse has none.
- **Connection:** tie to at least two (preferably three or more) higher-order or
  national control marks/CORS, so the datum is defined and checkable.
- **Monumentation:** durable marks (e.g. concrete-set pins, survey nails in sound
  concrete), each with a description and witness diagram.

## 2. Observations
- Total station: both faces, multiple rounds of angles, reciprocal distances, measured
  instrument and target heights, met corrections applied.
- GNSS static: session lengths suited to baseline length, independent (not trivial)
  baselines, repeated sessions in different satellite geometry.
- Levelling for heights where precision demands (see digital-level skill).
- Record realistic a-priori standard errors for each observation type (instrument
  spec + centring errors). The adjustment's statistics are only as honest as these.

## 3. Adjustment workflow (e.g. STAR*NET, Trimble Business Center, Leica Infinity, Columbus)
1. **Minimally constrained** adjustment — fix just enough to define the datum (one
   point and one bearing in 2D, or one point in 3D GNSS). This tests the internal
   consistency of *your* observations without being distorted by control errors.
2. Read the statistics:
   - **Variance factor / reference factor** near 1 → your a-priori errors match reality.
     Much greater than 1 → errors are underestimated or there's a blunder.
   - **Chi-square test** passed/failed.
   - **Standardised residuals**: flag anything beyond about 3. Investigate the largest
     first — fix or remove one at a time and re-run.
3. **Fully constrained** adjustment to all accepted control. If the variance factor jumps
   compared with minimally constrained, the control marks don't agree with each other or
   with your network — find which one before blaming your observations.
4. Report **error ellipses** (e.g. 95% confidence) and relative precisions between
   adjacent marks — the relative figure is what setting-out cares about.

## 4. Datums, projections and scale
- Coordinates on a map projection are **grid** coordinates; distances measured on site
  are **ground** distances at the site's elevation.
- Combined scale factor = grid scale factor × elevation (sea-level) factor. On a high
  site far from the projection's central meridian, the difference between grid and
  ground can be tens of ppm or more — a few cm across a long building.
- Decide and document: does the project work on the national grid (designers must
  apply the scale factor), or on a **site/ground grid** (scaled so distances are true)?
  Mixing them is a classic setting-out error.
- Heights: state whether orthometric (national levelling datum via geoid model) or
  ellipsoidal.

## Gotchas
- Fixing all control from the start can hide your blunders by spreading them out.
- Optimistic a-priori errors make good data look bad; pessimistic ones hide blunders.
- Disturbed old control: check existing marks against each other before trusting them.
- Coordinate transformation between old and new national datums is not a simple shift;
  use the official transformation/grid file.

## Verify
- [ ] Network has loops/cross-ties; every mark connected by ≥2 independent observations.
- [ ] Minimally constrained adjustment passes; outliers investigated, not deleted blindly.
- [ ] Constrained adjustment shows control is consistent.
- [ ] Error ellipses and relative precisions meet the spec.
- [ ] Datum, projection, scale factor approach and height datum documented in the control report.

*Uncertainty:* thresholds (e.g. standardised residual ~3) are common defaults and
vary by software and specification.
