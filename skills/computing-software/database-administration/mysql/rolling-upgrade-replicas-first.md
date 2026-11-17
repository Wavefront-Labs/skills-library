---
id: computing-software.database-administration.mysql.rolling-upgrade-replicas-first
name: rolling-upgrade-replicas-first
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-upgrade, rolling-upgrade-mysql, replica-first, switchover, innodb-cluster-upgrade, minimal-downtime, version-skew]
level: advanced
status: draft
description: "Upgrade a replicated MySQL topology with seconds of downtime: replicas first, soak, controlled switchover, then the old source, with clear version-skew rules."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-upgrade.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-compatibility.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rolling upgrade, replicas first

**Goal:** a major/minor MySQL upgrade where the only downtime is a switchover.

## Rule of version skew
Replication from an **older source to a newer replica** is supported (within one
major step, e.g. 8.0 → 8.4). Newer source → older replica is not guaranteed
(new binlog events, new defaults). Hence: replicas first, source last.

## Procedure (async replication, one source + N replicas)
1. Checker clean, backups verified, upgrade rehearsed on a clone.
2. For each replica, one at a time:
   - remove from read pool; `STOP REPLICA;` clean shutdown (`innodb_fast_shutdown=0`);
   - upgrade binaries; start; `START REPLICA;` confirm
     `Replica_SQL_Running: Yes`, `Seconds_Behind_Source` back to 0;
   - return to the pool; soak (hours/days) watching errors and query latency.
3. Switchover: pick an upgraded replica as the new source. Stop writes (proxy
   or `SET GLOBAL super_read_only=ON` on old source), wait for the candidate to
   catch up (`WAIT_FOR_EXECUTED_GTID_SET`), make it writable
   (`super_read_only=OFF`), repoint other replicas
   (`CHANGE REPLICATION SOURCE TO ... SOURCE_AUTO_POSITION=1`), switch the proxy.
4. Upgrade the old source and attach it as a replica.

## InnoDB Cluster / Group Replication
Upgrade secondaries one by one (`mysqlsh` restart, they rejoin), then
`cluster.setPrimaryInstance()` to an upgraded member and upgrade the old
primary. In a mixed-version group, automatic primary election favours the
member with the lowest version, newer members may be read-only, and a
lower-version server cannot join a group of higher-version members
(`group_replication_allow_local_lower_version_join` overrides; emergencies only).
Afterwards `cluster.upgradeMetadata()` / `dba.upgradeMetadata()` with the new Shell.

## Gotchas
- Plan the point of no return: after the upgraded source takes writes, the old
  version cannot replicate from it; rollback needs a backup or re-clone.
- Statement changes (new reserved words, removed functions) hit the replica SQL
  thread first: stopping replication on upgrade is the early warning.
- Keep ProxySQL/Router versions compatible with the new server (auth plugins).

## Verify
`SELECT @@version` on every node equals the target; replication healthy on all;
app error rate unchanged over the soak.
