---
id: humanities.archaeology.gis-for-archaeology.building-an-archaeological-site-gis
name: building-an-archaeological-site-gis
category: humanities
field: archaeology
product: gis-for-archaeology
tags: [gis-for-archaeology, archaeology, gis, qgis, arcgis, arcgis-pro, crs, coordinate-reference-system, epsg, georeferencing, historic-maps, geopackage, shapefile, site-gazetteer, her, smr, attribute-table, dem, dtm, lidar, viewshed, cost-surface, least-cost-path, kernel-density, predictive-modelling, spatial-analysis, cartography]
level: practitioner
status: draft
description: "Build a project GIS for archaeology in QGIS or ArcGIS: pick a CRS, structure a site gazetteer, georeference old maps, integrate survey data, and run viewshed and density analyses honestly."
sources:
  - "Conolly, J. & Lake, M. Geographical Information Systems in Archaeology (Cambridge, 2006)"
  - "QGIS user manual (docs.qgis.org)"
  - "Gillings, M., Hacıgüzeller, P. & Lock, G. (eds) Archaeological Spatial Analysis (Routledge, 2020)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building an archaeological site GIS

**Goal:** one coherent spatial database for a project — survey, excavation, historic maps,
LiDAR — that anyone can open, trust and analyse. Examples use QGIS (free); ArcGIS Pro has
equivalent tools under different names.

## 1. Coordinate reference system first
- Choose **one projected CRS** in metres for the project — usually the national grid
  (e.g. EPSG:27700 British National Grid) or the local UTM zone. Set it as the project CRS
  (Project › Properties › CRS).
- GNSS data arrives in WGS84 (EPSG:4326, degrees). Reproject it into the project CRS
  (Vector › Data Management › Reproject Layer) — don't just let on-the-fly reprojection hide
  the mismatch, or area/distance tools will give degree-based nonsense.
- Record datum transformations used (some national grids need a grid-based transformation
  such as OSTN15 for sub-metre accuracy). *Exact transformation availability depends on
  the PROJ version installed.*

## 2. Data structure
- Store layers in a **GeoPackage** (one .gpkg file, many layers, no 10-character field
  limit) rather than scattered shapefiles.
- A **site gazetteer** point/polygon layer with fields such as: `site_id` (stable, never
  reused), `name`, `type`, `period` (use a controlled vocabulary, e.g. a period thesaurus),
  `confidence`, `source`, `source_ref`, `location_accuracy_m`, `recorded_by`, `date`.
- Excavation: separate layers for trench outlines, context polygons (`context_no`
  links to the database), small finds points, sample points, section lines.
- Keep **source accuracy** as data: a find spot from a 1950s note is not ±0.02 m.

## 3. Georeferencing historic maps and plans
- Raster › Georeferencer. Pick control points at features that haven't moved — churches,
  road junctions, field corners — spread over the whole sheet, not clustered.
- Use a **polynomial 1** (affine) or **Helmert** transform for most maps; thin-plate spline
  only when you knowingly accept local warping. Check residuals; report the RMS error.
- Save the GCP points file alongside the output GeoTIFF.

## 4. Analysis
- **Density:** Heatmap (kernel density) of surface finds — state the radius and why; the
  pattern changes with it. Normalise by area walked / visibility where possible.
- **Viewshed:** Use a DTM (not DSM unless vegetation/buildings are wanted), set observer
  height (~1.6 m) and target height, and a max radius. Vegetation of the past is unknown —
  say so. Cumulative viewsheds over many sites are more robust than one.
- **Least-cost paths:** cost surfaces from slope; choice of cost function (e.g. Tobler's
  hiking function) is an assumption to report.
- **Predictive modelling:** useful for planning surveys, risky for "where sites aren't". It
  tends to reproduce where people already looked. Validate against independent data.

## Gotchas
- Mixed CRS is the most common silent error; check every layer's CRS on import.
- Don't publish precise coordinates of sensitive or unprotected sites (looting); generalise
  public maps to a grid square.
- Version your GeoPackage (dated copies or a repo); attribute edits are easy to lose.
- Symbology isn't analysis: a dramatic colour ramp on a hillshade proves nothing.

## Verify
- [ ] All layers in the single project CRS; transformations recorded.
- [ ] Gazetteer has stable IDs, controlled vocabularies, source and accuracy fields.
- [ ] Georeferenced rasters have GCPs saved and RMS error reported.
- [ ] Every analysis states its parameters and assumptions.
- [ ] Public outputs generalise sensitive locations.
