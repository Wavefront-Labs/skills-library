---
id: computing-software.database-administration.mysql.deploying-innodb-cluster-with-mysql-shell
name: deploying-innodb-cluster-with-mysql-shell
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, innodb-cluster, mysql-group-replication, dba-create-cluster, add-instance, mysql-shell, adminapi]
level: practitioner
status: docs-checked
description: "Build a 3-node MySQL InnoDB Cluster with MySQL Shell AdminAPI: configureInstance, createCluster, addInstance with clone recovery, then bootstrap MySQL Router."
sources:
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/deploying-production-innodb-cluster.html
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/configuring-production-instances.html
  - https://dev.mysql.com/doc/mysql-shell/8.4/en/add-instances-cluster.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying InnoDB Cluster with MySQL Shell

## Prerequisites
- Three hosts (odd number, up to 9), same MySQL version, reachable on 3306 and the GR port
  (`33061` by default; `localAddress`).
- All tables InnoDB with primary keys; unique `server_id`; resolvable hostnames
  (`report_host` if DNS is odd).

## 1. Prepare each instance
```js
// mysqlsh --uri root@db1:3306
dba.checkInstanceConfiguration('root@db1:3306')
dba.configureInstance('root@db1:3306', {clusterAdmin: "'icadmin'@'%'", clusterAdminPassword: '...', restart: true})
```
`configureInstance` checks and fixes the settings InnoDB Cluster requires (`gtid_mode`,
`enforce_gtid_consistency`, row-based binlog format, `log_replica_updates`), creates the
cluster admin account, and restarts if needed. Repeat for db2, db3.

## 2. Create the cluster on the seed
```js
\connect icadmin@db1:3306
var c = dba.createCluster('prod', {memberWeight: 50, communicationStack: 'MYSQL', ipAllowlist: '10.0.0.0/16'})
```
`communicationStack: 'MYSQL'` (the InnoDB Cluster default; a plain Group Replication setup
defaults to `XCOM`) uses the MySQL protocol port with authentication instead of the
separate XCom protocol.

## 3. Add members
```js
c.addInstance('icadmin@db2:3306', {recoveryMethod: 'clone'})
c.addInstance('icadmin@db3:3306', {recoveryMethod: 'clone'})
c.status()
```
`clone` wipes the joiner and copies a physical snapshot from a donor (fast for big data);
`incremental` replays binlogs (only if the donors still have them). Large datasets: prefer clone.

## 4. MySQL Router on each app host
```bash
mysqlrouter --bootstrap icadmin@db1:3306 --account=router_app --user=mysqlrouter --directory /opt/router
systemctl enable --now mysqlrouter
```
Apps connect to Router: 6446 read-write, 6447 read-only (classic), 6450 read-write split.

## Settings worth deciding at creation
- `exitStateAction` (default `OFFLINE_MODE`) and `autoRejoinTries` for members that lose quorum.
- `consistency` (`BEFORE_ON_PRIMARY_FAILOVER` default) for read-your-writes after failover.
- `expelTimeout` for flaky networks.

## Gotchas
- Root via localhost-only accounts cannot be used for AdminAPI across hosts: use the cluster
  admin account created by configureInstance.
- Firewalls must allow member-to-member traffic both ways; clone also uses 3306.
- Large transactions over `group_replication_transaction_size_limit` (default 150000000 bytes, about 143 MB) are rolled back.

## Verify
`c.status()` shows `"status": "OK"`, three members `ONLINE`, one `PRIMARY`; an app write via
Router port 6446 lands on the primary and appears on secondaries.

## Checked

2026-10-31: confirmed `dba.checkInstanceConfiguration`/`dba.configureInstance` options (clusterAdmin, clusterAdminPassword, restart) and `Cluster.addInstance` recoveryMethod (auto/clone/incremental, default auto) on the MySQL Shell AdminAPI docs; `communicationStack` MYSQL as the InnoDB Cluster default on the dev.mysql.com group-replication-system-variables page; router ports 6446/6447/6448/6449 and the read-write-splitting port 6450 (bind_port) on the MySQL Router docs; the transaction size limit of 150000000 bytes on the Group Replication limitations page. Removed the unconfirmed 8.0.27+ and 8.2+ version notes and the binlog_transaction_dependency_tracking detail.
Method: documentation only; no commands were run.
