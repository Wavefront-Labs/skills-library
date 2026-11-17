---
id: computing-software.search-and-information-retrieval.meilisearch.use-geojson-format
name: use-geojson-format
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [geojson, multipolygon, geo-shapes, meilisearch]
level: advanced
status: docs-checked
description: "Index Point, Polygon and MultiPolygon shapes in Meilisearch with the _geojson field, noting lng-lat order, no holes, no CSV and no _geoPoint sorting."
sources: ["https://www.meilisearch.com/docs/capabilities/geo_search/how_to/use_geojson_format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Use GeoJSON

Add a `_geojson` field (a GeoJSON Feature with a `geometry`) to documents that represent areas, such as neighbourhoods, properties or delivery zones. Supported geometries: `Point`, `Polygon`, `MultiPolygon`.

## Details

- Coordinate order is longitude first, then latitude (`[9.1967508, 45.4777599]`), opposite to `_geo` which names `lat` and `lng`.
- A Polygon's `coordinates` holds linear rings; the first is the outer boundary and the last coordinate repeats the first to close it.
- Use MultiPolygon when one document covers several separate areas.
- Holes are unsupported: inner rings are ignored and the polygon is solid.

## Search behaviour

Add `_geojson` to `filterableAttributes`, then filter with `_geoRadius`, `_geoBoundingBox` or `_geoPolygon`. Meilisearch tests whether the filter area intersects the document geometry.

If a document has both `_geo` and `_geojson`: `_geo` serves `_geoPoint` sorting, `_geojson` serves `_geoPolygon` filtering, and both are matched by `_geoRadius` and `_geoBoundingBox`.

## Limitations

- Transmeridian shapes are unsupported; split into two shapes grouped as MultiPolygon or MultiLine.
- No `_geoPoint` sorting on `_geojson` data.
- CSV import does not support `_geojson`; use JSON or NDJSON.

## Checked

2026-11-03. Confirmed claim by claim against the Use GeoJSON format page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
