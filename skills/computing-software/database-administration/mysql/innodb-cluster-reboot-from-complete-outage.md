---
id: computing-software.database-administration.mysql.innodb-cluster-reboot-from-complete-outage
name: innodb-cluster-reboot-from-complete-outage
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, reboot-cluster-from-complete-outage, innodb-cluster, group-replication, group-replication-bootstrap-group, gtid-superset, quorum-loss, force-quorum-using-partition-of]
level: practitioner
status: docs-checked
description: "Bring an InnoDB Cluster back after every member stopped (power loss) and pick the member with the most GTIDs, with MySQL Shell or by hand, without creating two groups."
sources:
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/reboot-outage.html
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/troubleshooting-innodb-cluster.html
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-restarting-group.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recovering an InnoDB Cluster from complete outage

**Goal:** restart a cluster whose members all went down, without losing transactions or creating two groups.

## Why it does not come back by itself
When every member has left the group, the group exists only as configuration on the members. It must be
bootstrapped again as if it were new, starting from the most up to date member. The last known primary is not
necessarily that member.

## With MySQL Shell (preferred)
1. Start mysqld on all members. The command fails if any cluster member is unreachable (unless you use `force`).
2. Connect to the most up-to-date instance and run:
   ```js
   var cluster = dba.rebootClusterFromCompleteOutage('prodCluster')
   ```
   If the instance you are connected to does not hold the GTID superset the operation aborts and says so. To find
   the right member, run it with `dryRun: true` (the report says `Switching over to instance '...' to be used as
   seed`) or run `SHOW VARIABLES LIKE 'gtid_executed';` on each instance and take the largest set.
   Options: `primary` (instance to select as primary), `force` (true or false, default false), `dryRun`,
   `switchCommunicationStack` (`mysql` or `xcom`), `ipAllowList`, `localAddress`.
3. `force: true` reboots with the reachable members only, or with a member that has a lower GTID set, and then
   discards transactions not in the selected member's set. Members left out must be added back with
   `cluster.rejoinInstance()`; rebootClusterFromCompleteOutage cannot add or rejoin them.
4. Check with `cluster.status()`.

## By hand (plain Group Replication)
On each member: set `group_replication_start_on_boot=OFF`, start mysqld, do not start Group Replication, then collect:
```sql
SELECT @@GLOBAL.GTID_EXECUTED;
SELECT received_transaction_set FROM performance_schema.replication_connection_status
  WHERE channel_name = 'group_replication_applier';
```
Compare all sets (both executed and certified transactions) and pick the member with the biggest. On it:
```sql
SET GLOBAL group_replication_bootstrap_group = ON;
START GROUP_REPLICATION;
SET GLOBAL group_replication_bootstrap_group = OFF;
```
Then `START GROUP_REPLICATION;` on each other member. Never store `group_replication_bootstrap_group=ON` in the
configuration file, or a second group with the same name is created on restart. Afterwards set
`group_replication_start_on_boot` back to ON (or remove it; ON is the default).

## Quorum loss with some members alive
Restoring a cluster from quorum loss is a separate procedure; see "Restoring a Cluster from Quorum Loss" in the
MySQL Shell manual (section 8.8.2) instead of rebooting.

## Last resort
If the reboot fails and the cluster metadata is badly corrupted, `dba.dropMetadataSchema()` drops it so you can
recreate the cluster. It cannot be undone and, with MySQL Router, drops all current connections and forbids new ones.

## Verify
```sql
SELECT * FROM performance_schema.replication_group_members;
```
All members `ONLINE` with one primary (single-primary mode), and a test write on the primary replicates.

## Checked
2026-11-01. Confirmed against the MySQL Shell 8.4 manual (Rebooting a Cluster from a Major Outage; section index of
Restoring and Rebooting an InnoDB Cluster) and the MySQL 8.4 manual (Restarting a Group): options list, force and
dryRun behaviour, GTID superset selection, manual bootstrap steps, `group_replication_applier` query. Removed as
unconfirmed: the forceQuorumUsingPartitionOf procedure details, split-brain warning, errant-transaction and clone
advice, `listRouters`, and the start_on_boot opinion.
Method: documentation only; no commands were run.
