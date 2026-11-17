---
id: computing-software.database-administration.postgresql.postgis-installation-and-spatial-indexing
name: postgis-installation-and-spatial-indexing
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgis, gist-index, spatial-index, geography, srid, st-dwithin, postgis-upgrade]
level: practitioner
status: docs-checked
description: "Install PostGIS, pick geometry vs geography and SRID, build GiST spatial indexes, write index-friendly ST_DWithin queries, and upgrade PostGIS safely."
sources:
  - https://postgis.net/documentation/
  - https://postgis.net/docs/using_postgis_dbmanagement.html
  - https://postgis.net/workshops/postgis-intro/indexing.html
  - https://postgis.net/docs/postgis_administration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostGIS installation and spatial indexing

## Install
Install the PostGIS packages for your platform and PostgreSQL major version first (see the PostGIS install docs).
```sql
CREATE EXTENSION postgis;                    -- per database
SELECT postgis_full_version();               -- reports versions and whether an upgrade is needed
```
Optional: `postgis_raster`, `postgis_topology` as separate extensions.

## Types and SRIDs
| Type | Units | Use |
|---|---|---|
| `geometry(Point, 4326)` | degrees (planar math on lat/lon is wrong for distance) | storage, bbox ops; transform for measurements |
| `geography(Point, 4326)` | metres on the spheroid | global distances, fewer functions, slower |

Always declare the type modifier so the column enforces one SRID.

## Spatial index
```sql
CREATE INDEX CONCURRENTLY places_geom_gix ON places USING gist (geom);
ANALYZE places;
```
BRIN and SP-GiST indexes also exist; see the PostGIS manual's index chapter for when to use them. For a live table, `CREATE INDEX CONCURRENTLY` avoids blocking writes.

## Index-friendly queries
```sql
-- geography distance arguments are in metres
SELECT id FROM places WHERE ST_DWithin(geog, ST_MakePoint(-0.12, 51.5)::geography, 1000);
```

## Upgrading PostGIS
```sql
SELECT postgis_extensions_upgrade();   -- after installing new PostGIS packages, per database
```
The administration chapter says to use this function for PostGIS 3 and later.

## Gotchas
- Large polygons hurt index selectivity; `ST_Subdivide` them into a helper table.
- Loading shapefiles: `shp2pgsql` generates SQL (`-s` sets the SRID, `-I` creates a GiST index); pipe it to psql.

## Checked

2026-10-28. Confirmed against PostGIS docs (administration and data management chapters): CREATE EXTENSION postgis, postgis_raster, postgis_topology, postgis_full_version, postgis_extensions_upgrade for PostGIS 3+, GiST / BRIN / SP-GiST index types, CREATE INDEX CONCURRENTLY, geography distances in metres, ST_DWithin on geography, ST_Subdivide for large geometries, shp2pgsql. Removed unconfirmed: package names, address_standardizer, 3857/UTM table row, KNN <-> and ST_Distance/ST_Transform index claims, mixed-SRID error text, pg_upgrade ordering advice, ogr2ogr.

Method: documentation only; no commands were run.
