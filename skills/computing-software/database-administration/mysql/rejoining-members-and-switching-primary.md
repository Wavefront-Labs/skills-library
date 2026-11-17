---
id: computing-software.database-administration.mysql.rejoining-members-and-switching-primary
name: rejoining-members-and-switching-primary
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, rejoin-instance, set-primary-instance, innodb-cluster, group-replication, mysql-shell, switchover]
level: practitioner
status: draft
description: "Bring InnoDB Cluster members back with rejoinInstance, choose clone vs incremental recovery, and move the primary role with setPrimaryInstance."
sources:
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/rejoin-cluster.html
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-innodb-cluster-working-with-primary.html
  - https://dev.mysql.com/doc/refman/8.4/en/group-replication-distributed-recovery.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rejoining members and switching primary

## Why a member is out
`cluster.status()` shows a member as `(MISSING)`, `ERROR` or `OFFLINE` after a restart, network blip or expulsion. Check its error log for `[GCS]` and `Plugin group_replication reported` lines first.

With `group_replication_start_on_boot = ON` (AdminAPI default) and `group_replication_autorejoin_tries` (default 3), members usually return by themselves. When not:

## rejoinInstance
```js
var c = dba.getCluster();
c.rejoinInstance('db3:3306');
c.rejoinInstance('db3:3306', {recoveryMethod: 'clone'});   // force full re-provision
c.status();
```
Recovery choice:
- **Incremental**: replays missing GTIDs from a donor's binlogs. Only possible if donors still have them (`binlog_expire_logs_seconds`).
- **Clone**: copies the whole dataset from a donor (needs the clone plugin, restarts the instance). Required if binlogs are purged or the member has **errant transactions** (GTIDs not in the group): Shell reports `The instance contains additional transactions`.

If the instance's data is corrupt or diverged, `c.removeInstance('db3:3306', {force: true})` then `c.addInstance('db3:3306', {recoveryMethod: 'clone'})`.

## Switching primary (single-primary mode)
```js
c.setPrimaryInstance('db2:3306');
```
- Waits for in-flight transactions per `group_replication_consistency` settings, then changes the primary; Routers redirect read/write traffic in seconds.
- Use before maintenance on the current primary (OS patching, rolling upgrade: upgrade secondaries, switch primary, upgrade old primary).
- Influence automatic elections with member weights: `c.setInstanceOption('db2:3306', 'memberWeight', 80)`.

## Verify
```sql
SELECT MEMBER_HOST, MEMBER_STATE, MEMBER_ROLE, MEMBER_VERSION FROM performance_schema.replication_group_members;
```
All `ONLINE`, exactly one `PRIMARY` in single-primary mode.

## Gotchas
- A member stuck in `RECOVERING` for long: watch `performance_schema.replication_applier_status_by_worker` for channel `group_replication_recovery` errors (donor auth, SSL, purged binlogs).
- Clone wipes the joining instance's data; check you have the right host.
- Losing quorum (majority) is a different problem: use `forceQuorumUsingPartitionOf` or `rebootClusterFromCompleteOutage`, not rejoinInstance.
