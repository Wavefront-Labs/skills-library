---
id: computing-software.database-administration.redis.geospatial-indexes-geoadd-geosearch
name: geospatial-indexes-geoadd-geosearch
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, valkey, geospatial, geoadd, geosearch, geosearchstore, nearby-search, geohash]
level: practitioner
status: docs-checked
description: "Build nearby-search features on Redis geo indexes with GEOADD, GEOSEARCH and GEOSEARCHSTORE, including limits, storage as a sorted set, and scaling patterns."
sources:
  - https://redis.io/docs/latest/commands/geoadd/
  - https://redis.io/docs/latest/commands/geosearch/
  - https://redis.io/docs/latest/commands/geosearchstore/
  - https://redis.io/docs/latest/develop/ai/search-and-query/query/geo-spatial/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geospatial indexes (GEOADD / GEOSEARCH)

**Goal:** "nearest 20 drivers within 3 km" lookups in sub-millisecond time.

## Add
```text
GEOADD drivers 151.2093 -33.8688 driver:17          # longitude first, then latitude
GEOADD drivers XX CH 151.2101 -33.8702 driver:17    # update only existing, return changed count (NX/XX/CH need 6.2+)
```
Valid longitudes are -180 to 180 and valid latitudes are -85.05112878 to 85.05112878 degrees (EPSG:900913 limits,
areas very near the poles are not indexable); other values return an error.

## Search (6.2+)
```text
GEOSEARCH drivers FROMLONLAT 151.2070 -33.8650 BYRADIUS 3 km ASC COUNT 20 ANY WITHDIST WITHCOORD
GEOSEARCH drivers FROMMEMBER driver:17 BYBOX 4 4 km ASC
GEOSEARCHSTORE nearby:req:99 drivers FROMLONLAT 151.2 -33.86 BYRADIUS 5 km STOREDIST
```
- `COUNT n ANY` returns as soon as n matches are found (faster, results may be unsorted and not the nearest).
  Without `ANY`, effort grows with the number of items in the area, so a huge area with a tiny `COUNT` can be slow.
- `GEORADIUS`/`GEORADIUSBYMEMBER` are deprecated in favour of `GEOSEARCH`/`GEOSEARCHSTORE`.
- `GEOSEARCHSTORE` writes the result to a destination sorted set; with `STOREDIST` the score is the distance from
  the centre instead of the geohash. In Redis Cluster the destination and source must share a hash slot.
- Units are `m`, `km`, `ft`, `mi`. `WITHHASH` returns the raw 52-bit geohash score.
- `GEODIST drivers driver:17 driver:22 km`, `GEOPOS`, `GEOHASH` are helpers.

## How it is stored
A sorted set whose score is a 52-bit integer made by interleaving latitude and longitude bits (a geohash).
So `ZREM drivers driver:17` removes a point and `ZCARD` counts them; there is no `GEODEL`. Distances use the
haversine formula on a sphere; the worst-case error is about 0.5%, so use something else for error-critical work.

## Patterns
- Moving objects: re-`GEOADD` on each position update; keep a separate hash for metadata and a TTL'd "last seen" key, and remove stale members with a sweeper (members cannot expire individually).
- Shard by city/region key to keep sets small: `drivers:{syd}`.

## Limits
Search complexity is O(N+log(M)) where N is the number of elements in the grid-aligned bounding box around the
shape and M the number inside the shape: very large radii over dense sets are slow. For polygon shapes, attribute
filters, or combined text and geo queries, use the Redis Query Engine; its GEOSHAPE field type (points and
polygons, `WITHIN`/`CONTAINS`/`INTERSECTS`/`DISJOINT` queries, not available in DIALECT 1) needs Redis 7.2 or later.

## Verify
Cross-check a few `WITHDIST` results against a known distance calculator; `SLOWLOG` shows searches within budget at peak.

## Checked
Date 2026-10-22. Redis documentation (redis.io, latest, which covers Redis 8): GEOADD, GEOSEARCH, GEOSEARCHSTORE,
Query Engine geospatial pages. Confirmed: argument order and ranges, `NX`/`XX`/`CH` since 6.2.0, GEOSEARCH and
GEOSEARCHSTORE since 6.2.0, `ANY` semantics, deprecation of GEORADIUS, sorted-set storage and no GEODEL, 52-bit geohash,
0.5% haversine error, complexity, GEOSHAPE needs 7.2+. Removed: the "about 0.6 m" precision figure (not documented).
The multi-key page lists GEOSEARCHSTORE as single-slot in a cluster.
Method: documentation only; no commands were run.
