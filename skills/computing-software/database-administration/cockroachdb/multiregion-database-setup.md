---
id: computing-software.database-administration.cockroachdb.multiregion-database-setup
name: multiregion-database-setup
category: computing-software
field: database-administration
product: cockroachdb
tags: [multi-region, primary-region, database-regions, locality, super-regions]
level: practitioner
status: docs-checked
description: "Turn a CockroachDB database multi-region: node --locality region and zone, SHOW REGIONS, primary region, adding regions, super and secondary regions."
sources:
  - https://www.cockroachlabs.com/docs/stable/multiregion-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure a database so CockroachDB optimizes placement and latency across geographies.

Concepts: cluster region (set at node start), database region (a cluster region added to a database), survival goal (how many simultaneous failures to survive), table locality (how access to a table is optimized).

Steps:
1. Start every node with locality, using the `region` and `zone` keys:
```shell
cockroach start --locality=region=us-east-1,zone=us-east-1b # ... other required flags
```
2. List what the cluster knows: `SHOW REGIONS FROM CLUSTER;`
3. Make the database multi-region by setting the primary region with `ALTER DATABASE ... PRIMARY REGION` (also available at database creation), then add more with `ALTER DATABASE ... ADD REGION`. `SHOW REGIONS FROM DATABASE` lists them. The first region added is the primary region; add other regions afterwards.
4. Optionally change table localities (regional by table, regional by row, global) and the survival goal. Defaults: all tables are homed in the primary region and the database survives zone failures.

Super regions (`ADD SUPER REGION`, `ALTER SUPER REGION`, `DROP SUPER REGION`, `SHOW SUPER REGIONS`) group database regions so the objects assigned to them keep all replicas only inside member regions, useful for data domiciling. Secondary regions (`SET SECONDARY REGION`, `DROP SECONDARY REGION`) designate a failover home region.

Gotchas: database regions come from the `region` locality key set at node start; table locality and survival goals have a significant impact on performance, so choose them deliberately. Secondary regions are not compatible with REGIONAL BY ROW tables, and with super regions the secondary region must sit inside the primary's super region.

Verify: `SHOW REGIONS FROM CLUSTER;` lists the node regions and `SHOW REGIONS FROM DATABASE <db>;` lists the database regions.

## Checked
2026-11-03. Confirmed on the multi-region overview page: the four concepts, the `--locality=region=...,zone=...` example, `SHOW REGIONS FROM CLUSTER`, primary region then added regions, defaults (tables homed in the primary region, survive zone failures), super regions for data domiciling, secondary regions for failover. Removed: the zone config extension sentence and the survival goal claim about SHOW REGIONS output; the exact super region and secondary region statement syntax was not readable on the page, so check the statement reference pages.
Method: documentation only; no commands were run.
