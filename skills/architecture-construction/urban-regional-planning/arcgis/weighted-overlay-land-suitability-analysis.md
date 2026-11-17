---
id: architecture-construction.urban-regional-planning.arcgis.weighted-overlay-land-suitability-analysis
name: weighted-overlay-land-suitability-analysis
category: architecture-construction
field: urban-regional-planning
product: arcgis
tags: [arcgis, arcgis-pro, esri, gis, urban-planning, land-suitability, suitability-analysis, suitability-modeler, weighted-overlay, weighted-sum, multi-criteria-analysis, mcda, constraints, exclusions, reclassify, euclidean-distance, raster, model-builder, land-use-planning, growth-areas, site-selection, sensitivity-analysis, census-data, demographic-overlay]
level: practitioner
status: draft
description: "Land suitability analysis in ArcGIS Pro: separate hard constraints from weighted criteria, reclassify to a common scale, combine with Suitability Modeler or Weighted Overlay, and test sensitivity."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ArcGIS Pro — weighted-overlay land suitability for planning

**Goal:** a transparent map of where growth (housing, industry, a facility) is most
and least suitable, that a planning committee can interrogate and that survives a
change of weights.

## 1. Frame the question
Write it down: "suitability for medium-density housing within the district, 2030 horizon".
List criteria with the policy reason for each (e.g. distance to rail station — transit
policy; slope — servicing cost; flood zone — risk). Agree them with the policy lead
before touching GIS; the weights are a policy decision, not a technical one.

## 2. Data preparation
- One **projected** coordinate system for everything (metres), the study-area boundary,
  and a common **cell size** (e.g. 10–25 m for a district) and snap raster.
- Set these in **Analysis › Environments** (Output Coordinate System, Extent, Cell Size,
  Snap Raster, Mask) so every tool output aligns.
- Typical inputs: DEM → Slope; flood zones; protected areas; transport stops →
  distance; existing services; land-use/zoning; parcel/ownership; census tracts for
  demand.

## 3. Constraints vs factors
- **Constraints (exclusions):** areas that are simply unavailable — e.g. high flood
  hazard, national parks, water bodies, existing cemeteries. Make a 0/1 mask. Do **not**
  give them a low weight instead: a high score elsewhere could outweigh it.
- **Factors:** criteria that make land more or less suitable on a continuum.

## 4. Transform factors to a common scale
- Use **Suitability Modeler** (ArcGIS Pro 2.8+, Spatial Analyst) which lets you
  transform each criterion with continuous functions (linear, small/large, MS-Small
  etc.) or categories to a common 1–10 scale with live preview.
- Or manually: **Euclidean Distance** / **Distance Accumulation** for proximity,
  **Slope** for terrain, then **Reclassify** to 1–9 (or 1–10).
- Make direction explicit: closer to a station = higher; steeper = lower.

## 5. Weighting and combining
- **Weighted Overlay** (integer scale, weights sum to 100%) or **Weighted Sum** (keeps
  decimals; better for continuous results). Suitability Modeler does this step in-tool.
- Derive weights by a documented method: stakeholder ranking, pairwise comparison
  (AHP), or simple equal weights as a baseline.
- Multiply the result by the constraint mask so excluded land is 0/NoData.
- Use **Locate** in Suitability Modeler (or region-grouping + zonal statistics) to find
  contiguous areas above a minimum size — a scattered cell of high suitability is not a site.

## 6. Sensitivity and reporting
- Re-run with alternative weights (e.g. ±10% on each criterion, or equal weights) and
  compare: areas that stay highly suitable in all runs are robust findings.
- Summarise by parcel or neighbourhood with **Zonal Statistics as Table**.
- Map with a clear classed legend (e.g. 5 classes) and state the criteria and weights on
  the map or in a table beside it. Build the workflow in **ModelBuilder** or a notebook
  so it can be re-run when data or weights change.

## Gotchas
- Mismatched cell sizes/extents give shifted or blocky results — set Environments first.
- Edge effects: distance surfaces stop at the extent; include a buffer beyond the study area.
- Equal intervals in reclassification can hide the policy-relevant threshold (e.g. 800 m
  walk catchment); classify on meaningful breakpoints.
- Spatial Analyst licence is required for most of these tools.

## Verify
- [ ] Criteria and weights have a written policy rationale agreed with the client.
- [ ] Constraints applied as a mask, not as low weights.
- [ ] All rasters share CRS, cell size and snap raster.
- [ ] Sensitivity runs done; robust areas identified.
- [ ] Model saved so the analysis is reproducible.

*Uncertainty:* menu paths and tool names reflect recent ArcGIS Pro 3.x releases and
may move between versions.
