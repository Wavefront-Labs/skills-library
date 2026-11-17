---
id: computing-software.database-administration.query-optimisation.temp-table-and-table-variable-statistics
name: temp-table-and-table-variable-statistics
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, temp-table-statistics, table-variables, temporary-tables, query-statistics, deferred-compilation]
level: practitioner
status: draft
description: "Get accurate estimates for temporary tables and table variables: SQL Server table variable deferred compilation, temp table auto stats, PostgreSQL ANALYZE on temp tables."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing-details#table-variable-deferred-compilation
  - https://www.postgresql.org/docs/current/sql-createtable.html#SQL-CREATETABLE-TEMPORARY
  - https://learn.microsoft.com/en-us/sql/relational-databases/statistics/statistics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Statistics for temp tables and table variables

## SQL Server
| | Table variable `@t` | Temp table `#t` |
|---|---|---|
| Column statistics | None | Auto-created/updated |
| Row count estimate | 1 row (before 2019 compat 150); actual count at first compile with deferred compilation (2019+) | From stats |
| Recompiles | No (fewer recompiles) | When stats change thresholds |
| Indexes | Inline PK/unique/indexes (2014+) | Any |

Guidance:
- Small sets (< ~100 rows) or high-frequency procedures: table variables avoid recompiles.
- Anything joined to large tables or filtered with skewed data: temp tables, because column distribution matters, not just row count.
- On older compat levels, `OPTION (RECOMPILE)` on the statement lets the optimiser see the table variable's actual row count.
- Temp table statistics caching in procedures can reuse stale stats across executions; `UPDATE STATISTICS #t` after populating if plans are wrong.

## PostgreSQL
Autovacuum **never** analyzes temporary tables (they are session-private). After filling one, run:
```sql
CREATE TEMP TABLE tmp_ids AS SELECT id FROM ... ;
ANALYZE tmp_ids;
```
Without it the planner assumes a default size (based on pages, often wildly off) and no distribution stats, leading to bad join choices. Consider `ON COMMIT DROP` for transaction-scoped temp tables; heavy temp table churn bloats the catalog (`pg_class`, `pg_attribute`): reuse with TRUNCATE or use CTEs/arrays for small sets.

## MySQL
Internal temp tables have no user stats; user `CREATE TEMPORARY TABLE` InnoDB tables get index statistics computed on `ANALYZE TABLE`. Prefer derived tables/CTEs that the optimiser can merge.

## Oracle
Global temporary tables: session-private statistics (12c+ default `GLOBAL_TEMP_TABLE_STATS = SESSION`), or dynamic sampling at parse time.

## Verify
Plan estimate for the temp table scan matches its actual row count; joins choose hash vs nested loop sensibly for large vs small temp sets.
