---
id: agriculture-environment.conservation-land-stewardship.conservation-gis.qgis-qfield-site-mapping-workflow
name: qgis-qfield-site-mapping-workflow
category: agriculture-environment
field: conservation-land-stewardship
product: conservation-gis
tags: [conservation-gis, qgis, qfield, qfieldsync, qfieldcloud, gis, field-mapping, gps, gnss, geopackage, crs, projected-crs, utm, mga, weed-mapping, infestation-layer, monitoring-points, photo-points, work-records, value-maps, attribute-form, field-calculator, area-calculation, buffer, dissolve, mergin-maps, avenza, site-map, print-layout]
level: practitioner
status: draft
description: "A QGIS + QField workflow for conservation sites: projected-CRS GeoPackage layers with dropdown forms, packaging for the field, syncing back, calculating treated areas and printing work maps."
sources: ["QGIS documentation (docs.qgis.org)", "QField documentation (docs.qfield.org)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QGIS + QField site mapping workflow

**Goal:** one tidy set of layers for a conservation site — boundary, infestations,
monitoring points, works done — that crews edit on phones in the field and that sums
cleanly into hectares treated and maps for reports. Tested against the QGIS 3.x LTR
line and QField 3.x; menu names may shift slightly between versions.

## 1. Set up the project
1. **Project › Properties › CRS:** choose a *projected* CRS for your zone (UTM zone,
   or national grid such as GDA2020 / MGA zone XX, British National Grid, a state plane).
   Areas and lengths in geographic WGS84 degrees are meaningless.
2. Save everything in **one GeoPackage** (`site.gpkg`) beside the `.qgz` project file —
   one file, multiple layers, no shapefile 10-character field-name limits.
3. **Layer › Create Layer › New GeoPackage Layer** for each:
   - `boundary` (polygon)
   - `infestations` (polygon): `species` (text), `density` (text), `stage` (text),
     `date` (date), `observer` (text), `photo` (text)
   - `monitoring_points` (point): `site_id`, `type` (photo point / camera / plot)
   - `works` (polygon or line): `date`, `method`, `product`, `rate`, `crew`, `hours`
   Use the same CRS as the project.

## 2. Build field-friendly forms
Layer **Properties › Attributes Form**:
- `species`, `density`, `stage`, `method`: widget **Value Map** with a fixed list (no
  free typing = no "Lantana", "lantana", "lantanna" mess).
- `date`: **Date/Time** widget, default value `now()`.
- `observer`: default value `@qgis_user` / or Value Map of crew names.
- `photo`: **Attachment** widget, relative paths, so phone photos link to features.
- Mark key fields **Not null** under Constraints so incomplete records can't be saved.

## 3. Package for QField
- Install the **QFieldSync** plugin (Plugins › Manage and Install).
- Basemap: add an imagery layer (XYZ tiles or a clipped GeoTIFF). For offline use,
  QFieldSync can render a basemap or you include a clipped raster.
- **Plugins › QFieldSync › Project Configuration:** set each layer's action —
  *offline editing* for the layers crews edit, *copy* for reference layers.
- Either **Package for QField** (copy the output folder to the phone over USB) or use
  **QFieldCloud** to sync over the network.

## 4. In the field (QField)
- Check GNSS accuracy before digitising: phone GPS is typically ~3–10 m; an external
  GNSS receiver gets sub-metre. Record accuracy if it matters.
- Digitise polygons by walking the edge with **position-tracking/streaming** mode, or
  by tapping vertices on imagery when the edge is visible.
- Take photos from the form so they attach to the feature.

## 5. Bring it back
- **QFieldSync › Synchronise from QField** (USB) or sync via QFieldCloud. Open the
  attribute table and sanity-check new rows.
- Fix geometry: **Vector › Geometry Tools › Check Validity** / Processing "Fix geometries".

## 6. Calculate and summarise
- Area in hectares: Field Calculator new field `area_ha` = `$area / 10000` (uses the
  project's ellipsoid settings; fine in a projected CRS).
- Hectares treated per method: Processing › **Statistics by categories** (sum of
  `area_ha` by `method`) or **Vector › Analysis Tools › Basic statistics**.
- Overlapping infestation polygons double-count: **Dissolve** by species before summing.
- Riparian zone: **Vector › Geoprocessing Tools › Buffer** on the stream layer (e.g.
  20 m), then **Clip/Intersection** with infestations to report weeds within it.

## 7. Maps for reports
**Project › New Print Layout**: map, legend, scale bar, north arrow, title, date,
CRS note, data source. Export PDF. Use **Atlas** for one page per management unit.

## Gotchas
- Mixed CRSs: QGIS reprojects on the fly, so it *looks* fine while calculations and
  exports silently use the layer's own CRS. Check each layer's CRS.
- Shapefiles lose long field names and fail on large text; stick with GeoPackage.
- Don't edit the same layer in QGIS on the desktop while a field package is out;
  sync conflicts follow.
- Keep the master GeoPackage backed up before each sync.
- Sensitive species locations: generalise or exclude before sharing maps.
Alternatives in common use: Mergin Maps (QGIS-based, sync-centric), Avenza Maps
(PDF map field collection), ArcGIS Field Maps (Esri licence).

## Verify
- [ ] Project and all layers in the same projected CRS.
- [ ] Forms use dropdowns for categorical fields; required fields enforced.
- [ ] Synced field data appears in the master GeoPackage with photos linked.
- [ ] Area summaries computed from dissolved, valid geometries in hectares.
- [ ] Report map has scale bar, north arrow, date and CRS.
