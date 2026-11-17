---
id: computing-software.database-administration.cloudnative-pg.automated-failover-process-and-rto-rpo
name: automated-failover-process-and-rto-rpo
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [failover, failoverdelay, switchoverdelay, fast-shutdown, immediate-shutdown, rto, rpo, targetprimary]
level: practitioner
status: docs-checked
description: "Walk through CloudNativePG automated failover: the two-phase TargetPrimary pending procedure, fast then immediate shutdown, switchoverDelay, and the effect on RTO and RPO."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/failover.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If the primary stays unhealthy longer than `.spec.failoverDelay` (default `0` seconds), the cluster enters failover mode. Typical causes: disk failure on the primary pod, pod deletion, or sustained failure of the `postgres` container. The primary's readiness probe fails, and the controller acts in two steps:

1. It marks `TargetPrimary` as `pending`, forcing the primary pod to shut down so WAL receivers on replicas stop. The cluster phase is "Failing over".
2. When all WAL receivers have stopped, a leader election names the new primary, which promotes. The former primary restarts, sees it is no longer primary and becomes a replica.

The two-phase design stops the failing primary streaming WAL again after restart, avoiding timeline discrepancies between the new primary and replicas.

While the old primary shuts down: first a PostgreSQL **fast shutdown** with `.spec.switchoverDelay` seconds as timeout (this tries to archive pending WAL); if that fails or times out, an **immediate shutdown**. If PostgreSQL does not answer `pg_isready`, the instance manager goes straight to immediate shutdown, `switchoverDelay` does not apply, and leftover `.ready` segments are archived when the instance restarts, before it rejoins as a replica.

Fast mode does not wait for clients, terminates a running online backup and rolls back active transactions; immediate mode aborts all server processes without a clean shutdown.

RTO/RPO: in-flight queries, WAL writes and checkpoints may fail before the controller reacts; after the fast shutdown starts the cluster refuses connections but loses no data; a failed or skipped fast shutdown can lose data; with no primary the cluster is impaired but lossless. A low `switchoverDelay` favours RTO over RPO (risking loss at cluster or backup level); a high one does the reverse.

## Checked

2026-11-04. Two-step failover, shutdown sequence, unreachable-PostgreSQL path and RTO/RPO notes confirmed on the Automated failover page.

Method: documentation only; no commands were run.
