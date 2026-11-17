---
id: computing-software.database-administration.vitess.reference-tables-sync
name: reference-tables-sync
category: computing-software
field: database-administration
product: vitess
tags: [reference-tables, materialize, vschema, vreplication, shard-targeting, replication-lag]
level: advanced
status: docs-checked
description: "Keep small lookup tables identical on every shard with reference tables: VSchema types, DML routing, Materialize and the shard-targeting hazard."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/reference_tables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reference tables are small, rarely changing tables (countries, currencies, time zones) copied to every shard so joins run locally. The source of truth is in an unsharded keyspace; all DML runs there and VReplication propagates changes to the sharded target.

Declare them in VSchema on both sides. Source keyspace:

```json
{ "tables": { "countries": { "type": "reference" } } }
```

Target keyspace, which also names the source so VTGate can route DML:

```json
{ "tables": { "countries": { "type": "reference", "source": "source.countries" } } }
```

SELECTs involving a reference table are served locally in each shard with no lookup against the unsharded keyspace. A DML issued against the target keyspace, for example `UPDATE countries SET name = 'The Netherlands' WHERE name = 'Netherlands'`, is routed by VTGate to the source keyspace.

Keep copies in sync with a Materialize workflow:

`Materialize --target-keyspace target --workflow ref1 create --source-keyspace source --reference-tables countries,currencies`

The copies are effectively caches updated through binlog replication, so under load there can be lag; watch `max_replication_lag` in `Workflow Show` output or in VTAdmin.

Warning: a DML sent with shard targeting to a specific target shard is not routed to the source. It writes to the target's copy and will most likely break the workflow later.

## Checked

2026-11-08. Read in full: Reference Tables page (vitess.io docs 25.0, via the website repo markdown). Confirmed: purpose, source and target VSchema fragments, SELECT and DML routing, the Materialize command, lag monitoring via max_replication_lag and the shard-targeting warning. Nothing removed.

Method: documentation only; no commands were run.
