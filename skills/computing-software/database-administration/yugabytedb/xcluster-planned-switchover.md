---
id: computing-software.database-administration.yugabytedb.xcluster-planned-switchover
name: xcluster-planned-switchover
category: computing-software
field: database-administration
product: yugabytedb
tags: [xcluster, switchover, planned-failover, reverse-replication, rpo-zero, safe-time, sequences]
level: sme
status: docs-checked
description: "Swap xCluster primary and standby with no data loss: confirm lag under 5 seconds, set up reverse replication, wait for safe time, fix sequences, switch apps."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/multi-dc/async-replication/async-transactional-switchover.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Planned xCluster switchover

A planned switchover moves write access from the primary universe (A) to the standby (B) with zero RPO. It mostly updates metadata and typically completes within 30 seconds, but applications must be redirected, so do it in a maintenance window.

1. Precheck: the existing replication must be healthy with lag under 5 seconds (see the Monitor xCluster page), and the xCluster prerequisites must hold for the new direction.
2. In automatic mode, run no DDL during the switchover: stop submitting DDL and wait for earlier DDL to replicate. The xCluster safe time shows the latest time up to which DDL has replicated.
3. Set up replication in the reverse direction (B to A) with the transactional xCluster setup steps, skipping the bootstrap (backup/restore) step because both universes already hold the data. Use the same replication mode as the original setup and keep monitoring the new replication. This step puts both universes in read-only mode so B can catch up with A.
4. Wait for B to catch up: get the current time on A, then wait until the xCluster safe time on B is a few seconds greater than that time. Lag and skew values may stay non-zero because they are estimates; with no new writes, no data is lost in this window. If CDC reads from YugabyteDB, also wait for the CDC target to catch up (lag zero or near zero, event count metrics 0).
5. Fix sequences and serial columns on B so new values sit above the existing maximum (for example set the sequence above 500 when the highest SERIAL value is 500), using `nextval`. Skip this in automatic mode, the only mode in which xCluster replicates sequence data.
6. Delete the old replication group by running against A: `yb-admin drop_xcluster_replication <replication_group_id> <standby_master_addresses>` (or `yugabyted xcluster delete_replication` with `--replication_id` and `--target_address`). If CDC reads from YugabyteDB, de-configure CDC on A (delete publications and slots) and create publications and slots on B.
7. Switch applications to B: update connection strings. B is now the primary and A the standby. For CDC, start the connector against B with `snapshot.mode=never`.

## Checked

2026-11-09: the 30-second figure, 5-second lag precheck, automatic-mode DDL warning, reverse setup without bootstrap, safe-time wait, sequence handling, drop command and CDC steps confirmed against the transactional switchover page and its transactional-drop include (yugabyte-db docs repo, read in full). Corrected the delete command (the page uses `drop_xcluster_replication`, not `delete_universe_replication`). Removed the unsourced lag metric name, `get_xcluster_safe_time` precheck, explicit write-stop step, `get_replication_status` check and the PITR comparison.

Method: docs-checked 2026-11-09 against yugabyte-db docs async-transactional-switchover.md and includes/transactional-drop.md
