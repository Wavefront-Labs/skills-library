---
id: computing-software.database-administration.mysql.monitoring-group-replication-members
name: monitoring-group-replication-members
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-group-replication, innodb-cluster, replication-group-members, cluster-status, monitoring, applier-queue]
level: practitioner
status: docs-checked
description: "Monitor MySQL Group Replication: member states and roles, certification and applier queues, conflicts, and cluster.status() health in InnoDB Cluster."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-monitoring.html
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-replication-group-member-stats.html
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/monitoring-innodb-cluster.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring Group Replication members

## Membership
```sql
SELECT member_host, member_port, member_state, member_role, member_version,
       member_communication_stack
FROM performance_schema.replication_group_members;
```
States: `ONLINE`, `RECOVERING` (catching up via clone or distributed recovery), `OFFLINE`,
`ERROR` (left due to error; check its error log), `UNREACHABLE` (others can't reach it;
if a majority is unreachable the group **loses quorum** and blocks writes).

## Queues and conflicts per member
```sql
SELECT member_id, count_transactions_in_queue AS cert_queue,
       count_transactions_remote_in_applier_queue AS applier_queue,
       count_transactions_checked, count_conflicts_detected,
       count_transactions_rows_validating, transactions_committed_all_members,
       count_transactions_local_rollback
FROM performance_schema.replication_group_member_stats;
```
- `applier_queue` growing on a secondary = it applies slower than the group writes; flow
  control will throttle the primary (see flow control settings).
- `count_conflicts_detected` rising in multi-primary mode = concurrent writes to the same
  rows; in single-primary mode it should be ~0.
- `count_transactions_local_rollback` = local transactions rolled back by certification.

## Recovery channel
```sql
SELECT channel_name, service_state, last_error_message
FROM performance_schema.replication_connection_status
WHERE channel_name IN ('group_replication_recovery', 'group_replication_applier');
```

## From MySQL Shell (InnoDB Cluster)
```js
var c = dba.getCluster(); c.status({extended: 1})
```
Look at `status` (`OK`, `OK_PARTIAL`, `OK_NO_TOLERANCE` = cannot survive another failure,
`NO_QUORUM`), each member's `mode` (`R/W`, `R/O`), `replicationLag`, `instanceErrors`.
`c.describe()` shows topology.

## Alerts
- Any member not `ONLINE` for > 1 min.
- `status` != `OK` (especially `OK_NO_TOLERANCE` and `NO_QUORUM`).
- applier queue above a threshold (e.g. 1000) for 5 min.
- Primary changed (log `member_role` transitions).

## Gotchas
- `replication_group_members` on a member that was expelled shows only itself as `ERROR`;
  query a healthy member for the true view.
- Time-based lag is not shown directly; use queue sizes, or compare
  `gtid_executed` between members.

## Verify
Stop mysqld on one secondary in a test: status becomes `OK_NO_TOLERANCE`, the member shows
`UNREACHABLE`/disappears, alerts fire; after restart it returns via `RECOVERING` to `ONLINE`.

## Checked

2026-10-31: confirmed the member_state values ONLINE/RECOVERING/OFFLINE/ERROR/UNREACHABLE and their meanings (group-replication-server-states), the replication_group_member_stats columns (COUNT_TRANSACTIONS_IN_QUEUE, COUNT_TRANSACTIONS_CHECKED, COUNT_CONFLICTS_DETECTED, COUNT_TRANSACTIONS_ROWS_VALIDATING, TRANSACTIONS_COMMITTED_ALL_MEMBERS, COUNT_TRANSACTIONS_REMOTE_IN_APPLIER_QUEUE, COUNT_TRANSACTIONS_LOCAL_ROLLBACK, performance-schema-replication-group-member-stats-table), the replication_connection_status channel view, and Cluster.status() values (OK, OK_PARTIAL, OK_NO_TOLERANCE, NO_QUORUM), mode R/W-R/O, replicationLag, instanceErrors with extended: 1, and Cluster.describe() on the MySQL Shell monitoring page. Dropped the unconfirmed Cluster.options() mention.
Method: documentation only; no commands were run.
