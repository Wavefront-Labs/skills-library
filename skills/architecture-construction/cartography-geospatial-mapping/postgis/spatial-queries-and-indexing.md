---
id: architecture-construction.cartography-geospatial-mapping.postgis.spatial-queries-and-indexing
name: spatial-queries-and-indexing
category: architecture-construction
field: cartography-geospatial-mapping
product: postgis
tags: [postgis, postgresql, spatial-database, spatial-sql, sql, geometry, geography, srid, st_transform, st_intersects, st_dwithin, st_contains, st_buffer, st_union, st_makevalid, st_isvalid, st_subdivide, gist-index, spatial-index, explain-analyze, knn, nearest-neighbour, ogr2ogr, shp2pgsql, gdal, typmod, geometry-columns, vacuum-analyze, bounding-box, operator]
level: practitioner
status: docs-checked
description: "Write fast PostGIS queries: ogr2ogr loading with a GiST index, index-using predicates like ST_DWithin, <-> nearest neighbour, validity, ST_Subdivide."
sources: ["https://postgis.net/docs/ST_DWithin.html", "https://postgis.net/docs/geometry_distance_knn.html", "https://postgis.net/docs/ST_Subdivide.html", "https://gdal.org/en/stable/drivers/vector/pg.html", "https://gdal.org/en/stable/programs/ogr2ogr.html", "https://postgis.net/docs/ST_Intersects.html", "https://postgis.net/docs/ST_Contains.html", "https://postgis.net/docs/ST_Transform.html", "https://postgis.net/docs/ST_MakeValid.html", "https://postgis.net/docs/ST_IsValidReason.html", "https://postgis.net/docs/ST_Area.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# PostGIS spatial queries and indexing

**Goal:** spatial SQL that returns correct answers quickly, which in PostGIS mostly means
a GiST index and predicates that can use it.

## 1. Columns and SRIDs
```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE parcels (
  id     bigserial PRIMARY KEY,
  parcel_ref text NOT NULL,
  geom   geometry(MultiPolygon, 27700) NOT NULL   -- type + SRID declared
);
```
- Declare the geometry type and SRID on the column.
- `ST_Area` on geometry is a 2D planar area in units specified by the SRID, so store or
  transform to a projected CRS in metres for metric areas. For `geography`, area is
  computed on a spheroid in square metres by default.
- Transform at query time with `ST_Transform(geom, 4326)` for output.

## 2. Loading data
```bash
ogr2ogr -f PostgreSQL PG:"dbname=<DB> host=<HOST> user=<USER>" parcels.gpkg \
  -nln parcels -nlt PROMOTE_TO_MULTI -lco GEOMETRY_NAME=geom \
  -t_srs EPSG:27700 -lco SPATIAL_INDEX=GIST
```
- `-nlt PROMOTE_TO_MULTI` converts geometries to their multi form (documented for ogr2ogr).
- `-lco GEOMETRY_NAME=value` names the geometry column (default `wkb_geometry`).
- `-lco SPATIAL_INDEX=[NONE/GIST/SPGIST/BRIN]` defaults to GIST and has effect only when
  PostGIS is available.

## 3. Index
```sql
CREATE INDEX parcels_geom_gix ON parcels USING GIST (geom);
```
`ST_Intersects`, `ST_Contains` and `ST_DWithin` each include a bounding-box comparison
that makes use of any spatial indexes available on the geometries. To avoid index use
with `ST_Contains`, call `_ST_Contains`.

## 4. Write index-friendly predicates
- **Distance filter:** `WHERE ST_DWithin(a.geom, b.geom, 50)` uses indexes; the
  `ST_DWithin` reference page describes `ST_Distance` as non-indexable, so use
  `ST_DWithin` to limit the candidate list.
- **Transformations:** the `ST_Transform` page advises a functional index on commonly
  used transformations to take advantage of index usage.
- **Nearest neighbour:** `<->` returns the 2D distance and gives index-assisted
  nearest-neighbour results when used in `ORDER BY`; the index is used only in `ORDER BY`,
  and only when one of the geometries is a constant rather than a subquery or CTE:
  ```sql
  SELECT id, name FROM streets
  ORDER BY geom <-> 'SRID=3005;POINT(1011102 450541)'::geometry LIMIT 10;
  ```
- Check query plans with `EXPLAIN ANALYZE` to confirm the index is used.

## 5. Validity and large geometries
- `SELECT id, ST_IsValidReason(geom) FROM parcels WHERE NOT ST_IsValid(geom);`
  `ST_IsValidReason` returns text saying whether a geometry is valid or why not.
- `ST_MakeValid` attempts to make an invalid geometry valid without losing vertices and
  returns valid geometries unchanged. After dimensional collapse the output may be a
  collection of lower-to-equal dimension geometries or a lower-dimension geometry, so
  check the result type.
- `ST_Contains` should not be used with invalid geometries: results are unexpected.
- `ST_Subdivide(geom, max_vertices)` divides a geometry into parts with no more than
  `max_vertices` each (default 256; must be 5 or more). Spatial operations are normally
  faster on indexed subdivided data because the part bounding boxes cover smaller areas
  and the index recheck handles fewer points.

## Gotchas
- Keep credentials out of command lines and scripts; use your PostgreSQL client's password file or environment variables.

## Verify
- [ ] Geometry columns declare a type and SRID.
- [ ] A GiST index exists and the query plan uses it.
- [ ] Distance filters use `ST_DWithin`, not `ST_Distance` in WHERE.
- [ ] No invalid geometries remain (`ST_IsValid` all true) before overlay or containment.
- [ ] Areas computed in a projected CRS in known units, or on geography.

## Checked
2026-11-09. Confirmed against the PostGIS reference pages for ST_DWithin, ST_Intersects, ST_Contains, ST_Transform, ST_MakeValid, ST_IsValidReason, ST_Area, ST_Subdivide and geometry_distance_knn (the `<->` operator), and the GDAL PostgreSQL driver and ogr2ogr pages (GEOMETRY_NAME, SPATIAL_INDEX, PROMOTE_TO_MULTI). Removed unconfirmed claims: mixed-SRID error behaviour, the LATERAL nearest-neighbour join (the KNN page says the index needs a constant), VACUUM ANALYZE advice, buffer-versus-DWithin and function-wrapping rules, GEOS TopologyException, and EXPLAIN plan node names.
Method: documentation only; no commands were run.
