---
id: computing-software.search-and-information-retrieval.typesense.geo-polygon-filter
name: geo-polygon-filter
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [geo-polygon, polygon-filter, geopolygon, typesense]
level: advanced
status: docs-checked
description: "Filter geopoints inside an arbitrary polygon in Typesense, or store areas with the geopolygon type and find those containing a point; CW or CCW ordering required."
sources: ["https://typesense.org/docs/30.2/api/geosearch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geo polygons

## Points inside a shape

Give lat, lng pairs for the vertices in `filter_by`: `location:(48.8662, 2.3255, 48.8581, 2.3209, 48.8561, 2.3448, 48.8641, 2.3469)`.

## Storing polygon areas

Define a field with type `geopolygon`, e.g. collection `territories` with `name` string and `area` geopolygon. Add documents with a flat coordinate array such as `"area": [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0]`. The vertices must be in proper clockwise or counter-clockwise order; wrong ordering gives an error.

## Which areas contain a point

`filter_by=area:(0.5, 0.5)` returns documents whose polygon contains that point, so the square above matches.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Geo Search page (https://typesense.org/docs/30.2/api/geosearch.html) and its source markdown (geo_distance_meters, polygon and sort examples). Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
