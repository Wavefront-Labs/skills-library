---
id: computing-software.database-administration.cockroachdb.physical-cluster-replication-failover
name: physical-cluster-replication-failover
category: computing-software
field: database-administration
product: cockroachdb
tags: [pcr-failover, failback, complete-replication, virtual-cluster, disaster-recovery]
level: advanced
status: docs-checked
description: "Fail over a CockroachDB standby to primary with ALTER VIRTUAL CLUSTER ... COMPLETE REPLICATION, start the service, point default target, then fail back."
sources:
  - https://www.cockroachlabs.com/docs/stable/failover-replication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: promote the standby when the primary is lost, and later return to the original primary.

Step 1, choose the failover time and complete replication on the standby. Check status first:
```sql
SHOW VIRTUAL CLUSTER main WITH REPLICATION STATUS;
ALTER VIRTUAL CLUSTER main COMPLETE REPLICATION TO LATEST;
```
`LATEST` uses the most recent replicated timestamp and minimizes loss from asynchronous replication lag. For a point in time use `COMPLETE REPLICATION TO SYSTEM TIME '-1h'` (or a future offset such as `'+5h'`).

Step 2, bring the standby into service and route SQL to it:
```sql
SHOW VIRTUAL CLUSTER main WITH REPLICATION STATUS;
ALTER VIRTUAL CLUSTER main START SERVICE SHARED;
SET CLUSTER SETTING server.controller.default_target_cluster='main';
```

Failback to the original primary (cluster A) from the now-active cluster B:
1. On A: `ALTER VIRTUAL CLUSTER {cluster_a} STOP SERVICE;`
2. Build a B connection string with `cockroach convert-url ... --format crdb --ca-cert certs/ca.crt --inline`.
3. On A: `SET CLUSTER SETTING kv.rangefeed.enabled = 'true';` then `ALTER VIRTUAL CLUSTER {cluster_a} START REPLICATION OF {cluster_b} ON 'postgresql://...';`
4. When caught up: `ALTER VIRTUAL CLUSTER {cluster_a} COMPLETE REPLICATION TO LATEST;` then `START SERVICE SHARED` and set `server.controller.default_target_cluster` to `{cluster_a}`.
If replicating from an existing primary that was not the original, the page offers creating a new virtual cluster `main` on A from B (initial scan) or building a new cluster C.

Job management: changefeeds running on the old primary fail on the promoted cluster, so recreate them there; check that no other schedule backs up to the same collection (schedules created on v23.1 or earlier, and changefeed schedules from v24.1 or earlier, do not pause automatically on the promoted cluster).

Verify: completion is asynchronous, so monitor it with `SHOW VIRTUAL CLUSTER main WITH REPLICATION STATUS;` before and after `START SERVICE SHARED`.

## Checked
2026-11-03. Confirmed on the failover page: `COMPLETE REPLICATION TO LATEST` and `SYSTEM TIME` forms (including `'-1h'` and `'+5h'`), `START SERVICE SHARED`, `server.controller.default_target_cluster`, the failback statements (`STOP SERVICE`, `START REPLICATION OF`), the two options for a non-original primary (new virtual cluster `main` on A, or a new cluster C), and the changefeed and backup schedule caveats. Corrected: job management wording and verify step.
Method: documentation only; no commands were run.
