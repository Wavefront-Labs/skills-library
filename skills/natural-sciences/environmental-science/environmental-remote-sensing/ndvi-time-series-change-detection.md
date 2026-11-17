---
id: natural-sciences.environmental-science.environmental-remote-sensing.ndvi-time-series-change-detection
name: ndvi-time-series-change-detection
category: natural-sciences
field: environmental-science
product: environmental-remote-sensing
tags: [environmental-remote-sensing, remote-sensing, ndvi, evi, nbr, vegetation-index, change-detection, time-series, landsat, sentinel-2, harmonized-landsat-sentinel, hls, surface-reflectance, cloud-masking, qa-pixel, scl, fmask, google-earth-engine, gee, bfast, landtrendr, ccdc, phenology, disturbance, deforestation, burn-severity, accuracy-assessment, drone-surveys]
level: practitioner
status: docs-checked
description: "Detect vegetation change from NDVI/NBR time series: surface reflectance, strict cloud masks, sensor harmonisation, BFAST/LandTrendr/CCDC, and error-adjusted area estimates."
sources: [https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-reflectance, https://www.usgs.gov/landsat-missions/landsat-normalized-burn-ratio, https://www.usgs.gov/landsat-missions/landsat-normalized-difference-vegetation-index, https://www.usgs.gov/landsat-missions/landsat-7, https://sentiwiki.copernicus.eu/web/s2-processing, https://hls.gsfc.nasa.gov/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NDVI time-series change detection

**Goal:** answer "where and when did vegetation change?" (clearing, fire, drought
browning, restoration greening) from satellite archives, with a map and an area
estimate whose uncertainty you can state.

## 1. Choose the index and the archive
- **NDVI = (NIR − Red)/(NIR + Red)** — general greenness; saturates in dense canopy.
- **NBR = (NIR − SWIR2)/(NIR + SWIR2)** (Landsat 4-7 bands 4 and 7; Landsat 8-9 bands 5
  and 7) — the usual index for fire and clearing; compare pre- and post-event values.
- **Landsat** (30 m surface reflectance, record from 1984, 16-day repeat cycle) for long
  records; **Sentinel-2** (10, 20 and 60 m bands) for detail; **HLS** (Harmonized
  Landsat and Sentinel-2, NASA) if you want both pre-matched as if one collection.
- Always use **surface reflectance** (Landsat Collection 2 Level-2, Sentinel-2 L2A),
  never top-of-atmosphere, for multi-date work. Apply the scale factors: Landsat C2 L2
  reflectance = DN × 0.0000275 − 0.2 (forgetting this gives nonsense NDVI).

## 2. Mask clouds aggressively
- Landsat: use the surface-reflectance QA bands (cloud, cloud shadow, fill) and read the
  product guide for the bit definitions.
- Sentinel-2: SCL classes (keep 4 vegetation, 5 not vegetated, 6 water as needed; drop
  3 cloud shadows, 8 and 9 cloud probability, 10 thin cirrus, 11 snow or ice).
- Residual cloud and shadow are the dominant source of false "change" — inspect
  outliers visually before trusting any break.

## 3. Harmonise across sensors
Landsat 5/7 (TM/ETM+) and 8/9 (OLI) are different sensors, so indices can differ
slightly. Apply published cross-sensor coefficients or use HLS.
Landsat 7 has scan-line gaps since the Scan Line Corrector failed on 31 May 2003
(about 78 percent of each scene's pixels remain; gap masks mark the rest) — mask them,
don't interpolate blindly.

## 4. Pick a method that fits the question
| Question | Method |
|---|---|
| Abrupt change between two dates | Image differencing (dNDVI, dNBR) with thresholds |
| When did a break occur, in a seasonal series | BFAST / BFAST Monitor |
| Annual disturbance and recovery trajectories | LandTrendr |
| Continuous land-cover change with all observations | CCDC |
| Gradual greening/browning trend | Mann-Kendall / Theil-Sen on annual composites |
Compare same-season composites (e.g. peak growing-season median) to avoid phenology
masquerading as change; in agriculture, crop rotation produces large "changes" that are
not land-cover change.

## 5. Accuracy and area estimation
Pixel-counting a change map biases area. Draw a **stratified random sample** of pixels
by map class, label each from reference imagery (high-resolution images, time-series
plots), build the confusion matrix, then compute **error-adjusted area** with confidence
intervals. Change is rare, so the change stratum needs a disproportionately large sample.

## 6. Drone surveys
UAV multispectral cameras give cm-scale NDVI for plots. Calibrate each
flight with a reflectance panel and irradiance sensor; otherwise NDVI shifts with
sun angle and clouds and can't be compared across dates.

## Gotchas
- Mask water and snow first (SCL classes 6 and 11).
- Mixed pixels at 30 m blur narrow features (riparian strips, roads).
- Topographic shadow mimics vegetation loss in winter scenes.
- Do not threshold dNBR from a published table without local field calibration.

## Verify
- [ ] Surface reflectance with correct scaling; masks for cloud, shadow, snow, water applied.
- [ ] Multi-sensor series harmonised; same-season comparison used.
- [ ] Method matches question (abrupt vs gradual); parameters documented.
- [ ] Stratified reference sample, confusion matrix, error-adjusted area with CIs reported.

## Checked
2026-11-01. Confirmed: Landsat Collection 2 surface reflectance scale factor 0.0000275 and offset -0.2, 30 m, sensor
record from Landsat 4/5 in 1982-84 (USGS Collection 2 surface reflectance page); NDVI and NBR band numbers (USGS NDVI
and NBR pages); Landsat 7 SLC failure date, 78 percent of pixels, 16-day repeat cycle (USGS Landsat 7 page); Sentinel-2
SCL class numbers and 10/20/60 m bands (SentiWiki); HLS combining Landsat and Sentinel-2 at 30 m (NASA HLS page).
Removed: EVI/saturation claims, dNBR definition, Sentinel-2 revisit and launch year, QA_PIXEL bit names, water/snow
NDVI sign claim, sample-size minimum, 95 percent CI, named paper references (no readable page).
Method: documentation only; no commands were run.
