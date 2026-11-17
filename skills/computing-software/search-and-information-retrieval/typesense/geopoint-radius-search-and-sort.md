---
id: computing-software.search-and-information-retrieval.typesense.geopoint-radius-search-and-sort
name: geopoint-radius-search-and-sort
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [geopoint, radius-filter, geo-sort, typesense]
level: practitioner
status: docs-checked
description: "Index geopoint fields as [lat, lng] and filter within a radius in km or mi via filter_by, sort nearest first with sort_by, and read geo_distance_meters."
sources: ["https://typesense.org/docs/30.2/api/geosearch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geo radius search and distance sort

Fields of type `geopoint` (or `geopoint[]`) hold latitude and longitude. A schema example: a `places` collection with `title` string, `points` int32 and `location` geopoint, with `default_sorting_field` `points`.

## Documents

`{"title": "Louvre Museuem", "points": 1, "location": [48.86093481609114, 2.33698396872901]}`. Order is `[Latitude, Longitude]`; GeoJSON often uses longitude first, which is invalid here.

## Filter and sort

`filter_by=location:(48.90615915923891, 2.3435897727061175, 5.1 km)` finds records within the radius; units are `km` or `mi` (e.g. `2 mi`). Order by closeness with `sort_by=location(48.853, 2.344):asc`; the sort point may differ from the filter centre. Example: `q=*`, `query_by=title`.

Each hit then carries `geo_distance_meters`, e.g. `{"location": 1020}`.

Note that curl needs `--data-urlencode` for these values with `-G`.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Geo Search page (https://typesense.org/docs/30.2/api/geosearch.html) and its source markdown (geo_distance_meters, polygon and sort examples). Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
