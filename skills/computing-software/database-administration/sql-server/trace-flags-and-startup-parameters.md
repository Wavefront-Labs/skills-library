---
id: computing-software.database-administration.sql-server.trace-flags-and-startup-parameters
name: trace-flags-and-startup-parameters
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, trace-flags, startup-parameters, dbcc-traceon, minimal-configuration, single-user-mode]
level: advanced
status: docs-checked
description: "Enable SQL Server trace flags globally or at startup, edit startup parameters (-T, -m, -f, -e), and know which flags still matter on current versions."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-traceon-trace-flags-transact-sql
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/database-engine-service-startup-options
  - https://learn.microsoft.com/en-us/sql/linux/configure/mssql-conf
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-objects/sys-dm-server-registry-transact-sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trace flags and startup parameters

## Session vs global vs startup
```sql
DBCC TRACEON (3226);        -- session scope (flags documented as global-only need -1)
DBCC TRACEON (3226, -1);    -- global, lost at restart
DBCC TRACESTATUS (-1);      -- what is on globally
DBCC TRACEOFF (3226, -1);
```
A flag you depend on must be a **startup parameter**, or it silently disappears after the next
patch reboot. Configuration Manager -> SQL Server service -> Properties -> Startup Parameters ->
add `-T3226` (uppercase T, no space; a lowercase t sets other internal flags meant for support engineers). On Linux:
`sudo /opt/mssql/bin/mssql-conf traceflag 3226 on` (applies at service startup, so restart).

## Flags worth knowing (descriptions per the current trace-flag page)
| Flag | Effect |
|---|---|
| 3226 | suppress the success entries every backup/restore writes to the error log and event log (global only) |
| 1222 | deadlock participants and resources as XML in the error log (global only) |
| 7745 | Query Store does not flush to disk at shutdown (data not yet flushed can be lost) |
| 7752 | async Query Store load; no effect from SQL Server 2019, where the engine controls it |
| 460 | message 2628 instead of 8152 for truncation (2016 SP2 CU6, 2017 CU12+); the default from compat level 150, no effect there |
| 2371 | linear auto-update-statistics threshold; engine-controlled from 2016 at compat 130+, no effect |
| 1117, 1118 | no effect from 2016: use `AUTOGROW_SINGLE_FILE`/`AUTOGROW_ALL_FILES` and `MIXED_PAGE_ALLOCATION` database options |
| 4199 | enables post-RTM optimizer fixes (global, session or query); with it off, optimizer changes are tied to the compat level (130+). Database equivalent: `QUERY_OPTIMIZER_HOTFIXES` scoped config |
| 845 | locked pages on Standard; on by default since 2012, must not be used |
| 834 | large pages; startup only; Microsoft advises against it without thorough testing |
| 8048 | NUMA-partitioned to CPU-partitioned memory objects; dynamic since 2014 SP2/2016 |
| 2528 | disables parallel DBCC CHECKDB/CHECKFILEGROUP/CHECKTABLE |
| 1224 | disables lock escalation by lock count (memory pressure can still escalate) |

Query level: `OPTION (QUERYTRACEON n)` works only for the optimizer flags the page documents.

## Startup parameters for emergencies
| Param | Use |
|---|---|
| `-m` / `-mSQLCMD` | single-user mode (no checkpoint process), optionally only for one client application name (case sensitive; not a security feature) |
| `-f` | minimal configuration (for example a value that prevents startup); implies single-user mode |
| `-e` / `-l` / `-d` | error log / master log / master data file paths |
| `-T<n>` | trace flag at startup |

With `net start` the options use a slash: `net start MSSQLSERVER /mSQLCMD`, then `sqlcmd -S . -E`. For the SSMS query editor
use `-m"Microsoft SQL Server Management Studio - Query"` (command line only, quotes needed there, not in Configuration Manager).
Locked out of sysadmin: start with `-m`; any member of the local Administrators group can then connect as sysadmin; then
`CREATE LOGIN [DOMAIN\me] FROM WINDOWS; ALTER SERVER ROLE sysadmin ADD MEMBER [DOMAIN\me];`
and restart normally.

## Gotchas
- In `-m` mode an unknown client application can take the only connection; restrict it with `-m<ApplicationName>`.
- Improper startup options can prevent SQL Server starting; Configuration Manager stores them in the registry.
- Test flags before use (834 especially); set startup parameters on every instance you run, including each FCI/AG node (per-instance setting).

## Verify
After restart, `DBCC TRACESTATUS(-1)` lists the flag, and
`SELECT registry_key, value_name, value_data FROM sys.dm_server_registry WHERE registry_key LIKE N'%Parameters';`
shows the startup arguments (the DMV's own documented example).

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 trace-flag page (first 100,000 characters read), Database Engine Service Startup Options, mssql-conf and sys.dm_server_registry pages.
Confirmed: flag descriptions and their 2016/2019/2012/2014 SP2 status, 460 compat-150 default, uppercase `-T` rule, `-m`, `-f`, `-d/-e/-l`, `-mClient` and `net start` slash form, local administrators as sysadmin in single-user mode, Linux `mssql-conf traceflag`, DMV example. Removed unconfirmed claims: QUERYTRACEON needing sysadmin, USE HINT alternative, system_health deadlock remark, flags 834/8048 being undocumented (they are documented), SQLArg filter.
The DBCC TRACEON page has a further 25,000 characters that were not read; no claim here depends on them.
Method: documentation only; no commands were run.
