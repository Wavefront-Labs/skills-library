---
id: architecture-construction.cartography-geospatial-mapping.qgis.atlas-map-series-print-layout
name: atlas-map-series-print-layout
category: architecture-construction
field: cartography-geospatial-mapping
product: qgis
tags: [qgis, open-source-gis, print-layout, atlas, map-series, map-book, coverage-layer, grid-index, index-map, overview-map, map-item, controlled-by-atlas, atlas-scale, fixed-scale, margin-around-feature, expressions, attribute-filter, dynamic-labels, map-theme, scale-bar, north-arrow, legend-filter, export-pdf, page-name, layout-template, qpt, data-defined-override, grid-annotation]
level: practitioner
status: draft
description: "Produce a map series in QGIS with the atlas: build a grid or feature coverage layer, drive map extent and scale, add dynamic titles and overview maps, filter legends, and export page-named PDFs."
sources: ["QGIS User Guide: Print layouts and Generate an Atlas", "QGIS expression reference (@atlas_* variables)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Atlas map series in QGIS print layouts

**Goal:** one layout that generates a consistent book of maps — one page per grid
square, parcel, district or asset — with titles, scales and overview maps that update
automatically, instead of hand-making 80 nearly identical layouts.

## 1. Build the coverage layer
The atlas iterates over features of a **coverage layer**.
- **Grid series:** *Vector › Research Tools › Create Grid* (or Processing *Create grid*)
  in a projected CRS; cell size = map frame size on paper × scale. Example: a 250 × 180 mm
  frame at 1:5,000 covers 1,250 × 900 m → cell 1,250 × 900 m. Clip/select to cells
  intersecting the area of interest and add a `sheet_id` field (e.g. row letter + column number).
- **Feature series:** use the features themselves (districts, parcels); add a sort field.
- Optional: a `page_name` field for output filenames and an `atlas_scale` field if pages
  need different fixed scales.

## 2. Configure the atlas
*Layout › Atlas Settings* (Atlas panel):
- Coverage layer; *Hidden coverage layer* if the grid shouldn't print.
- **Page name** expression (e.g. `"sheet_id"`), sort by a field, optional filter
  expression (e.g. `"status" = 'active'`).
- Open the *Atlas* toolbar to preview pages.

## 3. Map item controlled by atlas
In the main map item's properties tick **Controlled by Atlas** and choose:
- **Margin around feature** (e.g. 10%) for variable-size features — scale varies per page.
- **Predefined scale (best fit)** to snap to a list of nice scales (set in Project
  Properties › General › project scales).
- **Fixed scale** for grid series — every sheet identical scale, which is what map books
  normally need.
Lock layers / use a **map theme** for the main map so later layer toggles in the canvas
don't change printed pages.

## 4. Dynamic elements
- Title label with an expression: `[% 'Sheet ' || "sheet_id" || ' – ' || "name" %]`.
- Page counter: `[% @atlas_featurenumber || ' of ' || @atlas_totalfeatures %]`.
- Scale bar and grid linked to the main map item update automatically.
- **Overview/index map**: second map item at small scale, *Overviews* tab → frame =
  main map. Style the coverage layer in it with a rule highlighting the current feature:
  `@atlas_featureid = $id`.
- Adjacent sheet references: label neighbours in the overview, or compute with
  `aggregate`/`overlay_touches` expressions. *Expression functions vary by QGIS version.*
- **Highlight the current feature** in the main map with a data-defined style:
  `CASE WHEN $id = @atlas_featureid THEN ... ELSE ... END`, or mask outside features.

## 5. Legend
In the legend item, tick **Only show items inside linked map** and, where appropriate,
*Only show items inside current atlas feature* — otherwise every page lists all classes.

## 6. Export
*Export Atlas as PDF*: either one multi-page PDF or one file per page (named by the
page-name expression). Set export resolution (e.g. 300 dpi) and decide whether to force
vector output or rasterise (complex blending/effects force raster). Save the layout as a
**template (.qpt)** for reuse.

## Gotchas
- Coverage layer and project in a geographic CRS (degrees) gives distorted cells — use a
  projected CRS.
- Fixed scale + frame aspect not matching grid cell aspect → content cut or overlapping
  neighbours; compute cells from the frame.
- Labels cut at frame edges: enable label placement options to avoid partial labels, or
  accept them consistently.
- Large books are slow to export — test with a filter of 3 pages first.

## Verify
- [ ] Coverage features in a projected CRS, sized from frame × scale.
- [ ] Main map controlled by atlas at the intended scale mode, layers locked/themed.
- [ ] Title, page number and overview highlight change correctly across pages.
- [ ] Legend shows only classes present on each page.
- [ ] Test export of a few pages checked before the full run; layout saved as .qpt.
