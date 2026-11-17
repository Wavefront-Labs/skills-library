---
id: computing-software.database-administration.cockroachdb.survival-goals
name: survival-goals
category: computing-software
field: database-administration
product: cockroachdb
tags: [survival-goals, zone-failure, region-failure, survive-region-failure, multi-region]
level: practitioner
status: docs-checked
description: "Choose and set CockroachDB survival goals: zone failure default versus region failure, replication factor impact, write latency cost and three-region minimum."
sources:
  - https://www.cockroachlabs.com/docs/stable/multiregion-survival-goals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick how many simultaneous failures a multi-region database must survive.

Rules:
- One survival goal per database; all its tables share it.
- Zone failure (default): reads and writes continue if one zone, or a single node, fails. Multiple zone failures in the same region can make the database unavailable.
- Region failure: stays fully available if an entire region is lost, at a write-latency cost of at least the round trip to the nearest region; read performance is unaffected.

Statements:
```sql
ALTER DATABASE <db> SURVIVE REGION FAILURE;
ALTER DATABASE <db> SURVIVE ZONE FAILURE;
```
Requirements and side effects:
- Region survival needs at least 3 database regions.
- On a cluster with 3 cluster regions, setting it raises the replication factor for the database's ranges from 3 to 5 so replicas spread so that a lost region still leaves a majority.

Decision guide from the page: use `ZONE` when you can accept up to a full zone outage and want lower write latency; use `REGION` when the database must stay available through a region outage, you can pay the latency, and you have three or more database regions.

Inspect with `SHOW REGIONS FROM DATABASE <db>;` and `SHOW ZONE CONFIGURATION FOR DATABASE <db>;` (the ALTER DATABASE page shows `num_replicas = 5` in zone output).

## Checked

2026-11-03. Confirmed against the multiregion survival goals page: zone and region goals, write-latency cost, 3 database regions minimum, replication factor 3 to 5 on a 3-region cluster. Removed: the sizing gotcha and the claim that SHOW REGIONS displays the survival goal (not on the pages read).
Method: documentation only; no commands were run.
