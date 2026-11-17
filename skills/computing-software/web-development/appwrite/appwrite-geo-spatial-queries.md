---
id: computing-software.web-development.appwrite.appwrite-geo-spatial-queries
name: appwrite-geo-spatial-queries
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, geo, spatial, queries, tablesdb]
level: advanced
status: docs-checked
description: "Store points, lines and polygons and run distance and spatial relationship queries with spatial indexes."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/geo-queries/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/queries/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: location features such as nearby search and geofencing.

Coordinates are `[longitude, latitude]` arrays, which is easy to reverse. Distance measurements can be specified in meters or degrees.

Spatial columns (first-class types): `point` (one coordinate), `line` (a series of connected coordinates forming a path or route) and `polygon` (a closed area: first and last points are the same, with optional holes that lie completely inside the boundary with no overlaps).

Index: create spatial indexes on columns you will query, through the Console, a Server SDK or the CLI. The docs strongly recommend it if you query spatial data in any way.

Query operations (see the Queries page for each):
- Distance: `Query.distanceEqual`, `distanceNotEqual`, `distanceGreaterThan`, `distanceLessThan`, for example `Query.distanceEqual("location", [-73.9851, 40.7589], 200)`.
- Relationships: `intersects`, `notIntersects`, `overlaps`, `notOverlaps`, `touches`, `notTouches`, `crosses`, `notCrosses`, taking a geometry such as a coordinate list for a polygon.
- The helpers `equal`, `notEqual`, `contains` and `notContains` also work on spatial columns.

Use cases from the docs: bus stops within 200 meters, geofencing delivery vehicles, service area coverage, matching addresses to administrative boundaries, asset tracking and compliance zones.

Gotcha: self-hosted instances must choose MariaDB as the database to use geo queries; self-hosted instances using MongoDB do not currently support spatial columns or indexes.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages Geo queries and Queries: coordinate order, units, the three column types and polygon rules, spatial index advice, the operation names, the helper note, use cases and the self-hosting database restriction. Removed: the claim that an unclosed polygon or overlapping holes is rejected (the page states the rules but not the error), the "ordered list" wording for lines, and the Verify step.
Method: documentation only; no commands were run.
