---
id: computing-software.data-engineering.apache-pinot.apache-pinot-geospatial-h3-index
name: apache-pinot-geospatial-h3-index
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, geospatial, h3-index, st-distance, sphericalgeography, indexes-h3, resolution, geo-point]
level: advanced
status: docs-checked
description: "Pinot geospatial queries: BYTES geography column via transformFunction, H3 index resolutions, only ST_Distance in WHERE is accelerated."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/indexing/geospatial-support.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geospatial support and the H3 index

Store points as a geography value in a BYTES column built at ingestion with a transform:
```
"ingestionConfig": { "transformConfigs": [
  { "columnName": "location_st_point",
    "transformFunction": "toSphericalGeography(stPoint(lon, lat))" } ] }
```

Then index it with H3:
```
{ "name": "location_st_point", "encodingType": "RAW", "indexes": { "h3": { "resolution": [13, 5, 6] } } }
```

Facts:
- The column is `BYTES` and `RAW`; `resolution` lists H3 resolutions to build.
- The index accelerates **only** `ST_Distance` used in a WHERE clause, such as `ST_Distance(location_st_point, ST_Point(-122, 37, 1)) < 5000`.
- Other spatial predicates such as `ST_Contains` or `ST_Within` do not use the index.
- Reloading older segments that lack the source columns needs `ingestionConfig.continueOnError`.

The index finds records in nearby hexagons, then `ST_Distance` filters them exactly, so accuracy and speed depend on the configured resolutions.

## Checked

2026-11-09: confirmed against the Pinot Geospatial page (pinot-docs build-with-pinot/indexing/geospatial-support.md): BYTES column with a `toSphericalGeography(stPoint(lon,lat))` transform, RAW encoding, the `h3` index with `resolution` [13, 5, 6], the ST_Distance WHERE example, the `ingestionConfig.continueOnError` note for reloading older segments, and that only ST_Distance in WHERE uses the index. Removed the unconfirmed advice on coarse versus fine cells.

Method: documentation only; no commands were run.
