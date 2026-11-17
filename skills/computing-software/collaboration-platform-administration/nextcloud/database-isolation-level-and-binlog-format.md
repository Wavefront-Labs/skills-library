---
id: computing-software.collaboration-platform-administration.nextcloud.database-isolation-level-and-binlog-format
name: database-isolation-level-and-binlog-format
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [transaction-isolation, read-committed, binlog-format, mariadb, my-cnf]
level: advanced
status: docs-checked
description: "Configure MariaDB or MySQL for Nextcloud with READ-COMMITTED isolation, ROW binlog format and utf8mb4 defaults to avoid data loss under parallel sync load."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_database/linux_database_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make the database server match what Nextcloud assumes.

Supported databases: MySQL or MariaDB, PostgreSQL, and Oracle (Enterprise only). PostgreSQL and MariaDB are the recommended engines. Check the system requirements page for the version you choose, because not every version is recommended. Install the server before deploying Nextcloud; setup itself goes through the installation wizard and you should not need to edit values by hand.

Nextcloud uses the `TRANSACTION_READ_COMMITTED` isolation level. Some database configurations enforce a different one. To avoid data loss under high load, such as many sync clients doing parallel operations, configure it accordingly.

For MariaDB or MySQL set these in the server configuration (for example `/etc/mysql/my.cnf`) so they persist after a restart, and verify `transaction_isolation` and `binlog_format`:

```
[mysqld]
transaction_isolation = READ-COMMITTED
binlog_format = ROW
```

The manual's sample file also sets:
- `[client] default-character-set = utf8mb4`
- `character_set_server = utf8mb4` and `collation_server = utf8mb4_bin`
- `innodb_file_per_table=1`
- `skip_name_resolve = 1`, `innodb_buffer_pool_size = 128M`, `innodb_flush_log_at_trx_commit = 2`
- `slow_query_log = 1` with `long_query_time = 1`

Treat the sizing numbers as a starting point to tune, not a requirement. The sample also carries `query_cache_*` and `innodb_large_prefix` lines; check them against your database version before copying.

Check: the running server reports `READ-COMMITTED` for `transaction_isolation` and `ROW` for `binlog_format`.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_database/linux_database_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
