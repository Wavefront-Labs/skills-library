---
id: computing-software.database-administration.mysql.innodb-clusterset-dr
name: innodb-clusterset-dr
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, clusterset-dr, innodb-clusterset, disaster-recovery, mysql-shell, mysql-router, cross-site-replication]
level: practitioner
status: docs-checked
description: "Build an InnoDB ClusterSet for cross-site disaster recovery: create replica clusters, and know how controlled switchover differs from emergency failover."
sources:
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/innodb-clusterset.html
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/innodb-clusterset-deploy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InnoDB ClusterSet for cross-site DR

ClusterSet links one **primary InnoDB Cluster** to one or more **replica clusters** in other locations. Replication
between clusters uses a dedicated asynchronous channel named `clusterset_replication`, managed by Group Replication
(sender: primary of the primary cluster; receiver: primary of the replica cluster; re-established automatically
after a new primary is elected). Replica clusters do not accept writes and can be read, with normal replication lag.
No limit on the number of replica clusters; a replica cluster may be one member, three recommended, up to nine.

## Create (MySQL Shell, JS mode)
Connect to a member of the existing cluster with the InnoDB Cluster server configuration account (not root unless
you accept the same root password everywhere), then:
```js
var cluster1 = dba.getCluster();
var cs = cluster1.createClusterSet('myclusterset');       // options: dryRun, clusterSetReplicationSslMode, replicationAllowedHost
cs.status({extended: 1});
```
`domainName` is required, non-empty, at most 63 characters, starting with an alphanumeric or `_`, and made of
alphanumerics, `_`, `.`, `-`. `clusterSetReplicationSslMode` is `AUTO` (default), `REQUIRED`, `DISABLED`,
`VERIFY_CA` or `VERIFY_IDENTITY`.

For each standalone instance of a replica cluster, create the same configuration account first:
```js
dba.configureInstance('root@dr1-db1:3306', {clusterAdmin: 'icadmin'});
```
Then, from the ClusterSet object (`dba.getClusterSet()` while connected as the configuration account):
```js
var dr = cs.createReplicaCluster('dr1-db1:3306', 'drcluster', {recoveryMethod: 'clone', recoveryProgress: 1});
dr.addInstance('icadmin@dr1-db2:3306');
dr.addInstance('icadmin@dr1-db3:3306');
cs.status({extended: 1});
```
`recoveryMethod`: `AUTO` (default, compares GTID sets and may prompt), `CLONE` (overwrites the instance with a
physical snapshot) or `INCREMENTAL` (binary log transfer). Other options: `cloneDonor`, `timeout`,
`manualStartOnBoot`, `communicationStack`. Provisioning can take hours on large datasets.
Creation sets `skip_replica_start=ON` so replication threads do not start automatically, and `super_read_only` on
the replica cluster.

## Router
Bootstrap MySQL Router against the ClusterSet (re-bootstrap Routers that were bootstrapped against the plain
cluster). By default Routers send reads and writes to whichever cluster is the primary cluster, and can be
configured to target a specific cluster; see "Integrating MySQL Router With InnoDB ClusterSet" (section 9.6).

## Switchover versus failover
- **Controlled switchover** (primary still available): data consistency is assured and the old primary cluster
  becomes a read-only replica cluster. Use for maintenance. See section 9.8.
- **Emergency failover** (primary cluster lost): consistency is not assured; unreplicated or divergent transactions
  can be lost and only recovered manually, if at all. The old primary cluster is marked **invalidated**; shut it down
  when you can reach it. Try to repair or reconnect the primary cluster before failing over. An invalidated cluster
  can be rejoined only if its transaction set is consistent, and the check, repair and rejoin are manual AdminAPI
  steps; alternatively discard it and create new replica clusters. See sections 9.9 and 9.10.

## Monitoring
`cs.status({extended: 1})` shows per-cluster `globalStatus`, `clusterSetReplicationStatus`, replication lag per
member and `transactionSet`. Extended status also reports errant and missing GTID sets per replica cluster.

## Gotchas
- ClusterSet favours availability over consistency: asynchronous replication lag is your data-loss exposure on
  emergency failover.
- Fencing, repair, removal and rejoin of clusters are in section 9.10 of the MySQL Shell manual.

## Checked
2026-11-01. Confirmed against the MySQL Shell 8.4 manual: InnoDB ClusterSet overview (chapter 9) and Deploying
InnoDB ClusterSet (9.4): channel name, `createClusterSet` and `createReplicaCluster` options and values, naming
rules, `configureInstance` `clusterAdmin`, replica member limits, switchover versus failover semantics. Removed as
unconfirmed (their pages were not readable): exact switchover, failover, rejoin, removal, fencing and Router
routing-option call names, version requirements and the Router bootstrap command.
Method: documentation only; no commands were run.
