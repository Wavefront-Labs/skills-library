---
id: computing-software.database-administration.query-optimisation.large-in-lists
name: large-in-lists
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, query-anti-patterns, large-in-list, any-array, table-valued-parameter, temp-table, plan-cache-pollution]
level: practitioner
status: draft
description: "Replace huge IN (...) lists built by applications with array parameters, VALUES joins, table-valued parameters or temp tables, and why big literal lists hurt."
sources:
  - https://www.postgresql.org/docs/current/functions-comparisons.html#FUNCTIONS-COMPARISONS-ANY-SOME
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/use-table-valued-parameters-database-engine
  - https://dev.mysql.com/doc/refman/8.4/en/range-optimization.html#equality-range-optimization
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Large IN lists

## Why `WHERE id IN (1, 2, ..., 50000)` hurts
- Every distinct list length is a different statement text: plan cache pollution and constant
  re-parsing (SQL Server, Oracle shared pool, pg_stat_statements entries).
- Parse and plan time grows with list size; very long lists hit limits (Oracle: 1000 expressions
  per IN list, ORA-01795; SQL Server: 2100 parameters per request; drivers' bind limits).
- Estimates for long lists can be poor (MySQL switches from index dives to index statistics
  above `eq_range_index_dive_limit`, default 200).

## Better patterns
**PostgreSQL: one array parameter**
```sql
SELECT * FROM orders WHERE id = ANY($1::bigint[]);
-- or join for very large sets
SELECT o.* FROM orders o JOIN unnest($1::bigint[]) AS t(id) ON o.id = t.id;
```
One statement text regardless of size; planner sees a single parameter.

**SQL Server: table-valued parameter**
```sql
CREATE TYPE dbo.IdList AS TABLE (Id bigint PRIMARY KEY);
-- proc parameter: @Ids dbo.IdList READONLY
SELECT o.* FROM dbo.Orders o JOIN @Ids i ON i.Id = o.Id;
```
Or pass JSON/CSV and parse with `OPENJSON` / `STRING_SPLIT`.

**Oracle**: collection types with `TABLE(:ids)` / `MEMBER OF`, or a global temporary table.

**Any engine: temp table**
Bulk-insert the ids into a temporary table (indexed, analyzed if large), then join. Best when
the list is huge (100k+) or reused in several queries.

**VALUES list join**
`JOIN (VALUES (1),(2),(3)) AS v(id) ON ...` keeps it set-based but still varies the text.

## Often the real fix
A huge IN list usually means the application fetched ids from one query and fed them to another.
Express both as one SQL statement (join or subquery) and let the database do it.

## Verify
`pg_stat_statements` / Query Store shows a single normalized statement instead of thousands of
variants; latency for large inputs is stable; plans show a hash or nested-loop join with the
parameter set.
