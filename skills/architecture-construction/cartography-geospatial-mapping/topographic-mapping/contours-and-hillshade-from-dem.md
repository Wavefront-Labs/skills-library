---
id: architecture-construction.cartography-geospatial-mapping.topographic-mapping.contours-and-hillshade-from-dem
name: contours-and-hillshade-from-dem
category: architecture-construction
field: cartography-geospatial-mapping
product: topographic-mapping
tags: [topographic-mapping, topography, relief, dem, dtm, dsm, elevation-model, contours, contour-interval, index-contours, hillshade, multidirectional-hillshade, azimuth, altitude, z-factor, gdal, gdaldem, gdal_contour, gdal_fillnodata]
level: practitioner
status: docs-checked
description: "Depict relief from a DEM with GDAL: generate contours with gdal_contour, build hillshade with gdaldem, set azimuth/altitude/scale, fill nodata."
sources: ["https://gdal.org/en/stable/programs/gdal_contour.html", "https://gdal.org/en/stable/programs/gdaldem.html", "https://gdal.org/en/stable/programs/gdal_fillnodata.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contours and hillshade from a DEM

**Goal:** relief a reader understands instantly: hillshade for form, contours for
measurable height, without artefacts or misleading precision.

## 1. Choose the elevation model (cartographic practice)
- Use a bare-earth DTM for contours; a DSM includes buildings and trees, so contours
  would wrap round every roof.
- Check vertical units (metres or feet) and the vertical datum before contouring.
- Match DEM resolution to map scale, and make the contour interval comfortably larger
  than the DEM's vertical accuracy. National map series fix their own intervals; follow
  them.

## 2. Generate contours with gdal_contour
```bash
gdal_contour -a elev -i 10 -f GPKG dtm.tif contours_10m.gpkg
```
- `-i <interval>`: elevation interval; one of `-i`, `-fl` or `-e` is required. The first
  contour is at the first multiple of the interval above the raster minimum.
- `-off <offset>`: offset from zero; `-i 100 -off 25` gives ...-75, 25, 125...
- `-fl <level> ...`: fixed levels in ascending order.
- `-a <name>`: attribute name that stores the elevation. Without it no elevation
  attribute is written (ignored in `-p` polygon mode).
- `-snodata <value>`: input value to treat as nodata. `-nln <name>`: output layer name
  (default "contour"). `-f <format>`: output vector format.
- Index contours: contour at the index interval separately (for example run again with
  `-i 50`) or flag lines on the elevation attribute, then style them heavier and label
  them.

## 3. Hillshade with gdaldem
```bash
gdaldem hillshade dtm.tif hillshade.tif -az 315 -alt 45 -z 1 -compute_edges
```
- `-az`: light azimuth in degrees (0 = from the top of the raster, 90 = from the east).
  The default, 315, "should rarely be changed" because it is the value generally used
  for shaded maps.
- `-alt`: light altitude in degrees (90 = from directly above, 0 = raking light).
- `-z <factor>`: vertical exaggeration, pre-multiplying elevations. State it on the map
  if used.
- `-s <scale>`: ratio of vertical to horizontal units. For a lat/long DEM with metre
  elevations use 111120 (370400 if elevations are in feet); reprojecting first is the
  alternative.
- `-compute_edges`: compute values at image edges, and where nodata falls in the 3x3
  window, by interpolating missing values.
- Shading variants: `-combined` (slope plus oblique shading) and `-multidirectional`
  exist; `-alg Horn|ZevenbergenThorne` selects the slope algorithm.

## 4. Fill voids
`gdal_fillnodata src.tif dst.tif` interpolates nodata regions from valid edge pixels.
`-md` sets the maximum search distance in pixels (default 100), `-si` the number of 3x3
smoothing iterations after interpolation (default 0), `-mask` a validity file (zero
invalid), `-b` the band. It is a Python utility, available only with the GDAL Python
bindings.

## Verify
- [ ] DTM, not DSM, used for contours; vertical units and datum stated.
- [ ] Interval suits scale and DEM accuracy.
- [ ] Hillshade parameters recorded (azimuth, altitude, z, scale); exaggeration noted.
- [ ] Voids filled or masked before shading.

## Checked
2026-11-09. Confirmed on the three GDAL program pages: every option, default and example
quoted above. Cartographic practice in section 1 is general and not sourced from these
pages. Removed because not on any page read: the scale-denominator interval rule, the
0.5 mm spacing rule, resampling advice, lighting rationale (relief inversion), altitude
range advice, tint colour advice, label placement rules, line-smoothing advice, QGIS and
ArcGIS Pro tool paths, and the Imhof and Patterson references. The QGIS docs were not
readable.
Method: documentation only; no commands were run.
