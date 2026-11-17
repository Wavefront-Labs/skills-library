---
id: computing-software.database-administration.vitess.vreplication-overview
name: vreplication-overview
category: computing-software
field: database-administration
product: vitess
tags: [vreplication, workflows, streams, materialize, failover-continuation, schema-tracker]
level: practitioner
status: docs-checked
description: "What VReplication is built from: streams, copy and replicate phases, filtering SELECTs, journaling, lag tracking, DDL handling, schema tracker."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/vreplication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VReplication is the engine behind MoveTables, Reshard, Materialize, LookupVindex creation, online DDL (strategy `vitess`), VStream CDC and the Messaging job queue. It runs as streams, each from a source keyspace/shard to a target keyspace/shard, and one stream can replicate several tables. Each table carries a `SELECT` that gives the transformation (non-aggregate expressions, plus COUNT or SUM with GROUP BY for rollups) and the filter (WHERE); joins are not supported. Multiple streams are needed when source and target shards are not one to one.

It copies data consistently (interruptible and resumable), then replicates continuously; VDiff verifies correctness; a journal table records binlog positions at traffic cutovers so other streams can resume from the new source; routing rules steer queries during a workflow.

Properties from the page:
- Fast replay batches transactions when the source outpaces the target (3-20X over traditional MySQL replication in load tests).
- Lag tracking: the source sends its clock with each event, plus heartbeats, so the target corrects for clock skew and reports lag if it receives nothing.
- Self-replication: source and target may be the same keyspace/shard, useful for schema rollouts.
- Deadlocks and lock wait timeouts are retried silently and counted. Other errors are retried after a pause, picking a random source each time.
- A failover on the target keyspace/shard makes the new primary resume where the old one left off.
- `on-ddl` on MoveTables and Reshard: `IGNORE` (default), `STOP`, `EXEC`, `EXEC_IGNORE`; the page cautions against EXEC modes.
- Schema tracker: `--track-schema-versions` on vttablet stores versions in `_vt.schema_version`; it is off by default because of overhead; prune with `--schema-version-max-age-seconds`.

## Checked

2026-11-08. Re-read the full VReplication Overview page (v25.0). Use cases, stream model, essential functions, the Other Properties subsections and the schema tracker note confirmed on the VReplication page.

Method: documentation only; no commands were run.
