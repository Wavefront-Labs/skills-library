---
id: computing-software.database-administration.mysql.innodb-replicaset
name: innodb-replicaset
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, innodb-replicaset, mysql-shell, async-replication, mysql-router, adminapi, switchover]
level: practitioner
status: draft
description: "Deploy and operate a MySQL InnoDB ReplicaSet (AdminAPI-managed async replication): create, add instances with clone, Router, switchover and forced failover."
sources:
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/mysql-innodb-replicaset.html
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/working-with-replicaset.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# InnoDB ReplicaSet

A ReplicaSet is a primary plus async GTID replicas managed through MySQL Shell's AdminAPI, with MySQL Router for routing. Unlike InnoDB Cluster there is **no automatic failover** and no Group Replication: simpler, works across higher latency links, tolerates 2 nodes.

## Create
```js
// mysqlsh --js, as an admin account on each instance
dba.configureReplicaSetInstance('admin@db1:3306', {clusterAdmin: 'rsadmin'});
dba.configureReplicaSetInstance('admin@db2:3306', {clusterAdmin: 'rsadmin'});
\connect rsadmin@db1:3306
var rs = dba.createReplicaSet('app_rs');
rs.addInstance('db2:3306', {recoveryMethod: 'clone'});   // or 'incremental' if db2 already has the data
rs.status();
```
Requirements: MySQL 8.0+, GTIDs on, row-based binlog, all tables InnoDB with primary keys (the Shell checks).

## Router
```bash
mysqlrouter --bootstrap rsadmin@db1:3306 --directory /etc/mysqlrouter/app_rs --user=mysqlrouter
# apps connect: 6446 read/write (primary), 6447 read-only (replicas)
```

## Planned switchover
```js
rs.setPrimaryInstance('db2:3306', {dryRun: true});
rs.setPrimaryInstance('db2:3306');
```
Old primary becomes a replica of db2; Routers follow automatically.

## Primary failure
```js
\connect rsadmin@db2:3306
var rs = dba.getReplicaSet();
rs.forcePrimaryInstance('db2:3306');
```
- Unreplicated transactions on the dead primary are lost.
- The old primary is invalidated; when it comes back, check for errant GTIDs before `rs.rejoinInstance('db1:3306')`, or remove it (`rs.removeInstance('db1:3306', {force: true})`) and re-add with clone.
- Make sure the old primary cannot accept writes before forcing (power off or block network): a ReplicaSet has no fencing of its own.

## Monitoring
```js
rs.status({extended: 1});    // replication lag, applier errors, instance roles
```
Plus the usual `SHOW REPLICA STATUS` on replicas.

## Gotchas
- Instances must not have extra replication channels managed outside AdminAPI.
- Changing topology with plain SQL (`CHANGE REPLICATION SOURCE`) desynchronizes the metadata; always use AdminAPI.
- Need automatic failover? Use InnoDB Cluster (3+ nodes) instead, or external tooling.
