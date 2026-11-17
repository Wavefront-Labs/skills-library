---
id: computing-software.messaging-and-integration.debezium.mysql-binlog-configuration
name: mysql-binlog-configuration
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mysql, binlog, row-format, server-config]
level: practitioner
status: docs-checked
description: "Set server-id, log_bin, binlog_format=ROW, binlog_row_image=FULL and retention so Debezium can read the MySQL binlog."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Debezium reads the MySQL binary log, so it must be enabled and in row format. First check status:

```sql
SELECT variable_value FROM performance_schema.global_variables WHERE variable_name='log_bin';
```

(MySQL 5.x uses `information_schema.global_variables`.) If it is OFF, add to the server configuration file:

```
server-id = 223344
log_bin = mysql-bin
binlog_format = ROW
binlog_row_image = FULL
binlog_expire_logs_seconds = 864000
```

Meaning of each:

- `server-id` must be unique among all servers and replication clients in the cluster.
- `log_bin` is the base name of the binlog files.
- `binlog_format` must be `ROW`.
- `binlog_row_image` must be `FULL`.
- `binlog_expire_logs_seconds` replaces the deprecated `expire_logs_days`; its default is 2592000 (30 days). Set it to match the needs of your environment.

Amazon RDS: enable automated backups on the instance. Without them the binlog stays disabled even if the settings are applied.

Also check `binlog_row_value_options`: for the connector to consume `UPDATE` events it must not be `PARTIAL_JSON`.

Gotcha: if the connector is down longer than retention, the position is purged and it must re-snapshot (see mysql-failure-recovery-and-purged-binlog).

Check: re-run the status query after restart and confirm `ON`.

## Checked

2026-11-03. Page used: the Debezium mysql connector reference, https://debezium.io/documentation/reference/stable/connectors/mysql.html.
Confirmed against it: log_bin check query, server-id, binlog_format, binlog_row_image, binlog_expire_logs_seconds default 2592000, RDS automated backups, PARTIAL_JSON.
Removed or reworded: the advice to size retention beyond any outage.
Method: documentation only; no commands were run.
