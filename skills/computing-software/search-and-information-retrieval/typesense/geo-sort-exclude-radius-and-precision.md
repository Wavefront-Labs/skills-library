---
id: computing-software.search-and-information-retrieval.typesense.geo-sort-exclude-radius-and-precision
name: geo-sort-exclude-radius-and-precision
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [exclude-radius, geo-precision, geo-tie-break, typesense]
level: advanced
status: docs-checked
description: "Combine geo distance with another sort field in Typesense using exclude_radius or precision buckets so near results tie on distance and fall back to popularity."
sources: ["https://typesense.org/docs/30.2/api/geosearch.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# exclude_radius and precision

Plain geo sorting orders strictly by distance, so a second sort field never matters. Two options inside the geo sort expression let it break ties.

## exclude_radius

`sort_by=location(48.853, 2.344, exclude_radius: 2mi):asc, popularity:desc`. Every document within 2 miles ties on distance, so `popularity:desc` orders them. Documents outside that radius sort by distance first, then by popularity.

## precision

`sort_by=location(48.853, 2.344, precision: 2mi):asc, popularity:desc`. Results are bucketed into 2 mile groups; documents in the same bucket tie on geo score, so popularity decides order within each bucket.

Both take distances with `mi` or `km` units, as in geo filters.

## Checked

2026-11-03. Every endpoint, parameter, default, example value and behaviour above was read in the Typesense 30.2 Geo Search page (https://typesense.org/docs/30.2/api/geosearch.html) and its source markdown (geo_distance_meters, polygon and sort examples). Removed or reworded claims the pages do not state.

Method: documentation only; no commands were run.
