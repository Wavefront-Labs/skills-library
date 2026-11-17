---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-composite-and-spatial-indexes
name: cosmos-composite-and-spatial-indexes
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-composite-and-spatial-indexes, cosmos-indexing, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Support multi-property ORDER BY and geospatial queries."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-policy
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite and spatial indexes

**Goal:** Support multi-property ORDER BY and geospatial queries.

## Steps
- ORDER BY on two or more properties needs a composite index: "compositeIndexes":[[{"path":"/status","order":"ascending"},{"path":"/createdAt","order":"descending"}]]
- Filters with equality on one property and range on another benefit from composite indexes too.
- No spatial indexes are created by default; to use spatial built-in functions, define a spatial index on the property in the indexing policy. Types include Point, Polygon and MultiPolygon.
- Vector indexes (flat, quantizedFlat, diskANN) are defined in the vectorIndexes section of the indexing policy; see cosmos-vector-search-setup.

## Gotcha
Composite index property order and sort direction must match the query's ORDER BY.

## Checked

2026-11-03. Confirmed against the "Indexing policies" page: ORDER BY on two or more properties needs a composite index, composite path order and direction must match ORDER BY, equality and range queries benefit, no spatial indexes by default, spatial types, vector index types. The /status and /createdAt paths in the example are illustrative.
Removed: ST_DISTANCE/ST_WITHIN and the spatialIndexes key name (not on the page).
Method: documentation only; no commands were run.

## Verify
- [ ] The multi-property ORDER BY query succeeds and its RequestCharge drops.
