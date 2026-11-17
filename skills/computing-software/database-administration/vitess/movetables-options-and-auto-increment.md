---
id: computing-software.database-administration.vitess.movetables-options-and-auto-increment
name: movetables-options-and-auto-increment
category: computing-software
field: database-administration
product: vitess
tags: [movetables, auto-increment, sequences, on-ddl, defer-secondary-keys, source-time-zone, cells]
level: advanced
status: docs-checked
description: "Tune MoveTables with its key flags: sharded-auto-increment-handling, global-keyspace, initialize-target-sequences, on-ddl, defer-secondary-keys, source-time-zone and more."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/movetables/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Moving unsharded tables into a sharded keyspace breaks MySQL `auto_increment`, so MoveTables offers a transparent replacement:
1. On `create`: `--sharded-auto-increment-handling=replace --global-keyspace=<unsharded-keyspace>`. Values are `LEAVE`, `REMOVE` (default) and `REPLACE`; REPLACE strips auto_increment when copying schemas and updates the target VSchema. The global keyspace (must be existing and unsharded) holds the sequence tables.
2. On `switchtraffic`: `--initialize-target-sequences`, which creates and initialises sequences from the current maximum column value across target shards when primary traffic switches. Without it you must create and initialise sequences manually with ample buffer to avoid duplicate keys.

Other options:
- `--auto-start` (default true): false leaves the workflow Stopped so you can edit `_vt.vreplication` (for example to build a Materialize or fix copy_state/pos).
- `--cells` (default the source tablet's local cell) or `--all-cells`.
- `--defer-secondary-keys`: drop secondary keys for the copy and re-add afterwards, speeding large tables with many indexes.
- `--max-replication-lag-allowed` (default equals `--timeout`): SwitchTraffic refuses if lag is higher. Primary switches make sources read-only while targets catch up, so writes pause.
- `--on-ddl` (default IGNORE; STOP, EXEC, EXEC_IGNORE).
- `--no-routing-rules`, which also means no global routing or vtgate traffic.
- `--rename-tables`: on complete or cancel, rename tables to `<table_name>_old` instead of deleting.
- `--enable-reverse-replication` (default true).
- `--source-time-zone`: converts DATETIME columns from that zone to UTC (time zone tables must be populated; VARCHAR dates are not converted).
- `--stop-after-copy`.

## Checked

2026-11-04. Auto-increment flags and their semantics and each listed option's default and effect confirmed on the MoveTables reference page.

Method: documentation only; no commands were run.
