---
id: architecture-construction.cartography-geospatial-mapping.geospatial-data-management.crs-and-datum-transformations
name: crs-and-datum-transformations
category: architecture-construction
field: cartography-geospatial-mapping
product: geospatial-data-management
tags: [geospatial-data-management, crs, coordinate-reference-system, datum, datum-transformation, epsg, wkt, proj, projinfo, grid-shift, ntv2, axis-order, pyproj, gdalsrsinfo, ballpark]
level: practitioner
status: docs-checked
description: "Keep spatial data aligned with PROJ and GDAL: inspect a CRS, list candidate datum transformations, use grid shifts, and handle axis order."
sources: ["https://proj.org/en/stable/apps/projinfo.html", "https://proj.org/en/stable/usage/network.html", "https://proj.org/en/stable/usage/transformation.html", "https://proj.org/en/stable/faq.html", "https://gdal.org/en/stable/programs/gdalsrsinfo.html", "https://pyproj4.github.io/pyproj/stable/api/transformer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRS and datum transformations

**Goal:** layers that line up to the accuracy the work needs, with every coordinate
operation known and recorded.

## 1. Defining versus transforming (general practice)
Defining a CRS only changes the label on the data; transforming computes new
coordinates. Use defining only when the CRS is missing or wrong in the file, and
reproject to change CRS.

## 2. Inspect a CRS with gdalsrsinfo
`gdalsrsinfo` lists an SRS in several formats (WKT, PROJ.4 and others). Input can be any
usual GDAL/OGR form: complete WKT, PROJ.4, `EPSG:n`, or a file containing the SRS.
Useful options: `-o <out_type>` (outputs include PROJJSON and proj4), `--single-line` for
single-line WKT, `-e` to search for matching EPSG numbers.

## 3. List candidate transformations with projinfo
```bash
projinfo -s NAD27 -t EPSG:4269 --area "USA - Missouri"
```
- Between two CRS there can be several coordinate operations. `projinfo` lists them with
  their accuracy and area of use in summary form.
- Restrict by `--area <name_or_code>` or `--bbox west,south,east,north`; filter with
  `--spatial-test contains|intersects`, `--accuracy <value>` (minimum desired accuracy),
  `--hide-ballpark`, `--show-superseded`, and `--grid-check
  none|discard_missing|sort|known_available`.
- Output a PROJ pipeline with `-o PROJ`.

## 4. Grid shifts
National agencies provide grid shift files for converting between datums, such as NAD27
to NAD83. PROJ supports CTable, NTv1 and NTv2 (.gsb) formats. Shifts are interpolated
from the four grid points around the location. Several grids can be listed
(`+nadgrids=conus,alaska,...`) and each is tried in turn until one contains the point.
Pipelines can grid-shift between any two reference frames; the older cs2cs framework is
limited to shifts to WGS84.

**Missing grids:** since PROJ 7.0 grids can be fetched on demand from the CDN at
https://cdn.proj.org. Enable with `PROJ_NETWORK=ON`, `network = on` in `proj.ini`, or the
API; PROJ must be built with libcurl. Downloaded chunks are cached in `cache.db` (default
max 300 MB). `projsync` downloads whole resource files.

## 5. Axis order
PROJ follows the CRS definition, so the axis order is not always x=longitude. In doubt,
use `projinfo` and read the AXIS entries in the WKT output (EPSG:4326 lists latitude
then longitude). In pyproj, `Transformer.from_crs(..., always_xy=True)` takes and
returns the traditional GIS order: longitude, latitude for geographic CRS, easting,
northing for most projected CRS. The default is False.

## 6. Vertical
PROJ supports vertical shifts with `+geoidgrids`. When a CRS has both a horizontal
datum shift (`+towgs84` or `+nadgrids`) and `+geoidgrids` with `+geoid_crs=horizontal_crs`,
the vertical transformation is done before the horizontal one (PROJ 9.1 for
`+geoid_crs`).

## 7. Record it (general practice)
Record the CRS code, the transformation used and its accuracy, grid files, vertical
datum and processing date in metadata.

## Verify
- [ ] Every dataset has a defined CRS.
- [ ] Reprojection, not re-definition, used to change CRS.
- [ ] Chosen operation and its accuracy recorded; required grid available.
- [ ] Axis order confirmed.

## Checked
2026-11-09. Confirmed on the PROJ, GDAL and pyproj pages in sources: all options,
defaults and behaviours above. Sections 1 and 7 are general practice, not page claims.
Removed because not on pages read: coordinate-magnitude and offset heuristics, Helmert
accuracy figures, plate motion rates, epoch and realisation advice, Web Mercator
warnings, US survey foot details, QGIS and ArcGIS Pro dialogs, the `proj-data` package,
and the EPSG and IOGP sources.
Method: documentation only; no commands were run.
