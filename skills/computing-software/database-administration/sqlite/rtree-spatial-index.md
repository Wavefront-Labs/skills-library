---
id: computing-software.database-administration.sqlite.rtree-spatial-index
name: rtree-spatial-index
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, rtree, spatial-index, sqlite-query-planner, bounding-box, geospatial]
level: practitioner
status: verified
description: "Use the SQLite R*Tree virtual table for fast bounding-box and range-overlap queries (maps, time intervals), joined with ordinary tables, with auxiliary columns."
sources:
  - https://sqlite.org/rtree.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# R*Tree spatial index

**Goal:** "which items intersect this rectangle/interval?" in milliseconds over millions of rows. The R*Tree module is included in most builds (`SQLITE_ENABLE_RTREE`; check `PRAGMA compile_options`).

## Create and fill
```sql
CREATE VIRTUAL TABLE poi_idx USING rtree(
  id,               -- integer primary key, matches poi.id
  min_x, max_x,     -- longitude bounds
  min_y, max_y      -- latitude bounds
);
INSERT INTO poi_idx VALUES (1, 151.20, 151.21, -33.87, -33.86);
```
1 to 5 dimensions (a 6-dimension table failed with `Too many columns for an rtree table`). Coordinates are 32-bit floats (`rtree_i32` for integers): bounds are rounded outward slightly, so results are a superset; refine with exact checks. Checked on 3.50.4: `151.20` was stored as `151.1999969` (min) and `151.21` as `151.2100067` (max); `0.1` as min and max came back as `0.0999999866` and `0.1000000015`.

## Query
```sql
SELECT p.* FROM poi p JOIN poi_idx r ON p.id = r.id
WHERE r.min_x <= 151.25 AND r.max_x >= 151.15
  AND r.min_y <= -33.80 AND r.max_y >= -33.90
  AND p.category = 'cafe';
```
The overlap pattern: item.min ≤ query.max AND item.max ≥ query.min on each axis.

## Auxiliary columns (3.24+)
```sql
CREATE VIRTUAL TABLE poi_idx USING rtree(id, min_x, max_x, min_y, max_y, +name TEXT, +category TEXT);
```
`+` columns are stored with the entry but not indexed: avoid the join for simple listings.

## Time ranges
One dimension = interval index: `rtree(id, start_ts, end_ts)` finds bookings overlapping a window far faster than B-tree on start/end for large tables.

## Gotchas
- Keep the R*Tree in sync with the base table with triggers (insert/update/delete).
- Points: store min = max.
- For true geometry (polygons, distance on the sphere), use SpatiaLite or the `geopoly` module (compiled into the 3.54.1 shell, absent from the Python 3.14 build tested: `no such module: geopoly`).

## Verify
`EXPLAIN QUERY PLAN` shows `SCAN r VIRTUAL TABLE INDEX 2:B0D1B2D3` (R*Tree constraint codes; the string seen on 3.50.4) followed by `SEARCH p USING INTEGER PRIMARY KEY (rowid=?)`; compare row counts to a brute-force query on a sample.
