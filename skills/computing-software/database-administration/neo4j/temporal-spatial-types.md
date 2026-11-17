---
id: computing-software.database-administration.neo4j.temporal-spatial-types
name: temporal-spatial-types
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, datetime, duration, point-type, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Dates, durations and points"
sources:
  - https://neo4j.com/docs/cypher-manual/current/values-and-types/temporal/
  - https://neo4j.com/docs/cypher-manual/current/functions/spatial/
  - https://neo4j.com/docs/cypher-manual/current/functions/temporal/duration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temporal and spatial types

Goal: use rich types correctly.
- `datetime()` creates a zoned datetime; `duration({days: 14, hours: 16, minutes: 12})` builds a duration.
- `point({latitude: 55.67, longitude: 12.56})` and `point.distance(from, to)` for geospatial distance.
Verify: results match a hand-checked example.

## Checked

2026-11-02. Confirmed: `datetime()`, `duration({...})`, `point.distance()` syntax and latitude/longitude keys (temporal, spatial, duration pages). Removed: native-type and indexing advice, `date()` arithmetic and the time-zone verification claim.
Method: documentation only; no commands were run.
