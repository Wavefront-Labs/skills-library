---
id: computing-software.search-and-information-retrieval.meilisearch.filter-by-geo-bounding-box
name: filter-by-geo-bounding-box
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [geo-bounding-box, map-viewport, geo-filter, meilisearch]
level: practitioner
status: docs-checked
description: "Filter Meilisearch results to a map viewport rectangle with _geoBoundingBox([topRightLat, topRightLng], [bottomLeftLat, bottomLeftLng])."
sources: ["https://www.meilisearch.com/docs/capabilities/geo_search/how_to/filter_by_geo_bounding_box"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filter by geo bounding box

Syntax: `_geoBoundingBox([topRightLat, topRightLng], [bottomLeftLat, bottomLeftLng])`. The first pair is the north-east corner, the second the south-west corner, so top-right latitude and longitude should exceed the bottom-left ones.

Example filter: `_geoBoundingBox([45.494181, 9.214024], [45.449484, 9.179175]) AND type = pizza`; it can be combined with AND/OR like any filter.

## Map UIs

When the user pans or zooms, read the visible bounds from the map library and pass them in. From the docs: take `bounds.getNorthEast()` and `bounds.getSouthWest()` and build the filter string `_geoBoundingBox([ne.lat, ne.lng], [sw.lat, sw.lng])`, searching with an empty query to list everything visible.

## Distance note

Without `_geoRadius` or `_geoPoint` sorting there is no reference point, so `_geoDistance` in hits is 0.

## Checked

2026-11-03. Confirmed claim by claim against the Filter by geo bounding box page on the Meilisearch documentation site (names, defaults, limits, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
