---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.satellite-imagery-selection-and-cloud-handling
name: satellite-imagery-selection-and-cloud-handling
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, satellite-imagery-agriculture, remote-sensing-agriculture, crop-sensing, sentinel-2, landsat, cloud-masking, ndvi-time-series]
level: practitioner
status: verified
description: "Choose satellite imagery for crop monitoring: resolution and revisit of Sentinel-2, Landsat and commercial sources, cloud masking, atmospheric correction and field-edge handling."
sources:
  - "Copernicus Sentinel-2 mission, SentiWiki (https://sentiwiki.copernicus.eu/web/s2-mission)"
  - "NASA Landsat 9 (https://landsat.gsfc.nasa.gov/satellites/landsat-9/)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Satellite imagery selection and cloud handling

**Goal:** the right imagery for the decision at an affordable cost, with clouds handled correctly.

## Sources (check current availability)
- **Sentinel-2** (Copernicus programme): 10 m bands for visible and near-infrared (B2, B3, B4, B8), 20 m red-edge bands (B5-B7, B8a), nominal revisit of 5 days at the equator with two satellites (more often at higher latitude); free and open data.
- **Landsat 8 and 9**: 30 m, combined revisit about 8 days; free; thermal bands useful for water stress.
- **Commercial constellations**: metre-scale resolution and up to daily revisit, depending on the vendor (check the product sheet); paid; useful for small fields and frequent monitoring.
- **Radar (Sentinel-1)**: penetrates cloud; used for soil moisture and crop structure.

## Selection by decision
1. Field size: pixel size should be small relative to the field and management zone (10 m pixels need fields of several hectares).
2. Timing: revisit and cloud frequency in your region during the key growth stage.
3. Spectral needs: red-edge for chlorophyll or nitrogen indices; thermal for water stress.

## Processing
1. Use surface-reflectance products (atmospherically corrected, such as Sentinel-2 L2A).
2. **Cloud and shadow masking** using the product's scene classification layer or a cloud-probability tool; remove contaminated pixels; check visually for thin cloud.
3. **Field boundary buffer**: shrink the boundary inward by about one pixel width or more (10 m or more for Sentinel-2) to avoid mixed pixels at edges.
4. Compute indices (NDVI = (NIR - Red)/(NIR + Red)), build time series, compare with the field's or region's normal.

## Gotchas
- NDVI saturates in dense canopy; use red-edge indices where sensitivity is needed.
- Different sensors need cross-calibration for combined time series.

## Verify
- [ ] Time series is smooth for a healthy field and shows expected seasonal curve; check against ground observations.
