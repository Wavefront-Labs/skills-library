---
id: computing-software.database-administration.sql-server.database-options-auto-shrink-auto-close-page-verify
name: database-options-auto-shrink-auto-close-page-verify
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, auto-shrink, auto-close, page-verify, checksum, database-options, read-committed-snapshot, shrinkfile]
level: practitioner
status: docs-checked
description: "Audit and fix SQL Server database options: turn off AUTO_SHRINK and AUTO_CLOSE, set PAGE_VERIFY CHECKSUM, and choose RCSI and async statistics deliberately."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-set-options
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinkfile-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-databases-transact-sql
  - https://learn.microsoft.com/en-us/sql/relational-databases/databases/shrink-a-file
  - https://dbachecks.readthedocs.io/en/latest/functions/Invoke-DbcCheck/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database options: AUTO_SHRINK, AUTO_CLOSE, PAGE_VERIFY

## Audit every database
```sql
SELECT name, is_auto_shrink_on, is_auto_close_on, page_verify_option_desc,
       is_read_committed_snapshot_on, snapshot_isolation_state_desc,
       is_auto_create_stats_on, is_auto_update_stats_on, is_auto_update_stats_async_on,
       compatibility_level, recovery_model_desc, target_recovery_time_in_seconds
FROM sys.databases ORDER BY name;
```

## Fix the bad ones
```sql
ALTER DATABASE [<DB>] SET AUTO_SHRINK OFF;
ALTER DATABASE [<DB>] SET AUTO_CLOSE OFF;
ALTER DATABASE [<DB>] SET PAGE_VERIFY CHECKSUM;
ALTER DATABASE [<DB>] SET TARGET_RECOVERY_TIME = 60 SECONDS;  -- indirect checkpoints (the default for new databases since SQL Server 2016)
```
- **AUTO_SHRINK**: the file shrinks, then autogrows again; each shrink moves pages from the end
  to the front, leaving indexes heavily fragmented, and burns CPU, IO and log. Never on in
  production. If space must be reclaimed once: `DBCC SHRINKFILE (logical_name, target_MB)`, then
  rebuild the affected indexes. SQL Server 2022+ adds `WITH WAIT_AT_LOW_PRIORITY (ABORT_AFTER_WAIT = SELF | BLOCKERS)` to `DBCC SHRINKFILE` for data files to limit blocking.
- **AUTO_CLOSE**: the database closes when the last user leaves; the next connection pays the
  startup cost and its plans are flushed. Azure SQL Database does not offer the option.
- **PAGE_VERIFY CHECKSUM**: the default for new databases; older databases can still be `TORN_PAGE_DETECTION` or
  `NONE`. The checksum is calculated when a page is written, so existing pages are protected only once rewritten (for example by an index rebuild). Changing an option in `model` sets the default for new databases.

## Deliberate choices
- `READ_COMMITTED_SNAPSHOT ON` removes reader/writer blocking at the cost of version store space. Needs exclusive access:
  `ALTER DATABASE x SET READ_COMMITTED_SNAPSHOT ON WITH ROLLBACK IMMEDIATE;`. Test code that
  relies on blocking for correctness (queue tables, check-then-insert).
- `AUTO_UPDATE_STATISTICS_ASYNC ON`: queries do not wait for statistics updates; helps OLTP on large tables.
- Compatibility level controls optimizer behaviour; raise it with Query Store capturing and a rollback plan.

## Enforce
dbachecks `Invoke-DbcCheck -Check AutoShrink, AutoClose, PageVerify`, or a Policy-Based
Management policy on the Database facet. Set `model` correctly so new databases inherit the defaults.

## Verify
Re-run the audit query: no database has auto shrink or auto close on; all show `CHECKSUM`.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: sys.databases reference for SQL Server 2025 (every column in the audit query exists: is_auto_shrink_on, is_auto_close_on, page_verify_option_desc, is_read_committed_snapshot_on, snapshot_isolation_state_desc, is_auto_create_stats_on, is_auto_update_stats_on, is_auto_update_stats_async_on, compatibility_level, recovery_model_desc, target_recovery_time_in_seconds), ALTER DATABASE SET options (CHECKSUM default, model sets defaults, termination clauses, AUTO_CLOSE not in Azure SQL Database, TARGET_RECOVERY_TIME), model database page (AUTO_SHRINK and AUTO_CLOSE OFF by default; TARGET_RECOVERY_TIME 60 s default since 2016), DBCC SHRINKFILE (WAIT_AT_LOW_PRIORITY with ABORT_AFTER_WAIT = SELF or BLOCKERS from SQL Server 2022, data files only), Shrink a File page (shrink fragments indexes; rebuild afterwards), dbachecks (AutoShrink, AutoClose and PageVerify check tags). Removed as unconfirmed: the Express AUTO_CLOSE default (documented only for old releases) and the tempdb-specific version store wording.
Method: documentation only; no commands were run.
