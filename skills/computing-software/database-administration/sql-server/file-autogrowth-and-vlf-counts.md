---
id: computing-software.database-administration.sql-server.file-autogrowth-and-vlf-counts
name: file-autogrowth-and-vlf-counts
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, sql-server-configuration, vlf-count, log-autogrowth, autogrowth, transaction-log, dm-db-log-info]
level: practitioner
status: docs-checked
description: "Set SQL Server data and log file sizes and autogrowth in fixed MB, check VLF counts with sys.dm_db_log_info, and fix a log with thousands of VLFs."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-log-architecture-and-management-guide
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-db-log-info-transact-sql
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-file-and-filegroup-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File autogrowth and VLF counts

## Autogrowth settings
Percentage growth (old default 10%) makes each growth bigger and slower; tiny fixed growth
(1 MB) causes thousands of growth events and log fragmentation. Pre-size files for expected
data and set fixed-MB growth as a safety net:
```sql
ALTER DATABASE Sales MODIFY FILE (NAME = Sales_data, SIZE = 200GB, FILEGROWTH = 4GB);
ALTER DATABASE Sales MODIFY FILE (NAME = Sales_log,  SIZE = 32GB,  FILEGROWTH = 8GB);
```
- Data file growth is instant only with **Instant File Initialization** (service account or SID has
  "Perform volume maintenance tasks"). **Log** growth is zero-initialized, except growths up to 64 MB on SQL Server 2022+
  (default growth for new databases is 64 MB), so huge log growths stall the database while zeroing.
- Slow growth is logged as errors 5144/5145 and shows `PREEMPTIVE_OS_WRITEFILEGATHER` waits.

## Virtual log files (VLFs)
The log is divided internally into VLFs; each growth adds VLFs. Documented rule: from SQL Server 2014, growth less than 1/8 of
the current log size adds 1 VLF; otherwise growth under 64 MB adds 4 VLFs (1 VLF up to 64 MB on 2022+ and Azure SQL),
64 MB to 1 GB adds 8, over 1 GB adds 16. Many VLFs slow **database startup/recovery, log backup and restore, and cause
transactional replication/CDC and Always On redo latency**. You cannot set VLF size or count directly.
`sys.dm_db_log_info` needs SQL Server 2016 SP2 or later (VIEW SERVER STATE; 2022+: VIEW DATABASE PERFORMANCE STATE).
```sql
SELECT DB_NAME(d.database_id) AS db, COUNT(*) AS vlfs,
       SUM(CASE WHEN li.vlf_active = 1 THEN 1 ELSE 0 END) AS active
FROM sys.databases d CROSS APPLY sys.dm_db_log_info(d.database_id) li
GROUP BY d.database_id ORDER BY vlfs DESC;
```
Microsoft says to keep the total "a maximum of several thousand"; symptoms become severe in the hundreds of thousands (error 9017 warns on restore).

## Fixing a fragmented log
1. Make the log reusable: take a log backup (FULL/BULK_LOGGED) or checkpoint (SIMPLE).
2. Shrink the log, then grow it manually to the required size (Microsoft's fix grows it in one step; the stepwise growth below is a common variation):
   ```sql
   USE Sales;
   DBCC SHRINKFILE (Sales_log, 1024);           -- may need a second log backup + shrink
   ALTER DATABASE Sales MODIFY FILE (NAME = Sales_log, SIZE = 16GB);
   ALTER DATABASE Sales MODIFY FILE (NAME = Sales_log, SIZE = 32GB);
   ```
   Take a restorable backup first. Microsoft also points to its Fixing-VLFs script (tigertoolbox) for sizing.
3. Set fixed FILEGROWTH so it does not recur.
Do this in a quiet period; the shrink fails to go below active VLFs.

## Gotchas
- Never schedule routine `SHRINKFILE` on data files: it fragments indexes and the file grows back.
- Under FULL/BULK_LOGGED the log is truncated after a log backup (once a checkpoint has occurred), so a missing log backup
  is the classic runaway log; under SIMPLE it truncates at checkpoint, and a long-running transaction can still hold it.

## Verify
`sys.dm_db_log_info` count drops to a few hundred or less; `sys.database_files` shows
`is_percent_growth = 0` and the intended `growth` (8-KB pages when not percent).

## Checked
Date 2026-10-23. Documentation release: SQL Server 2025 Transaction Log Architecture and Management Guide, Database Instant File Initialization, sys.dm_db_log_info and sys.database_files pages (2017-2025).
Confirmed: VLF-per-growth rule including the 2022 change, effects of many VLFs, shrink-then-regrow fix and several-thousand guidance, log IFI up to 64 MB on 2022+, errors 5144/5145, `sys.dm_db_log_info` columns and 2016 SP2 gate, `sys.database_files` growth units, log truncation rules. Removed the unconfirmed default-trace event ids, XE event name and the AG disk-size and 8-16 GB step claims. Removed the `log_reuse_wait_desc` check because its values were not confirmed.
Method: documentation only; no commands were run.
