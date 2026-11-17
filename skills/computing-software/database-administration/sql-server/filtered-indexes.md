---
id: computing-software.database-administration.sql-server.filtered-indexes
name: filtered-indexes
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, filtered-index, filtered-statistics, set-options, parameterized-queries, unique-where-not-null]
level: advanced
status: docs-checked
description: "Create SQL Server filtered indexes for hot subsets and unique-where-not-null rules, and avoid the SET options and parameterization traps that stop queries using them."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/create-filtered-indexes
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtered indexes

**Goal:** a small index on just the rows that matter (open orders, non-null
emails) that the optimizer actually uses.

## Create
```sql
CREATE INDEX ix_orders_open ON dbo.orders (customer_id, created_at)
  INCLUDE (total) WHERE status = 'open';

-- uniqueness only among non-null values
CREATE UNIQUE INDEX ux_users_email ON dbo.users (email) WHERE email IS NOT NULL;
```
Filter predicate grammar (CREATE INDEX): `column IN (constants)` or `column <comparison_op> constant`, combined only with AND.
Microsoft also notes: no `LIKE`; one table only (use a view for multi-table logic); no computed column in the filter (a computed column
may be a key or included column); no CLR-typed filter columns; no filtered index on a view; filters cannot be on PK or unique
constraints but can be on a `UNIQUE` index. A conversion on the left side of the comparison raises an error: put CAST/CONVERT on the right.
Modify a filter with `CREATE INDEX ... WITH DROP_EXISTING`. Creating needs ALTER on the table plus sysadmin or db_ddladmin/db_owner roles.

## When the optimizer will NOT use it
- The query's `WHERE` clause must be a subset of the filter's (Microsoft's rule); a predicate the optimizer cannot show
  to be inside the filter (for example a different or broader condition) does not qualify. Check the actual plan.
- Put the filter column in the key or INCLUDE list when the query predicate uses it in a comparison that is not equivalent
  to the filter, or when it is in the select list; otherwise not needed. The clustered key is added automatically.

## SET options
Required whenever you create a filtered index, run INSERT/UPDATE/DELETE/MERGE that changes data in it, or the optimizer uses it
for a plan: `ANSI_NULLS`, `ANSI_PADDING`, `ANSI_WARNINGS`, `ARITHABORT`, `CONCAT_NULL_YIELDS_NULL`, `QUOTED_IDENTIFIER` ON and
`NUMERIC_ROUNDABORT` OFF. Wrong settings make creation fail or roll back the data-changing statement. DB-Library clients default
most of these to OFF, and OLE DB/ODBC default `ARITHABORT` to OFF (ANSI_WARNINGS ON implies it on compat 90+).
Check legacy clients, jobs and procedures.

## Statistics
Filtered indexes get filtered statistics covering only the rows in the index, which Microsoft says are more accurate than
full-table statistics. Include them in your statistics maintenance.

## Verify
```sql
SELECT name, filter_definition FROM sys.indexes WHERE has_filter = 1;
```
Actual execution plan shows the filtered index in use (Microsoft's own check).

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 Create Filtered Indexes, Index Architecture and Design Guide, and CREATE INDEX pages (2017-2025).
Confirmed: filter predicate grammar and restrictions, subset rule, key/include guidance, required SET options and when they apply, filtered statistics. `sys.indexes` has `has_filter` and `filter_definition` columns. Removed unconfirmed claims: error 1934, parameterised-predicate and RECOMPILE advice, stale-statistics-threshold claim, the Ola Hallengren parameter and the NULL-uniqueness aside.
Method: documentation only; no commands were run.
