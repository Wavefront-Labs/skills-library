---
id: architecture-construction.cartography-geospatial-mapping.remote-sensing-interpretation.supervised-land-cover-classification
name: supervised-land-cover-classification
category: architecture-construction
field: cartography-geospatial-mapping
product: remote-sensing-interpretation
tags: [remote-sensing-interpretation, remote-sensing, image-classification, supervised-classification, land-cover, land-use, sentinel-2, landsat, multispectral, surface-reflectance, atmospheric-correction, cloud-mask, training-samples, random-forest, maximum-likelihood, svm, ndvi, ndwi, spectral-indices, accuracy-assessment, confusion-matrix, kappa, overall-accuracy, producers-accuracy, users-accuracy, stratified-random-sampling, google-earth-engine, qgis, arcgis-pro, scp-plugin]
level: practitioner
status: draft
description: "Classify land cover from satellite imagery: analysis-ready reflectance, a clear class scheme, honest training data, a random-forest classifier with indices, then stratified accuracy assessment."
sources: ["Olofsson et al. (2014), Good practices for estimating area and assessing accuracy of land change, Remote Sensing of Environment", "Congalton & Green, Assessing the Accuracy of Remotely Sensed Data", "ESA Sentinel-2 and USGS Landsat product documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Supervised land-cover classification

**Goal:** a land-cover map from satellite imagery with a **known, defensible accuracy**
— not just a pretty classified raster. The classifier is the easy part; data preparation
and accuracy assessment are where results are made or broken.

## 1. Define the class scheme first
- Mutually exclusive, exhaustive classes with written definitions and a minimum mapping
  unit (e.g. "Tree cover: ≥ 30% canopy, ≥ 0.5 ha").
- Match the classes to what the sensor can see: Sentinel-2 at 10–20 m can separate
  water, built-up, cropland, grassland, forest; it cannot reliably separate "residential
  vs commercial" (that's land *use*, not cover).

## 2. Prepare imagery
- Use **surface reflectance** (atmospherically corrected) products, e.g. Sentinel-2 Level-2A
  or Landsat Collection 2 Level-2. Don't mix top-of-atmosphere and surface reflectance.
- **Mask clouds and shadows** (scene classification layer / QA bands), then build a
  median composite over a season to fill gaps.
- Consider **multi-season** composites: cropland vs grassland often only separate by
  phenology.
- Add derived bands: **NDVI** = (NIR − Red)/(NIR + Red); NDWI/MNDWI for water; NDBI for
  built-up; terrain (elevation, slope) where relief matters.
- Same CRS and resolution for all inputs; resample 20 m bands to 10 m consistently.

## 3. Training data
- Collect polygons/points per class from high-resolution imagery, field data or trusted
  reference maps, spread across the whole area and all sub-types (shaded slopes, dry
  and wet fields, different roof materials).
- Pure samples, well inside homogeneous areas; avoid edges.
- Balance: enough samples per class (often hundreds of pixels), not dominated by one class.
- Keep **training and validation data separate** — never assess accuracy on training
  samples (spatially adjacent pixels from the same polygon also leak; split by polygon).

## 4. Classify
- **Random forest** is a robust default (e.g. 100–500 trees); also SVM. Maximum
  likelihood assumes normal distributions and suits fewer, well-behaved classes.
- Tools: Google Earth Engine (`ee.Classifier.smileRandomForest`), QGIS (Semi-Automatic
  Classification Plugin / Processing), ArcGIS Pro (*Classification Wizard*), Python
  (scikit-learn + rasterio).
- Post-process: majority filter or sieve to the minimum mapping unit to remove salt-and-
  pepper noise.

## 5. Accuracy assessment (the part reviewers check)
- Draw an independent **stratified random sample** of validation points by mapped class
  (good practice per Olofsson et al.), with enough points in rare classes (e.g. ≥ 50).
- Label each point from reference data **without looking at the classification**.
- Build a **confusion (error) matrix**: overall accuracy, **producer's accuracy**
  (omission errors — how much of real class X was mapped as X) and **user's accuracy**
  (commission errors — how often a pixel mapped as X really is X).
- Report **area estimates with confidence intervals** adjusted by the error matrix,
  rather than pixel counts — pixel counting is biased when errors are unequal.
- Kappa is common in older literature but is now widely discouraged as a sole measure.

## Gotchas
- Classifying a single cloudy-season image and calling it annual land cover.
- Shadows of buildings/mountains classified as water — use terrain/shadow masks or a
  shadow class.
- Spectral confusion between bare soil and built-up, and between wetland and water.
- Overall accuracy can look high while a small class of interest is badly mapped — read
  per-class accuracies.

## Verify
- [ ] Class definitions and minimum mapping unit written down.
- [ ] Surface reflectance, cloud-masked composite used.
- [ ] Training and validation independent (split by polygon/location).
- [ ] Confusion matrix with producer's and user's accuracies reported per class.
- [ ] Areas reported with error-adjusted estimates and confidence intervals.
