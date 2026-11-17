---
id: social-sciences.human-geography.spatial-analysis.spatial-autocorrelation-and-spatial-regression
name: spatial-autocorrelation-and-spatial-regression
category: social-sciences
field: human-geography
product: spatial-analysis
tags: [spatial-analysis, spatial-statistics, spatial-autocorrelation, morans-i, global-morans-i, lisa, local-morans-i, getis-ord, gi-star, hot-spot-analysis, spatial-weights, queen-contiguity, rook-contiguity, k-nearest-neighbours, spatial-regression, spatial-lag-model, spatial-error-model, lagrange-multiplier-tests, gwr, geographically-weighted-regression, geoda, pysal, esda, spreg, spdep, r-sf, maup, accessibility, two-step-floating-catchment, 2sfca]
level: advanced
status: draft
description: "Testing and modelling spatial dependence in area data: weights matrices, Moran's I, LISA/Gi* hot spots, and spatial lag vs error models in GeoDa or PySAL."
sources: ["Anselin, 'Local Indicators of Spatial Association - LISA' (1995)", "Anselin & Rey, Modern Spatial Econometrics in Practice (GeoDa Press, 2014)", "Getis & Ord, 'The Analysis of Spatial Association by Use of Distance Statistics' (1992)", "PySAL (esda, spreg) and R spdep documentation", "Luo & Wang, '2SFCA' (2003)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spatial autocorrelation and spatial regression

**Goal:** check whether a social variable clusters in space, find where, and fit
regressions that don't pretend neighbouring areas are independent.

## 1. Build a spatial weights matrix (W)
W defines "neighbour". Choices:
- **Queen contiguity** (shared edge or corner) — default for areal units.
- **Rook** (shared edge only).
- **k-nearest neighbours** — avoids islands and uneven neighbour counts.
- **Distance band** — needs a threshold so every unit has ≥1 neighbour.
Row-standardise W for most tests. Check the connectivity histogram: **islands** (no
neighbours) break statistics — fix by kNN or manual links. Results depend on W, so
test robustness to an alternative.
Tools: GeoDa (GUI), PySAL (`libpysal.weights.Queen.from_dataframe`), R `spdep`
(`poly2nb`, `nb2listw`).

## 2. Global spatial autocorrelation: Moran's I
- Positive I = similar values cluster; ~0 (expected value −1/(n−1)) = random;
  negative = checkerboard.
- Inference by **permutation** (999+ permutations) rather than normal approximation.
- Use rates, not counts; for small-population rates use the **Empirical Bayes**
  Moran's I variant (available in GeoDa) to avoid variance instability.

## 3. Local clusters: LISA and Gi*
- **Local Moran (LISA):** classifies units as High-High, Low-Low (clusters) or
  High-Low, Low-High (outliers).
- **Getis-Ord Gi\*:** hot/cold spots of high/low values (ArcGIS *Hot Spot Analysis*).
- **Gotcha: multiple testing.** With hundreds of local tests, many "significant"
  clusters are false positives. Use a stricter p (e.g. 0.01 or 0.001), FDR correction,
  and check stability across W choices. Don't over-interpret single-unit clusters.

## 4. Spatial regression
1. Fit OLS. Run Moran's I on residuals. If significant, OLS SEs are wrong.
2. Use **Lagrange Multiplier diagnostics** (LM-lag, LM-error and their robust versions)
   from GeoDa/`spreg`:
   - Lag significant → **spatial lag model** (outcome in one area depends on neighbours'
     outcomes; diffusion/spillover).
   - Error significant → **spatial error model** (unmodelled spatially clustered factors).
   - Both robust tests significant → consider SAR combined (SARAR) or Durbin models.
3. **Interpretation gotcha:** in a lag model, coefficients are not marginal effects;
   report direct, indirect (spillover) and total impacts.
4. **GWR** (geographically weighted regression) explores varying relationships across
   space; treat it as exploratory, watch local multicollinearity, and use MGWR for
   variable-specific bandwidths.

## 5. Accessibility measures
Distance to nearest facility is crude; the **two-step floating catchment area
(2SFCA)** combines supply capacity and demand within travel-time catchments. Use
network travel time (OSRM, OpenRouteService, ArcGIS Network Analyst), not straight-
line distance, where roads matter.

## 6. MAUP
Results change with the areal units (scale and zoning effects). Re-run at another
scale (e.g. tract vs county) and report it.

## Verify
- [ ] W choice justified, islands handled, results checked with an alternative W.
- [ ] Moran's I computed on rates with permutation inference.
- [ ] Local cluster maps use a multiple-testing-aware threshold.
- [ ] OLS residual autocorrelation tested; model choice follows LM diagnostics.
- [ ] Lag-model impacts (direct/indirect) reported rather than raw coefficients.
