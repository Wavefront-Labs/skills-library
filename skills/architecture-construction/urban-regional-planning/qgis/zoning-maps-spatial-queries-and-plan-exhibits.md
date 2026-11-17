---
id: architecture-construction.urban-regional-planning.qgis.zoning-maps-spatial-queries-and-plan-exhibits
name: zoning-maps-spatial-queries-and-plan-exhibits
category: architecture-construction
field: urban-regional-planning
product: qgis
tags: [qgis, gis, open-source-gis, urban-planning, zoning-map, land-use-map, spatial-query, select-by-location, select-by-expression, field-calculator, join-attributes-by-location, buffer, notification-radius, categorized-symbology, rule-based-symbology, print-layout, atlas, plan-exhibit, geopackage, crs, topology-checker, parcels, cadastre]
level: practitioner
status: draft
description: "Planning work in QGIS: build a clean zoning map from parcels, answer spatial questions (which lots are within 400 m of a station?), and produce consistent print layouts and atlas exhibits."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QGIS — zoning maps, spatial queries and plan exhibits

**Goal:** answer everyday planning questions with reproducible queries and produce
exhibit maps that look consistent across a whole plan.

## 1. Project set-up
- Set the **project CRS** to your local projected system (metres) in Project ›
  Properties › CRS. Distances and areas in a geographic CRS (degrees) are meaningless.
- Store layers in a **GeoPackage** (`.gpkg`) — one file, many layers, no shapefile
  field-name truncation at 10 characters.
- Keep relative paths on (Project Properties › General) so the project opens on other
  machines.

## 2. A clean zoning layer
- Zoning polygons should tile the jurisdiction without gaps or overlaps. Check with
  **Topology Checker** (rules "must not overlap", "must not have gaps") or
  Vector › Geometry Tools › Check Validity; fix with Snapping (Project › Snapping
  Options, enable topological editing) or Processing › Fix Geometries.
- Use a code field (e.g. `zone_code`) plus a lookup table of zone names and controls
  joined in (Layer Properties › Joins), so the legend text lives in one place.
- Symbology: **Categorized** on `zone_code`, colours following your jurisdiction's
  convention (e.g. yellows for residential, reds for commercial, purples for industrial,
  greens for open space — conventions differ by country; follow the local standard).
- Save the style as a `.qml` (or in the GeoPackage) so every map uses identical colours.

## 3. Spatial queries planners actually need
- **Lots within 400/800 m of a station:** Vector › Geoprocessing › Buffer the station
  points (set distance in layer units), then Vector › Research Tools › **Select by
  Location** (parcels "intersect" or "are within" the buffer). Note straight-line buffers
  overstate walkability; for network catchments use a routing plugin or service areas
  on a street network.
- **Notification radius** for an application: buffer the subject site, select
  intersecting parcels, export owners' parcel IDs (handle personal data according to
  your privacy rules).
- **Attribute + spatial:** **Select by Expression** e.g.
  `"zone_code" = 'R2' AND $area > 600` to find lots above a minimum size.
- **Attach zone to parcels:** Processing › **Join Attributes by Location** (or by
  location summary if parcels straddle zones — and then flag split-zoned lots).
- **Field Calculator** for derived values: `$area`, potential yield
  (`$area * "far"`), distance to nearest service via `overlay_nearest()`/`distance()`
  expressions in recent versions.
- Save repeated workflows with the **Graphical Modeler** so they can be re-run when data change.

## 4. Print layouts and atlas
- Project › New Print Layout. Add map, legend (filter to visible features), scale bar,
  north arrow, title, data source and date, and a disclaimer.
- Lock layers and styles for each map item ("Lock layers" / map themes) so later edits
  in the main canvas don't change finished exhibits.
- **Atlas** (Atlas › Atlas Settings) generates one page per feature — per
  neighbourhood, per rezoning site — with the map extent following each feature and
  dynamic labels like `[% "site_name" %]`.
- Export to PDF (vector) for plan documents; check text remains selectable and fonts embed.

## Gotchas
- Buffer distance uses layer CRS units: buffering in EPSG:4326 gives degrees.
- Joins are virtual until you save them as a new layer (Processing › Join by field value).
- Area of parcels from the cadastre may differ from titled area — don't use GIS area
  for legal purposes.
- Plugins and expression functions vary between QGIS LTR versions; note the version on exhibits.

## Verify
- [ ] Project in a projected CRS; data in GeoPackage; relative paths on.
- [ ] Zoning layer passes gap/overlap checks.
- [ ] Spatial queries saved as models or documented expressions.
- [ ] Exhibits use the shared style, show source, date and disclaimer.

*Uncertainty:* menu paths reflect QGIS 3.x LTR; some functions (e.g. `overlay_nearest`)
need 3.16+.
