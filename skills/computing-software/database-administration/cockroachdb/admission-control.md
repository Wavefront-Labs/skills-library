---
id: computing-software.database-administration.cockroachdb.admission-control
name: admission-control
category: computing-software
field: database-administration
product: cockroachdb
tags: [admission-control, overload, work-queues, node-overload, quality-of-service]
level: practitioner
status: docs-checked
description: "Understand and monitor CockroachDB admission control: CPU and storage IO queues, overload signals, per-layer cluster settings, and its limits."
sources:
  - https://www.cockroachlabs.com/docs/stable/admission-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use admission control to keep individual overloaded nodes from degrading the cluster, and know when it will not help.

What it does: queues work for CPU and storage IO per node, ordered by priority and transaction start time, so important work proceeds during hotspots. For storage it aims to stop the LSM tree from building read amplification while still absorbing write bursts. It also paces replication: regular SQL writes at quorum speed, background (elastic) replication at the slowest replica's rate.

Covered work: SQL queries, imports, `COPY`, deletes (including row-level TTL), backups, restores, schema change backfills, follower replication, Raft log writes, changefeeds, intent resolution.

Overload signals from the docs, shown in the DB Console Overload and Hardware dashboards:
- more than 32 runnable goroutines per CPU
- high IO Overload (Pebble LSM) graph
- high CPU utilization
- out-of-memory errors

Settings per layer (enable or disable them for all layers together, as recommended): `admission.kv.enabled`, `admission.sql_kv_response.enabled`, `admission.sql_sql_response.enabled`; optional storage limits `kvadmission.store.snapshot_ingest_bandwidth_control.enabled` and `kvadmission.store.provisioned_bandwidth`.

Limits: it helps when a few nodes are overloaded. If many nodes show overload the cluster needs more resources. Client connections are not managed, so too many connections per gateway node can still hurt.

## Checked

2026-11-03. Confirmed against the admission control page: queues and ordering, covered work, overload signals including 32 runnable goroutines per CPU, the `admission.*` and `kvadmission.*` settings, replication pacing, limits. Removed: invented verification step.
Method: documentation only; no commands were run.
