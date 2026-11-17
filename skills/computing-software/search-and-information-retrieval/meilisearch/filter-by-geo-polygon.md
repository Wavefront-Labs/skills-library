---
id: computing-software.search-and-information-retrieval.meilisearch.filter-by-geo-polygon
name: filter-by-geo-polygon
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [geo-polygon, delivery-zones, geo-filter, meilisearch]
level: practitioner
status: docs-checked
description: "Filter Meilisearch results to an arbitrary polygon with _geoPolygon, needing 3+ vertices, auto-closing, no transmeridian shapes, combinable with radius or box."
sources: ["https://www.meilisearch.com/docs/capabilities/geo_search/how_to/filter_by_geo_polygon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filter by geo polygon

`_geoPolygon([lat1, lng1], [lat2, lng2], [lat3, lng3], ...)` matches documents inside a custom shape, useful for delivery zones, school districts or sales territories that a circle or rectangle cannot express.

- At least 3 coordinate pairs are required.
- The polygon closes automatically from the last point to the first; do not repeat the first vertex.
- Use as many vertices as needed. A triangle example: `_geoPolygon([45.490, 9.170], [45.490, 9.210], [45.450, 9.190])`.
- Polygons crossing the 180th meridian are unsupported. Split them in two and run each query separately.

## Combining

AND/OR with other conditions, for example `... AND type = pizza`, or with other geo filters such as `_geoPolygon(...) AND _geoRadius(45.472735, 9.184019, 1000)` for tighter targeting.

In the docs example output, hits from a polygon filter show `_geoDistance` of 0.

## Checked

Method: docs-checked 2026-11-09 against the Filter by geo polygon page (raw mdx of github.com/meilisearch/documentation, read in full). Dropped the unconfirmed explanation of why `_geoDistance` is 0.