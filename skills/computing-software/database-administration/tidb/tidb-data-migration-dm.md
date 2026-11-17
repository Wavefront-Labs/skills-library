---
id: computing-software.database-administration.tidb.tidb-data-migration-dm
name: tidb-data-migration-dm
category: computing-software
field: database-administration
product: tidb
tags: [tidb, dm, data-migration, mysql-migration, binlog, shard-merge, dmctl, online-ddl, gh-ost]
level: practitioner
status: docs-checked
description: "Use TiDB Data Migration (DM) for full and incremental replication from MySQL-compatible databases, including shard merge, filters, install and restrictions."
sources: ["https://docs.pingcap.com/tidb/stable/dm-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tidb data migration dm

DM is a task management platform for full migration and incremental replication from MySQL-compatible sources (MySQL, MariaDB, Aurora MySQL) into TiDB.

Features:
- MySQL protocol compatible with most MySQL 5.7 and 8.0 features and syntax.
- Parses and replicates DML and DDL events from the binlog.
- Merges and migrates MySQL shards from many upstream instances into one TiDB database, with custom rules and automatic handling of upstream shard DDL.
- Event filters by type, regular expression or SQL expression.
- Central management of thousands of nodes and many concurrent tasks.
- Optimised handling of online schema change tools such as gh-ost and pt-osc, avoiding migration of intermediate data.
- High availability: tasks reschedule across nodes, and a small number of node crashes does not affect running tasks.

Install: `curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh` then `tiup install dm dmctl`.

Restrictions:
- Sources: MySQL 5.6 to 8.0; MariaDB 10.1.2 or later (experimental). With primary-secondary upstream chains, use MySQL above 5.7.1 or MariaDB 10.1.3 or later.
- DM uses the TiDB parser, so only DDL supported by TiDB works. On an incompatible statement it errors and you handle it with dmctl by skipping or replacing the statement.
- View DDL and DML are not replicated; create views downstream manually.
- DM does not support migrating `charset=GBK` tables to TiDB clusters earlier than v5.4.0.
- MySQL 8.0 binlog `Transaction_payload_event` is unsupported and can cause inconsistency.
- MySQL vector data types are not supported.

Since v5.3, DM versions follow TiDB versions.

## Checked

2026-11-04. Confirmed against the TiDB Data Migration Overview page: feature list, install commands, restrictions, version policy. Fixed the supported MySQL range (5.6 to 8.0) and removed the unconfirmed GB18030 claim.
Method: documentation only; no commands were run.
