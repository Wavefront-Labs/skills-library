---
id: computing-software.database-administration.sql-server.instant-file-initialization-and-lock-pages-in-memory
name: instant-file-initialization-and-lock-pages-in-memory
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, instant-file-initialization, ifi, lock-pages-in-memory, lpim, perform-volume-maintenance-tasks, sql-server-configuration, autogrowth, working-set-trim]
level: practitioner
status: docs-checked
description: "Grant SQL Server instant file initialization and lock pages in memory, verify they are active, and know when each is safe or pointless."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/databases/database-instant-file-initialization
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/enable-the-lock-pages-in-memory-option-windows
  - https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/server-memory-server-configuration-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instant file initialization and lock pages in memory

Two Windows user rights granted to the SQL Server service account (or its virtual
account `NT SERVICE\MSSQLSERVER`). Both need a service restart to take effect.

## Instant file initialization (IFI)
Without IFI, every data file create/grow/restore writes zeros over the new space:
a 200 GB restore spends minutes zeroing before copying data; an autogrowth stalls
every query touching the file.

Grant: `secpol.msc` -> Local Policies -> User Rights Assignment ->
**Perform volume maintenance tasks** -> add the service SID (Microsoft recommends the service SID so the grant survives a service-account change). Setup can grant it from SQL Server 2016
(`/SQLSVCINSTANTFILEINIT` on the command line, or the wizard checkbox). Then restart the service; the error log at startup says
`Database Instant File Initialization: enabled` or `disabled`.

Check:
```sql
SELECT servicename, instant_file_initialization_enabled FROM sys.dm_server_services;
```
Scope and limits:
- Data files get IFI with the privilege. Log files are zeroed on older versions; from SQL Server 2022 (all editions)
  log autogrowth events up to 64 MB use IFI (no privilege needed for that), larger log growths are still zeroed.
  The default autogrowth increment for new databases is 64 MB.
- TDE prevents IFI for data files; on 2022+ it still allows IFI for log growth.
- Security trade-off: deleted disk content stays on the new region until overwritten, and a SQL Server
  administrator could read raw page contents; detached data files and backups need restrictive ACLs.
  Microsoft still recommends enabling IFI. Disable it by revoking the privilege (only affects later growth).
- Slow zeroing shows as errors 5144/5145 in the error log and `PREEMPTIVE_OS_WRITEFILEGATHER` waits.

## Lock pages in memory (LPIM)
Lets SQL Server use the Windows AWE APIs ("locked pages") so Windows cannot page its memory out. Use it
when the error log shows 17890 ("A significant part of sql server process memory has been paged out").

Grant: `gpedit.msc`/local policy -> User Rights Assignment -> **Lock pages in memory** -> add the service account or
service SID; SQL Server Configuration Manager can also do it in 2019+. Restart the instance. It is honoured in Standard edition and
higher; trace flag 845 is not needed for Standard since SQL Server 2012.

Check:
```sql
SELECT sql_memory_model_desc FROM sys.dm_os_sys_info;   -- 2016 SP1+: CONVENTIONAL = not granted, LOCK_PAGES = granted,
                                                        -- LARGE_PAGES = granted plus trace flag 834 (advanced, not recommended for most)
```
Rules:
- **Set `max server memory` to a specific value first.** Microsoft strongly recommends this with LPIM; a cap that ignores other
  memory consumers can cause instability. LPIM does not change dynamic memory management.
- In virtual environments Microsoft says `min server memory` is essential; coordinate memory reservations with the hypervisor team.
- This page is for Windows; for Linux see `memory.memorylimitmb` in mssql-conf.

## Verify
- [ ] `instant_file_initialization_enabled` shows enabled for the engine service (and the error log agrees).
- [ ] `sql_memory_model_desc = LOCK_PAGES` where intended, with max server memory set.
- [ ] A test 10 GB data file grow completes in seconds.

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 pages for Database Instant File Initialization, Enable Lock Pages in Memory, and Server Memory Configuration Options (2017-2025).
Confirmed: privilege name and grant steps, setup switch, 2022 log IFI up to 64 MB and TDE behaviour, security trade-off, errors 5144/5145, LPIM Standard edition and TF 845, error 17890, `sql_memory_model_desc` values and TF 834, max-server-memory requirement. Removed unconfirmed balloon-driver and Azure SQL Database statements and the `DBCC PAGE` claim.
Method: documentation only; no commands were run.
