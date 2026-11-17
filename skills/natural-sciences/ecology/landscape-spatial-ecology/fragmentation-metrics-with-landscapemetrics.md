---
id: natural-sciences.ecology.landscape-spatial-ecology.fragmentation-metrics-with-landscapemetrics
name: fragmentation-metrics-with-landscapemetrics
category: natural-sciences
field: ecology
product: landscape-spatial-ecology
tags: [landscape-spatial-ecology, landscape-ecology, habitat-fragmentation, fragmentation-metrics, landscape-metrics, landscapemetrics, fragstats, r, terra, land-cover, raster, patch-density, edge-density, core-area, largest-patch-index, aggregation-index, effective-mesh-size, mesh, clumpy, contagion, neighbour-rule, edge-depth, buffer-analysis, scale-dependence, modifiable-areal-unit-problem, gis, qgis]
level: practitioner
status: docs-checked
description: "Quantify habitat fragmentation from a land-cover raster with landscapemetrics: choosing metrics, sample buffers, neighbour rule, edge depth, scale and correlated metrics."
sources: [https://r-spatialecology.github.io/landscapemetrics/reference/index.html, https://r-spatialecology.github.io/landscapemetrics/reference/sample_lsm.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fragmentation metrics with landscapemetrics

**Goal:** numbers describing how much habitat there is and how it is broken up, for
landscapes or buffers around study sites, that you can relate to ecological responses
without fooling yourself with redundant or scale-dependent metrics.

## 1. Get the input right first
- A **categorical raster** (land-cover classes as integers) in a **projected CRS**. The
  package notes that buffer-area results may be influenced by the CRS and the `transform`
  argument, so keep the CRS consistent.
- **Resolution and thematic detail** shape the answer: a coarse and a fine map of the same
  forest give very different patch counts. Choose the resolution that matches the
  organism's perception and keep it constant across sites.
- Reclassify to what matters (e.g. habitat = 1, matrix = 0; or a few classes). Check
  the raster with `landscapemetrics::check_landscape(r)`.
## 2. Choose a small, interpretable set
Separate **habitat amount** from **configuration** (Fahrig): many "fragmentation"
effects are really habitat-loss effects.
- Amount: percentage of landscape (`lsm_c_pland`).
- Subdivision: number of patches / patch density (`lsm_c_np`, `lsm_c_pd`), **effective
  mesh size** (`lsm_c_mesh`).
- Edge: edge density (`lsm_c_ed`); core area (`lsm_c_cai_mn`, which needs an edge depth).
- Dominance: largest patch index (`lsm_c_lpi`).
- Aggregation: aggregation index (`lsm_c_ai`) or clumpiness (`lsm_c_clumpy`).
Many metrics are correlated with each other and with PLAND — compute a correlation
matrix (`show_correlation`) and keep one per cluster.

## 3. Compute (R)
```r
library(landscapemetrics); library(terra); library(sf)
r   <- rast("landcover_utm.tif")
pts <- st_read("sites.gpkg") |> st_transform(crs(r))
lsm <- sample_lsm(r, y = pts, shape = "circle", size = 1000,     # radius in map units
                  what = c("lsm_c_pland", "lsm_c_ed", "lsm_c_mesh", "lsm_c_np"))
subset(lsm, class == 1)    # keep the habitat class
```
`sample_lsm` takes `y` (coordinates or a spatial object), `shape` ("circle" or
"square"; default square) and `size` in map units (the radius for circles, half the side
for squares). Extra arguments, such as edge depth and the neighbour rule, are passed on to
`calculate_lsm()`; read that page for their names and defaults.

## 4. Settings that change results
- **Neighbour rule:** whether diagonals connect changes patch counts and sizes. State it.
- **Edge depth** for core area: the unit and its meaning depend on resolution. Base it on
  a known edge-effect distance for your organism.
- **Landscape boundary:** patches cut by the buffer edge are truncated; patch metrics are
  biased in small buffers.
- **Scale of effect:** responses depend on buffer size. Compute metrics at several radii
  and choose the scale with the strongest relationship, or justify a biological scale a
  priori. Overlapping buffers create spatial non-independence.

## Gotchas
- Classes absent from a buffer may return no row — treat as 0 habitat explicitly.
- Noise in the classification creates spurious tiny patches; consider a minimum mapping
  unit or majority filter (and report it).
- Function names follow the package reference index; check it for your installed version.

## Verify
- [ ] Raster in a projected CRS; categorical classes preserved when resampling.
- [ ] Habitat amount reported alongside every configuration metric.
- [ ] Correlated metrics pruned.
- [ ] Neighbour rule, edge depth, buffer size and resolution stated.
- [ ] Multiple buffer sizes explored or one justified biologically.

## Checked
2026-11-01. Confirmed on the landscapemetrics reference pages: lsm_c_pland, np, pd, mesh, ed, cai_mn, lpi, ai, clumpy, sample_lsm, check_landscape, show_correlation and calculate_lsm exist; sample_lsm arguments y, shape (circle/square, default square) and size (radius for circles, half side for squares, in map units); extra arguments pass to calculate_lsm(); CRS may influence buffer-area results. Removed (not stated on pages read): edge_depth = 3 and directions = 8 values, the 4- vs 8-neighbour consequence, the 0.7 correlation cut-off, example radii, the Jaeger definition of mesh size, FRAGSTATS equivalence claim, terra project call.
Method: documentation only; no commands were run.
