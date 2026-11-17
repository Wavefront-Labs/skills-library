---
id: computing-software.search-and-information-retrieval.apache-solr.spatial-geofilt
name: spatial-geofilt
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [spatial, spatial-search, geofilt, bbox, latlonpointspatialfield, geodist]
level: practitioner
status: docs-checked
description: "Search by location in Solr with LatLonPointSpatialField: geofilt and bbox filters (sfield, pt, d in kilometers), geodist sorting, and when to choose RPT or BBoxField."
sources:
  - https://solr.apache.org/guide/solr/latest/query-guide/spatial-search.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# spatial-geofilt

Four spatial field types: `LatLonPointSpatialField` (ideal for most lat/lon point data; docValues on by default), `PointType`, `SpatialRecursivePrefixTreeFieldType` (RPT, with `RptWithGeometrySpatialField` for polygons, non-point shapes and heatmaps) and `BBoxField` (indexed boxes with predicates Intersects, Within, Contains, Disjoint, Equals).

Schema: `<fieldType name="location" class="solr.LatLonPointSpatialField" docValues="true"/>`.

Filtering uses two query parsers with the same parameters: `sfield` (the field), `pt` (center, lat,lon) and `d` (radial distance, in kilometers by default):
- `fq={!geofilt sfield=store}&pt=45.15,-93.85&d=5` - circle (great circle distance).
- `fq={!bbox sfield=store}&pt=45.15,-93.85&d=5` - bounding box of that circle, faster but may return points outside the radius.

RPT and BBoxField can set other units with `distanceUnits`.

For sorting or boosting by distance use `geodist()`, usually the most appropriate function, for example `sort=geodist() asc` with `sfield` and `pt` set.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Spatial Search page: the four field types and their roles, the `LatLonPointSpatialField` schema line, `geofilt` and `bbox` parameters, kilometers and `distanceUnits`, the bounding-box trade-off, and `geodist()` for sorting. Removed the closing claim about complex shapes, which the page does not state in that form.

Method: documentation only; no commands were run.
