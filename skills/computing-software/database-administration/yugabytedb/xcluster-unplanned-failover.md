---
id: computing-software.database-administration.yugabytedb.xcluster-unplanned-failover
name: xcluster-unplanned-failover
category: computing-software
field: database-administration
product: yugabytedb
tags: [xcluster, failover, disaster-recovery, safe-time, restore-snapshot-schedule, delete-universe-replication, rpo]
level: sme
status: docs-checked
description: "Fail over a transactional xCluster standby after losing the primary: pause replication, read safe time, PITR to it, delete replication, then fix sequences and CDC."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/deploy/multi-dc/async-replication/async-transactional-failover.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unplanned xCluster failover

Use only when the primary (A) is unavailable and you are sure it will not recover soon and the data loss is acceptable. Failover has a non-zero RPO and can lose committed data.

Steps on the standby (B), which becomes the new primary:
1. Stop application traffic to A so no more updates are attempted.
2. Pause replication on B, so no unexpected updates arrive if A comes back or was partially down: `yb-admin --master_addresses <B-master-addresses> set_universe_replication_enabled <replication_name> 0`.
3. Get the safe time: `yb-admin --master_addresses <B-master-addresses> get_xcluster_safe_time include_lag_and_skew`. `safe_time` is the latest timestamp at which all tables in the namespace were transactionally replicated, and failover restores the namespace to it. `safe_time_lag_sec` is the time between now and `safe_time`; `safe_time_skew_sec` is the gap between the most and least caught-up tablet and roughly estimates the data lost. Decide whether that loss is acceptable.
4. PITR-restore each database to the safe time, one database after another. With yugabyted: `yugabyted restore --database <database> --recover_to_point_in_time '<safe_time>'`. Manually: find the schedule with `yb-admin list_snapshot_schedules`, run `yb-admin restore_snapshot_schedule <schedule_id> "<safe_time>"`, then repeat `yb-admin list_snapshot_restorations` until the state is RESTORED.
5. Delete the old replication group: `yb-admin --master_addresses <B-master-addresses> delete_universe_replication <replication_group_id>`.
6. Fix sequences and serial columns with `nextval` so values sit above the existing maximum (for example above 500 when the highest SERIAL value is 500). Skip this in automatic mode; xCluster only replicates sequence data in automatic mode.
7. Fix CDC if used: failover can lose CDC data, and the loss may differ from the xCluster loss. Either create publications and slots on B (resumes from the failover point, subject to loss) or clear the CDC target and start from a fresh full copy of B, then point the target at B.
8. Update application connection strings to B. There is no standby until A returns and is restored.

If A returns, bringing it back as a standby means dropping its databases and bootstrapping from B (see the transactional setup steps); disable PITR and drop the xCluster streams on A first.

## Checked

2026-11-09: warnings, the pause, safe-time, PITR (yugabyted and manual), delete, sequence, CDC and cutover steps and the recovery note confirmed against the transactional failover page (yugabyte-db docs async-transactional-failover.md, read in full). Removed the claim that CDC streams and slots do not survive the restore (the page only says to recreate publications and slots on B) and the unsourced snapshot-schedule prerequisite sentence.

Method: docs-checked 2026-11-09 against yugabyte-db docs async-transactional-failover.md
