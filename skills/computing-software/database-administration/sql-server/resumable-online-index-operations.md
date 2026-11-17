---
id: computing-software.database-administration.sql-server.resumable-online-index-operations
name: resumable-online-index-operations
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, azure-sql, resumable-index, resumable-index-rebuild, online-index-rebuild, max-duration, wait-at-low-priority]
level: advanced
status: docs-checked
description: "Rebuild or create big SQL Server indexes online and resumably (RESUMABLE=ON, MAX_DURATION, PAUSE/RESUME) to fit maintenance windows and survive failovers."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/guidelines-for-online-index-operations
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql#resumable--on--off
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/guidelines-for-online-index-operations
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-index-resumable-operations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resumable online index operations

**Goal:** a 6-hour index rebuild runs in 1-hour slices across nights, and a
failover or cancel doesn't throw away the progress.

## Syntax (SQL Server 2017+ rebuild, 2019+ create; Azure SQL)
```sql
ALTER INDEX ix_orders_customer ON dbo.orders
  REBUILD WITH (ONLINE = ON (WAIT_AT_LOW_PRIORITY (MAX_DURATION = 5 MINUTES, ABORT_AFTER_WAIT = SELF)),
                RESUMABLE = ON, MAX_DURATION = 60 MINUTES);

CREATE INDEX ix_orders_status ON dbo.orders (status, created_at)
  WITH (ONLINE = ON, RESUMABLE = ON, MAX_DURATION = 60);
```
`MAX_DURATION` (minutes, greater than 0; `MINUTES` optional) is the time slice: when it elapses the operation **pauses** (not rolls back). The
`WAIT_AT_LOW_PRIORITY` options (`ABORT_AFTER_WAIT` = NONE, SELF or BLOCKERS) are nested inside `ONLINE = ON (...)`. `RESUMABLE` is not stored in
index metadata, applies only to that statement, is not supported with the `ALL` keyword, and cannot run inside an explicit transaction.
```sql
ALTER INDEX ix_orders_customer ON dbo.orders PAUSE;
ALTER INDEX ix_orders_customer ON dbo.orders RESUME WITH (MAX_DURATION = 60 MINUTES);   -- or re-run the original ALTER INDEX ... REBUILD
-- KILL <session_id> also pauses the operation
ALTER INDEX ix_orders_customer ON dbo.orders ABORT;
SELECT name, state_desc, percent_complete, last_pause_time, page_count
FROM sys.index_resumable_operations;
```
2019+ database-scoped default: `ALTER DATABASE SCOPED CONFIGURATION SET ELEVATE_RESUMABLE = WHEN_SUPPORTED;`

## Why it matters
- Restarts after an unexpected failure, a database failover, or `ALTER INDEX ... PAUSE` from where it stopped.
- Resumable operations do not need one large transaction, so the log can be truncated during them; a non-resumable index
  operation keeps the log from truncating until it completes (log backups still run). With ADR enabled online operations do not grow the log much,
  but the persistent version store can grow.

## Costs and limits
- ONLINE (and so RESUMABLE) is not available in every edition: check Microsoft's editions and supported features page.
- While paused, both the original index and the new one need disk space and are updated by DML. Any transaction needing a table-level
  exclusive lock, such as `INSERT ... WITH (TABLOCK)`, fails with error 10637 until the operation is resumed or aborted.
- Not supported: `SORT_IN_TEMPDB = ON`, disabled indexes, filtered indexes.
- Online operations still take a shared (S) or schema-modification (Sch-M) lock at the end; `WAIT_AT_LOW_PRIORITY` manages that.

## Verify
`sys.index_resumable_operations` (state 0 running, 1 paused; `percent_complete`, `last_pause_time`, `page_count`) is empty after completion; log
space was reusable between slices.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Guidelines for Online Index Operations, Perform index operations online, ALTER INDEX and sys.index_resumable_operations (2017-2025).
Confirmed: version gates (ALTER INDEX 2017, CREATE INDEX 2019), corrected the `WAIT_AT_LOW_PRIORITY` nesting inside `ONLINE = ON (...)`, MAX_DURATION units, PAUSE/RESUME/ABORT, restrictions (SORT_IN_TEMPDB, disabled, filtered, ALL, explicit transactions), error 10637, view columns, ELEVATE_RESUMABLE scoped configuration. Removed unconfirmed claims: columnstore, computed-column and timestamp restrictions, and the edition list.
Method: documentation only; no commands were run.
