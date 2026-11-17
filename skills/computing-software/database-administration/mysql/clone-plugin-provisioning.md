---
id: computing-software.database-administration.mysql.clone-plugin-provisioning
name: clone-plugin-provisioning
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, clone-plugin, clone-instance, remote-clone, replica-provisioning, clone-valid-donors, backup-admin, performance-schema-clone-status]
level: practitioner
status: docs-checked
description: "Provision a MySQL replica or Group Replication member from a live donor with the clone plugin, including privileges, donor list, monitoring and replication start."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/clone-plugin.html
  - https://dev.mysql.com/doc/refman/8.4/en/clone-plugin-remote.html
  - https://dev.mysql.com/doc/refman/8.4/en/clone-plugin-monitoring.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The clone plugin

**Goal:** turn an empty MySQL instance into a physical copy of a running server over the network in one SQL command, then attach it as a replica.

## Setup (both sides)
```sql
INSTALL PLUGIN clone SONAME 'mysql_clone.so';          -- or plugin-load-add=mysql_clone.so in my.cnf
-- donor
CREATE USER clone_donor@'%' IDENTIFIED BY '...'; GRANT BACKUP_ADMIN ON *.* TO clone_donor@'%';
-- recipient
CREATE USER clone_user@'localhost' IDENTIFIED BY '...'; GRANT CLONE_ADMIN ON *.* TO clone_user@'localhost';
SET GLOBAL clone_valid_donor_list = 'db1.internal:3306';
```
Same MySQL version series (for example 8.4.0 with 8.4.11), same OS/platform, enough disk.

## Clone
```sql
-- on the recipient, as clone_user
CLONE INSTANCE FROM 'clone_donor'@'db1.internal':3306 IDENTIFIED BY '...' REQUIRE SSL;
```
The recipient's data is replaced, then mysqld restarts automatically (needs a supervisor: systemd or mysqld_safe). Without a supervisor it shuts down and you start it.

## Monitor
```sql
SELECT STATE, BEGIN_TIME, END_TIME, SOURCE, ERROR_NO, ERROR_MESSAGE, BINLOG_FILE, BINLOG_POSITION, GTID_EXECUTED FROM performance_schema.clone_status;
SELECT STAGE, STATE, ESTIMATE, DATA, NETWORK FROM performance_schema.clone_progress;
```

## Start replication
GTID: the clone carries `gtid_executed`, so
```sql
CHANGE REPLICATION SOURCE TO SOURCE_HOST='db1.internal', SOURCE_USER='repl', SOURCE_PASSWORD='...', SOURCE_AUTO_POSITION=1, SOURCE_SSL=1;
START REPLICA;
```
Non-GTID: use `BINLOG_FILE`/`BINLOG_POSITION` from `clone_status`. InnoDB Cluster/Group Replication uses clone automatically (`cluster.addInstance(..., {recoveryMethod:'clone'})`).

## Throttling and impact
`clone_max_concurrency`, `clone_max_data_bandwidth`, `clone_max_network_bandwidth` throttle the operation and are set on the recipient. Donor keeps serving traffic. Concurrent DDL is permitted on the donor by default; `clone_block_ddl = ON` restores blocking.

## Gotchas
- Only InnoDB data is cloned; MyISAM/CSV tables come across empty.
- Recipient user accounts are replaced by the donor's; the clone_user disappears after restart.
- Configuration files are not part of the clone; after the restart check `server_id`, `report_host` and `performance_schema.persisted_variables` on the recipient.

## Verify
`clone_status.STATE = 'Completed'`, `SHOW REPLICA STATUS` shows both threads Yes and lag dropping to 0.

## Checked

2026-10-31: confirmed INSTALL PLUGIN clone SONAME 'mysql_clone.so' and plugin-load-add, BACKUP_ADMIN on the donor and CLONE_ADMIN on the recipient, clone_valid_donor_list, replacement of recipient data and automatic restart, same-version-series requirement, concurrent DDL permitted on the donor by default, and the performance_schema clone_status/clone_progress columns (STATE, BEGIN_TIME, END_TIME, SOURCE, ERROR_NO, ERROR_MESSAGE, BINLOG_FILE, BINLOG_POSITION, GTID_EXECUTED; STAGE, STATE, ESTIMATE, DATA, NETWORK) on the dev.mysql.com 8.4 clone-plugin and performance-schema-clone-* pages. Removed the unconfirmed 8.0.17+/8.0.37 version notes and the innodb_page_size restore requirement.
Method: documentation only; no commands were run.
