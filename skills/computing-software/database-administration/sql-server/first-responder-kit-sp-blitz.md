---
id: computing-software.database-administration.sql-server.first-responder-kit-sp-blitz
name: first-responder-kit-sp-blitz
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sp-blitz, first-responder-kit, sp-blitzfirst, sp-blitzcache, sp-blitzindex, health-check, triage]
level: practitioner
status: docs-checked
description: "Use the First Responder Kit (sp_Blitz, sp_BlitzFirst, sp_BlitzCache, sp_BlitzIndex) for health checks, live triage, and finding the worst queries and indexes."
sources:
  - https://github.com/BrentOzarULTD/SQL-Server-First-Responder-Kit
  - https://www.brentozar.com/first-aid/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# First Responder Kit (sp_Blitz family)

Free procedures. Install into `master` (or a DBA database) from the repo's
`Install-All-Scripts.sql`, or `Install-DbaFirstResponderKit -SqlInstance sql01 -Database master` (dbatools).
Keep them updated.

## Which one when
| Situation | Run |
|---|---|
| Inherited server / annual health check | `EXEC sp_Blitz @CheckServerInfo = 1;` |
| "It is slow right now" | `EXEC sp_BlitzFirst @Seconds = 30, @ExpertMode = 1;` |
| Which queries cost the most | `EXEC sp_BlitzCache @SortOrder = 'cpu', @Top = 20;` |
| Index problems in a database | `EXEC sp_BlitzIndex @DatabaseName = 'appdb', @Mode = 0;` |
| Deadlocks lately | `EXEC sp_BlitzLock @StartDate = '2026-10-17';` |
| Who is running what | `EXEC sp_BlitzWho;` |

## sp_Blitz
Results are sorted by `Priority` (lower number = more urgent;
`@CheckServerInfo = 1` adds rows at priority 250). Work top-down; each row has a URL explaining the fix.
`@OutputDatabaseName/@OutputSchemaName/@OutputTableName` stores results for trending.
Suppress known-acceptable findings with a skip table (`@SkipChecksDatabase`, `@SkipChecksTable`).

## sp_BlitzFirst
Samples performance data over `@Seconds` and reports what happened in that window; `@ExpertMode = 1` adds more columns.
Scheduled every 15 minutes with `@OutputDatabaseName`
it builds a history (the "Blitz tables") for later comparison.

## sp_BlitzCache
`@SortOrder` picks the metric (for example `'cpu'`, `'reads'`; average variants such as `'avg reads'` exist); see the sp_BlitzCache section of the README for the full list.
It reads the plan cache, so it misses queries already evicted; Query Store fills that gap.

## sp_BlitzIndex
`@Mode = 0` (default) returns high-priority advice on the most urgent index issues; `@Mode = 2` inventories existing indexes and their usage; `@Mode = 4` returns more advice (priorities 1-255); `@TableName = 'Orders'` (with `@SchemaName`) analyses one table. Index usage stats reset at restart, so check `sqlserver_start_time` (in `sys.dm_os_sys_info`) before dropping "unused" indexes.

## Gotchas
- Checks inside user databases can be slow on servers with many databases; `@CheckUserDatabaseObjects = 0` skips them (`@BringThePain = 1` is required to run them with over 50 databases).
- Findings are prompts to investigate, not orders; validate before changing production.

## Checked

2026-10-28. Confirmed in the First Responder Kit README: Install-All-Scripts.sql, @CheckServerInfo (priority 250 rows), @SkipChecksDatabase/@SkipChecksTable, @OutputDatabaseName/@OutputSchemaName/@OutputTableName, scheduling sp_BlitzFirst every 15 minutes with output tables, @ExpertMode, @CheckUserDatabaseObjects and @BringThePain (over 50 databases), sp_BlitzIndex @Mode 0/2/4 and @TableName, sp_BlitzLock @StartDate, sp_BlitzWho, the sqlserver_start_time source. Removed: MIT licence claim, monthly check cadence, priority band meanings, @SinceStartup, 'avg cpu' sort value, warning list, RECOMPILE claim, older-version rebuild claim, thousands-of-databases claim.

Method: documentation only; no commands were run.

## Verify
Procedures installed at the current release on every instance and sp_Blitz output reviewed, with the most urgent priorities ticketed.
