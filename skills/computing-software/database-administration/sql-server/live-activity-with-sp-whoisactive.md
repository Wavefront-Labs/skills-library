---
id: computing-software.database-administration.sql-server.live-activity-with-sp-whoisactive
name: live-activity-with-sp-whoisactive
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sp-whoisactive, live-activity, blocking, tempdb, wait-stats, activity-logging, adam-machanic]
level: practitioner
status: docs-checked
description: "Use sp_WhoIsActive to see what SQL Server is running right now, with plans, blockers, tempdb and deltas, and log its output to a table."
sources:
  - https://github.com/amachanic/sp_whoisactive
  - https://github.com/amachanic/sp_whoisactive/blob/master/sp_WhoIsActive.sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live activity with sp_WhoIsActive

**Goal:** a one-call answer to "what is running and why is it slow". A comprehensive activity-monitoring stored procedure, GPLv3, versioned on GitHub, for SQL Server 2005 through 2022 and Azure SQL DB.

## Install
Download `sp_WhoIsActive.sql` from the repo root, open it in SSMS and run it. It is created in the database of the current session; use `master` to make it callable from every database. For SQL Server 2012 to 2019 use the script in the `2019` folder; for 2008 or earlier use the `2008` folder.

## Everyday calls
```sql
EXEC sp_WhoIsActive;                                -- defaults
EXEC sp_WhoIsActive @get_plans = 1;                 -- plan for the request's statement offset (2 = entire plan)
EXEC sp_WhoIsActive @find_block_leaders = 1, @sort_order = '[blocked_session_count] DESC';
EXEC sp_WhoIsActive @get_locks = 1;                 -- locks per request, aggregated as XML
EXEC sp_WhoIsActive @get_outer_command = 1;         -- the outer ad hoc query or procedure call
EXEC sp_WhoIsActive @show_sleeping_spids = 2;       -- 0 none, 1 only with open tran (default), 2 all sleeping
EXEC sp_WhoIsActive @delta_interval = 5;            -- second pull after 5 s, adds *_delta columns
EXEC sp_WhoIsActive @get_task_info = 2;             -- all task metrics; block_info on lock waits needs @get_additional_info = 1
EXEC sp_WhoIsActive @filter_type = 'database', @filter = 'appdb';  -- types: session, program, database, login, host
```
Other parameters in the script: `@get_transaction_info`, `@get_avg_time`, `@get_memory_info`, `@not_filter`, `@output_column_list`, `@format_output`, `@help`. Useful sort/output columns include `blocking_session_id`, `blocked_session_count`, `tempdb_allocations`, `tempdb_current`, `open_tran_count`, `percent_complete`, `wait_info`, `host_name` and `program_name`.

## Log to a table
```sql
DECLARE @schema varchar(max);
EXEC sp_WhoIsActive @get_plans = 1, @find_block_leaders = 1,
     @return_schema = 1, @schema = @schema OUTPUT;
SET @schema = REPLACE(@schema, '<table_name>', 'dba.dbo.WhoIsActiveLog');
EXEC (@schema);
-- then, from a scheduled job:
EXEC sp_WhoIsActive @get_plans = 1, @find_block_leaders = 1,
     @destination_table = 'dba.dbo.WhoIsActiveLog';
```
`@return_schema = 1` returns a CREATE TABLE statement with a `<table_name>` placeholder instead of data. The script does not check that the destination table exists or has the right schema before inserting, so create it first. Pick your own schedule and retention.

## Gotchas
- It shows a moment in time.
- `@format_output` values 4 to 6 compress LOB columns with `COMPRESS()` (they become varbinary); use `DECOMPRESS()` plus a cast to read them.

## Verify
- [ ] Installed in a known database on every instance.
- [ ] The logging job inserts rows and old rows are removed by a job you wrote.

## Checked
2026-11-09. Read the repository README in full and the parameter header of `sp_WhoIsActive.sql` (lines 1050-1170 and the output-column list), confirming parameter names, values and defaults. Partial read: the procedure body was not read. Removed (not stated in the sources): the dbatools installer, the `VIEW SERVER STATE` grant, the wait_info example, performance-cost advice, and the transaction-age remark.
Method: documentation only; no commands were run.
