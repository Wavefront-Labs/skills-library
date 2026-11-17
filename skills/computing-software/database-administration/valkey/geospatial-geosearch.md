---
id: computing-software.database-administration.valkey.geospatial-geosearch
name: geospatial-geosearch
category: computing-software
field: database-administration
product: valkey
tags: [geospatial, geoadd, geosearch, bypolygon, byradius, location]
level: intro
status: docs-checked
description: "Valkey geospatial indexes: GEOADD (longitude first) and GEOSEARCH by radius or BYPOLYGON, with WITHDIST, for nearby-point queries."
sources:
  - https://valkey.io/topics/geospatial/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A geospatial index stores coordinates and finds points within a radius, bounding box or polygon.

Commands:
- `GEOADD key longitude latitude member` adds a location. Longitude comes before latitude, the opposite of most map apps.
- `GEOSEARCH` returns members inside a search area.

Example from the page, bike rental stations:
```
GEOADD bikes:rentable -122.27652 37.805186 station:1
GEOADD bikes:rentable -122.2674626 37.8062344 station:2
GEOADD bikes:rentable -122.2469854 37.8104049 station:3
GEOSEARCH bikes:rentable FROMLONLAT -122.2612767 37.7936847 BYRADIUS 5 km WITHDIST
```
The radius search returns each station with its distance in the chosen unit (1.8523, 1.4979 and 2.2441 km in the example). `FROMLONLAT` gives the centre point; `BYRADIUS 5 km` the shape; `WITHDIST` adds the distance to each reply.

For irregular areas use `BYPOLYGON` with a vertex count followed by that many longitude latitude pairs. The page example passes `BYPOLYGON 5` and five coordinate pairs enclosing downtown Oakland, and it returns `station:1` and `station:2`.

The full list of geo commands is under the GEO group in the command reference.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/geospatial/ (page text read in full): GEOADD with longitude before latitude, GEOSEARCH radius/bounding box/polygon, the three station coordinates, FROMLONLAT BYRADIUS 5 km WITHDIST output (1.8523, 1.4979, 2.2441), BYPOLYGON 5 example returning station:1 and station:2.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
