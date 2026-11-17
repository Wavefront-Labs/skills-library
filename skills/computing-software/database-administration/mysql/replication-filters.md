---
id: computing-software.database-administration.mysql.replication-filters
name: replication-filters
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, replication-filters, replicate-do-db, replicate-ignore-db, replicate-wild-do-table, change-replication-filter, binlog-do-db, cross-database-statements]
level: practitioner
status: docs-checked
description: "Replicate only some MySQL schemas or tables with replica-side filters (replicate-wild-do-table, CHANGE REPLICATION FILTER) and avoid the default-database trap."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/replication-rules.html
  - https://dev.mysql.com/doc/refman/8.4/en/change-replication-filter.html
  - https://dev.mysql.com/doc/refman/8.4/en/replication-options-replica.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replication filters

**Goal:** a replica that applies only the schemas/tables it needs, with predictable behaviour for cross-database statements.

## Filter on the replica, not the source
Source-side `binlog-do-db`/`binlog-ignore-db` decide what is logged at all (with statement logging they test the default database), so they affect every replica. The manual says not to use them to control what is replicated: filter on the replica instead.

## Options
| Option | Matches |
|---|---|
| `replicate-do-db` / `replicate-ignore-db` | By database (semantics depend on format, see below) |
| `replicate-do-table` / `replicate-ignore-table` | `db.table` exact |
| `replicate-wild-do-table` / `replicate-wild-ignore-table` | `db.tbl%` patterns |
| `replicate-rewrite-db` | `from_db->to_db` |

```ini
[mysqld]
replicate-wild-do-table = app.%
replicate-wild-ignore-table = app.tmp\_%
```
Online (stop the SQL thread first; without `FOR CHANNEL` the filter is global, applying to all channels):
```sql
STOP REPLICA SQL_THREAD;
CHANGE REPLICATION FILTER REPLICATE_WILD_DO_TABLE = ('app.%');   -- or ... FOR CHANNEL channel_1;
START REPLICA SQL_THREAD;
SELECT * FROM performance_schema.replication_applier_filters;
```
Not persisted: lost on restart, so add to my.cnf as well (`replicate-wild-do-table=channel_1:app.%` for a named channel). Setting a filter type with the statement replaces existing rules of that type; `= ()` empties it.

## The default-database trap
With statement-format events, `*-do-db` checks the **default database** (`USE`), not the database named in the statement:
```sql
USE other; UPDATE app.orders SET ...;  -- ignored by replicate-do-db=app under SBR
```
With row-format events (`binlog_format=ROW`), `*-do-db` checks the database where data changes, but DDL is always logged as statements, so it needs the right `USE`. Table-level options check the tables operated on. Avoid mixing do-* and ignore-* options, or wildcard and non-wildcard ones.

## Gotchas
- A filtered replica does not hold the full dataset, so do not promote it as a full copy.
- Statement-based replication stops if one statement touches a table included by `*-do-table` and another ignored by `*-ignore-table`; only row-logged DML can do this.
- Table filters apply only to tables a statement names, not tables updated implicitly (a `GRANT` is not hit by `mysql.%`).
- Global filters cannot be set on a Group Replication member, and channel filters cannot be set on `group_replication_applier` or `group_replication_recovery`.

## Verify
Write to a filtered-out table on the source and confirm the replica's table is unchanged. Inspect the active rules with `performance_schema.replication_applier_filters` (columns include `CHANNEL_NAME`, `FILTER_NAME`, `FILTER_RULE`, `CONFIGURED_BY`, `COUNTER`).

## Checked
2026-11-01. Confirmed against MySQL 8.4 pages "How Servers Evaluate Replication Filtering Rules", database-level and table-level evaluation, "CHANGE REPLICATION FILTER", channel based filters and the replication_applier_filters table. Removed: PITR claim, DDL matching claim for wild options, the empty-transaction GTID claim and the foreign-key divergence claim.
Method: documentation only; no commands were run.

