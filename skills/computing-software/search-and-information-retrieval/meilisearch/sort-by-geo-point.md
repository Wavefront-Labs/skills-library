---
id: computing-software.search-and-information-retrieval.meilisearch.sort-by-geo-point
name: sort-by-geo-point
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [geo-point-sort, nearest-first, geo-distance, meilisearch]
level: practitioner
status: docs-checked
description: "Sort Meilisearch results by distance with _geoPoint(lat, lng):asc or desc, chain tiebreakers, and pair with _geoRadius filters."
sources: ["https://www.meilisearch.com/docs/capabilities/geo_search/how_to/sort_by_geo_point"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sort by geo point

Add `_geoPoint(lat, lng):asc` to the `sort` array to order hits nearest first, or `:desc` for farthest first. Each hit then carries `_geoDistance`, the distance in meters from your reference point. That field is computed only in results and cannot be filtered or sorted on.

Example: sort by distance from the Eiffel Tower (48.8561446, 2.2978204) with `"sort": ["_geoPoint(48.8561446, 2.2978204):asc"]`.

## Chaining

Sort rules apply in order, so later entries break ties: `_geoPoint(...)` first, then `rating:desc`.

## With filters

Restrict and order at once: `"filter": "_geoRadius(45.472735, 9.184019, 5000)"` together with `"sort": ["_geoPoint(45.472735, 9.184019):asc"]` returns documents within 5 km, nearest first.

## Checked

Method: docs-checked 2026-11-09 against the Sort by geo point page (raw mdx of github.com/meilisearch/documentation, read in full). Dropped the unconfirmed claims about sort ranking rule position and `_geojson`.