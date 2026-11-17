---
id: computing-software.database-administration.sql-server.reading-and-cycling-the-error-log
name: reading-and-cycling-the-error-log
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-error-log, xp-readerrorlog, sp-cycle-errorlog, agent-error-log, error-18456, monitoring]
level: practitioner
status: docs-checked
description: "Search the SQL Server and Agent error logs with xp_readerrorlog, cycle them on a schedule, raise the retained file count, and know which messages matter."
sources:
  - https://learn.microsoft.com/en-us/sql/tools/configuration-manager/viewing-the-sql-server-error-log
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-cycle-errorlog-transact-sql
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/scm-services-configure-sql-server-error-logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading and cycling the SQL Server error log

## Where it is
`SELECT SERVERPROPERTY('ErrorLogFileName');` Files `ERRORLOG`, `ERRORLOG.1` ... `.6` by default (SQL Server keeps the previous six logs; the current log has no extension). Default Windows folder is `MSSQL\LOG` under the instance folder; on Linux `/var/opt/mssql/log`.
If the instance will not start, open the file in a text editor: the last lines say why.

## Search
```sql
-- xp_readerrorlog <file#>, <1=SQL 2=Agent>, <search1>, <search2>, <start>, <end>, <'asc'|'desc'>
EXEC xp_readerrorlog 0, 1, N'Login failed', NULL, NULL, NULL, N'desc';
EXEC xp_readerrorlog 0, 1, N'error', N'severity: 2', '2026-10-17', '2026-10-18';
EXEC xp_readerrorlog 0, 2;   -- current Agent log
```
dbatools across many servers: `Get-DbaErrorLog -SqlInstance sql01,sql02 -After (Get-Date).AddDays(-1) | Where-Object Text -match 'error'`.

## Messages to know
Look up each error number in the SQL Server errors documentation before acting. Typical entries to alert on: failed logins (18456), I/O stalls, corruption errors (823, 824, 825), log or filegroup full, memory pressure, availability group state changes.

## Cycle and retain
A new log is created at each restart; `sp_cycle_errorlog` (sysadmin only) cycles the numbering without a restart, so a long-running instance does not keep one huge log. Cycle daily or weekly:
```sql
EXEC sp_cycle_errorlog;             -- SQL Server log
EXEC msdb.dbo.sp_cycle_agent_errorlog;
```
Schedule in an Agent job at midnight. Keep more files so cycling does not lose history: in Object Explorer, Management, right-click SQL Server Logs, Configure, then set the maximum number of error log files (default 6, not counting the current one) and optionally a maximum size per file in KB (0 = unlimited). dbatools: `Set-DbaErrorLogConfig -LogCount 30 -LogSize 102400`.

## Reduce noise
Failed login auditing level (server properties -> Security) controls 18456 volume; keep failed logins on.

## Gotchas
- `xp_readerrorlog` is an undocumented procedure; its argument order can change between versions.
- On Linux the logs are under `/var/opt/mssql/log`; the cycle procedures are the same.

## Checked
2026-11-01. Confirmed on Learn: View the SQL Server error log (previous six logs, Windows and Linux locations, current log has no extension), sp_cycle_errorlog (cycles without restart, sysadmin only), Configure SQL Server error logs (default 6, size in KB, 0 unlimited). Removed: error-number table, trace flag 3226, registry write, 99-file maximum, xp_readerrorlog wildcard claim (unconfirmed).
Method: documentation only; no commands were run.

## Verify
Cycle job scheduled, maximum error log files raised to 30 or more, and an alert or daily report on severity >= 17 entries.
