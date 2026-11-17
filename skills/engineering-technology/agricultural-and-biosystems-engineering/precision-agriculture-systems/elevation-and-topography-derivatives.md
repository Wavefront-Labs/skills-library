---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.elevation-and-topography-derivatives
name: elevation-and-topography-derivatives
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, elevation-mapping, digital-elevation-model, topographic-wetness-index, slope-aspect, rtk-elevation, lidar-dem, terrain-analysis]
level: practitioner
status: draft
description: "Build elevation models and terrain layers for farm fields: RTK or LiDAR sources, DEM cleaning, slope, aspect, curvature and wetness index for zones and drainage."
sources:
  - "Topographic wetness index, Wikipedia (https://en.wikipedia.org/wiki/Topographic_wetness_index)"
  - "USGS 3D Elevation Program (https://www.usgs.gov/3d-elevation-program)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Elevation and topography derivatives

**Goal:** a clean field DEM and terrain layers that explain yield, water and erosion patterns.

## Sources
- RTK GNSS elevation logged during field operations (planting, spraying, yield mapping) gives centimetre-level relative elevation if the base position and the antenna height are consistent; a dedicated survey with RTK is best.
- Public LiDAR-derived DEMs where available (for example the US 3DEP programme or national equivalents) at 1-3 m resolution (unconfirmed; see the USGS 3DEP page for current products); check the date of collection and the post-collection field changes (levelling, drainage).
- Drone photogrammetry gives surface models (crop canopy) and not bare ground unless taken bare.

## Processing
1. Clean points: remove outliers and spikes, apply the geoid or datum correction consistently (GNSS ellipsoid heights versus orthometric heights), and combine multiple passes.
2. Interpolate to a grid (inverse distance weighting or kriging) at a resolution appropriate to the point density; avoid over-smoothing or artefacts along the passes.
3. Derive: slope, aspect, curvature (plan and profile), flow direction and accumulation, and topographic wetness index TWI = ln(a / tan(b)), where a is the specific catchment area and b the slope; use the tools in QGIS, SAGA, GDAL or Whitebox.
4. Fill sinks only when real depressions are not important to your question; do not fill prairie potholes that matter.

## Uses
Management zones for variable-rate seeding and nitrogen, waterlogging and drainage design (`surface-drainage-and-field-ditches`), erosion and grassed waterway planning, and the correct interpretation of yield maps.

## Verify
- [ ] Compare the DEM with surveyed check points: report RMSE.
- [ ] Datum and units written in the metadata.
- Unconfirmed: availability and dates of public datasets in your area.
