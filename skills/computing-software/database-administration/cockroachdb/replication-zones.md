---
id: computing-software.database-administration.cockroachdb.replication-zones
name: replication-zones
category: computing-software
field: database-administration
product: cockroachdb
tags: [replication-zones, zone-configs, configure-zone, num-replicas, constraints, lease-preferences]
level: practitioner
status: docs-checked
description: "Control replica count, placement, range size and GC with CockroachDB replication zones: levels, inheritance, ALTER ... CONFIGURE ZONE and required privileges."
sources:
  - https://www.cockroachlabs.com/docs/stable/configure-replication-zones
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune where and how many replicas of data live, using the right zone level.

What a zone controls: number of replicas, constraints on location (for example "only German availability zones"), range size limits, how long old data is kept before garbage collection, and leaseholder preferences.

Statement: `CONFIGURE ZONE` is a subcommand of `ALTER DATABASE`, `ALTER TABLE`, `ALTER INDEX`, `ALTER PARTITION` and `ALTER RANGE`. You need the `admin` role, or `CREATE` or `ZONECONFIG` privileges; system objects require `admin`.
```sql
ALTER DATABASE test CONFIGURE ZONE USING num_replicas = 1;
ALTER TABLE kv CONFIGURE ZONE USING num_replicas = 5;
```
Fields visible in the docs' `SHOW ZONE CONFIGURATION` output: `range_min_bytes` (134217728), `range_max_bytes` (536870912), `gc.ttlseconds` (14400 in the example), `num_replicas`, `constraints`, `lease_preferences`.

Levels, least to most granular: cluster `default`, database, table, index (distinct index zones need an Enterprise license), row via partitions. System ranges (meta, liveness) have their own pre-configured zones. CockroachDB always applies the most granular zone available.

Inheritance: a zone stores only the values that differ from its parent; unset fields are looked up in the parent. Once a child sets a field (the docs set the table to 5 replicas under a database at 1, then changed the database to 7), later changes to the parent no longer flow to that field. Known limitation: sub-partitions inherit from the parent table, not the parent partition.

The page cautions against manual zone config management for most users.

Verify: `SHOW ZONE CONFIGURATION FROM TABLE <name>;` shows the expected effective values.

## Checked
2026-11-03. Confirmed on the configure replication zones page: what a zone controls, the five zone levels, Enterprise licence for distinct index zones, most granular zone wins, inheritance and the sub-partition limitation, the example field values (`range_min_bytes` 134217728, `range_max_bytes` 536870912, `gc.ttlseconds` 14400), the 1 to 5 to 7 replica example, and the caution against manual zone configs. Corrected: `SHOW ZONE CONFIGURATION FROM TABLE` is the form the page uses.
Method: documentation only; no commands were run.
