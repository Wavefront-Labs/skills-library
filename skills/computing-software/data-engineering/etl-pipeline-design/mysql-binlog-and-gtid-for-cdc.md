---
id: computing-software.data-engineering.etl-pipeline-design.mysql-binlog-and-gtid-for-cdc
name: mysql-binlog-and-gtid-for-cdc
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, cdc, binlog, gtid, mysql, debezium, binlog-retention, replica-failover]
level: advanced
status: docs-checked
description: "Prepare MySQL for log-based CDC: ROW binlog with full image, GTIDs for failover-safe positions, binlog retention, CDC user grants, and reading from replicas."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
  - https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MySQL binlog and GTID setup for CDC

**Goal:** a Debezium MySQL connector can read every change, survive failover, and not lose its position because binlogs were purged.

## Server settings (from the Debezium setup guide)
```ini
[mysqld]
server-id                  = 223344
log_bin                    = mysql-bin
binlog_format              = ROW
binlog_row_image           = FULL
binlog_expire_logs_seconds = 864000
gtid_mode                  = ON
enforce_gtid_consistency   = ON
binlog_rows_query_log_events = ON
```
- `server-id` must be unique per server and replication client in the cluster. `binlog_format` must be ROW and `binlog_row_image` must be FULL.
- `binlog_expire_logs_seconds` replaces the deprecated `expire_logs_days`; the MySQL default is 2592000 (30 days). Set it to fit your environment.
- `binlog_rows_query_log_events` adds the original SQL statement to binlog entries (optional, for debugging).
- On Amazon RDS, automated backups must be enabled or the binlog stays disabled despite these settings.
- Check status with `SELECT variable_value FROM performance_schema.global_variables WHERE variable_name='log_bin'` (MySQL 8) or the information_schema equivalent (5.x). `binlog_row_value_options` must not be PARTIAL_JSON for UPDATE events to be consumed.

## CDC user
```sql
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'user' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
```
- SELECT, RELOAD and SHOW DATABASES are used only during snapshots; REPLICATION SLAVE lets it read the binlog; REPLICATION CLIENT (SHOW MASTER STATUS, SHOW SLAVE STATUS, SHOW BINARY LOGS) is always required.
- On hosted options such as RDS or Aurora that disallow a global read lock, the snapshot uses table-level locks and the user also needs LOCK TABLES.

## GTIDs
GTIDs uniquely identify transactions on servers in a cluster. They are not required by the connector, but they simplify replication and make it easier to confirm primary and replica consistency. Because most HA MySQL clusters use GTIDs, replicas track changes from any primary, and the connector can fail over to another replica as long as that replica has caught up with every transaction the first one had (GTID source include/exclude settings help it find its position). Enable with `gtid_mode=ON` and `enforce_gtid_consistency=ON` (required when using GTIDs); confirm with `show global variables like '%GTID%'`.

## Reading from a replica
The connector can follow a primary or a replica that has its binlog enabled, but sees only changes visible to that server.

## Retention
If the logs are pruned while the connector is down, its saved position may no longer be available on restart. Size `binlog_expire_logs_seconds` above the longest expected outage plus recovery.

## Schema history
The connector records all DDL with binlog positions in an internal schema history Kafka topic, used to rebuild table structures on restart. It is for connector use only and must have a single partition (never partition it).

## Verify
- [ ] Failover drill in staging: connector resumes on the new server without a re-snapshot.
- [ ] Retention exceeds the maximum tolerated CDC downtime, and is documented.

## Checked
Method: docs-only read on 2026-11-09 of the Debezium MySQL page (setup, GTID, primary/replica and schema history sections via targeted reads of a very long page) and the MySQL 8.0 binary-log options page (binlog_expire_logs_seconds entry only). The MySQL replication-gtids page returned only navigation text, so that source was removed. Dropped unstated items: RDS `rds_set_configuration` and Cloud SQL steps, the exact grant list for managed services beyond LOCK TABLES, `log_replica_updates` and 5.7 variable names, the binlog_row_image=MINIMAL gotcha, error message text, large-transaction tuning, the 3-7 day retention figure, and SHOW BINARY LOG STATUS in 8.2.
