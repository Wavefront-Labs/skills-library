---
id: computing-software.database-administration.mysql.gtid-replica-setup-with-change-replication-source
name: gtid-replica-setup-with-change-replication-source
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, change-replication-source, replication, gtid, source-auto-position, start-replica, replication-user, show-replica-status, replica-provisioning]
level: practitioner
status: docs-checked
description: "Build a MySQL 8 GTID replica from scratch: source settings, replication user, seeding data, CHANGE REPLICATION SOURCE TO with auto-position and TLS, and health checks."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-gtids-howto.html
  - https://dev.mysql.com/doc/refman/8.4/en/change-replication-source-to.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-howto-repuser.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting up a GTID replica (CHANGE REPLICATION SOURCE TO)

**Goal:** a new replica that follows the source by GTID, survives restarts and can be repointed during failover without hunting coordinates.

## 1. Both servers
```ini
[mysqld]
server_id = 2                         # unique per server
gtid_mode = ON
enforce_gtid_consistency = ON
log_bin = binlog
log_replica_updates = ON              # default in 8.4; needed for chaining/failover
binlog_format = ROW
relay_log_recovery = ON               # replica: discard possibly corrupt relay logs after crash
read_only = ON
super_read_only = ON                  # replica only
```
Switching an existing non-GTID source online goes through `gtid_mode` OFF_PERMISSIVE -> ON_PERMISSIVE -> ON with `enforce_gtid_consistency=WARN` first.

## 2. Replication user (source)
```sql
CREATE USER 'repl'@'10.0.%' IDENTIFIED BY '...' REQUIRE SSL;
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'10.0.%';
```

## 3. Seed data
Clone plugin, XtraBackup, or `mysqldump --single-transaction --source-data=2 --set-gtid-purged=ON`. The replica's `gtid_purged`/`gtid_executed` must equal the snapshot's GTID set (the dump sets it; `RESET BINARY LOGS AND GTIDS` — the replacement for the removed `RESET MASTER` — first if the replica has its own GTIDs).

## 4. Point and start
```sql
CHANGE REPLICATION SOURCE TO
  SOURCE_HOST = 'db1.internal', SOURCE_PORT = 3306,
  SOURCE_USER = 'repl', SOURCE_PASSWORD = '...',
  SOURCE_AUTO_POSITION = 1,
  SOURCE_SSL = 1, SOURCE_SSL_VERIFY_SERVER_CERT = 1, SOURCE_SSL_CA = '/etc/mysql/ca.pem',
  GET_SOURCE_PUBLIC_KEY = 1,          -- caching_sha2_password without TLS
  SOURCE_CONNECT_RETRY = 10, SOURCE_RETRY_COUNT = 8640;
START REPLICA;
```

## 5. Health
```sql
SHOW REPLICA STATUS\G
-- Replica_IO_Running: Yes, Replica_SQL_Running: Yes, Seconds_Behind_Source small,
-- Last_IO_Error / Last_SQL_Error empty, Retrieved_Gtid_Set vs Executed_Gtid_Set
SELECT * FROM performance_schema.replication_applier_status_by_worker WHERE LAST_ERROR_NUMBER <> 0;
```

## Gotchas
- The source refuses the connection with `ER_SOURCE_HAS_PURGED_REQUIRED_GTIDS` (source binlogs purged before the replica retrieved the transactions): reseed.
- `Seconds_Behind_Source` is NULL when the receiver thread is disconnected and the relay log is exhausted (it is 0 while the relay log is still being applied); alert on the thread states too, or use a heartbeat table (pt-heartbeat).
- Credentials in `CHANGE REPLICATION SOURCE` are stored in `mysql.slave_master_info`; supply them at `START REPLICA USER=... PASSWORD=...` to avoid storing.

## Verify
Write a row on the source; it appears on the replica within a second, and `SHOW REPLICA STATUS` shows matching executed GTID sets.

## Checked

2026-10-31: confirmed gtid_mode/enforce_gtid_consistency requirements and the online GTID-mode steps (enforce_gtid_consistency=WARN first, then OFF_PERMISSIVE/ON_PERMISSIVE, wait for Ongoing_anonymous_transaction_count=0, then GTID_MODE=ON) on dev.mysql.com; log_replica_updates default ON in 8.4; the REPLICATION SLAVE grant for the replication user; CHANGE REPLICATION SOURCE TO options (SOURCE_AUTO_POSITION, SOURCE_CONNECT_RETRY default 60, SOURCE_RETRY_COUNT default 10, GET_SOURCE_PUBLIC_KEY, SOURCE_SSL/SOURCE_SSL_VERIFY_SERVER_CERT); RESET BINARY LOGS AND GTIDS (takes the place of the no-longer-supported RESET MASTER); Seconds_Behind_Source NULL semantics; credentials stored in the mysql.slave_master_info metadata repository with START REPLICA-supplied credentials as the alternative; mysqldump --source-data and --set-gtid-purged. Removed the 8.0.23+ renaming note and the 1236 error number (8.4 documents ER_SOURCE_HAS_PURGED_REQUIRED_GTIDS).
Method: documentation only; no commands were run.
