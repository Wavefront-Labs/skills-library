---
id: computing-software.database-administration.sql-server.backup-throughput-tuning
name: backup-throughput-tuning
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, buffercount, backup-striping, maxtransfersize, blocksize, backup-performance, trace-flag-3213]
level: advanced
status: docs-checked
description: "Speed up SQL Server backups and restores by striping to multiple files and tuning BUFFERCOUNT, MAXTRANSFERSIZE and BLOCKSIZE, measuring where the bottleneck is."
sources:
  - https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-transact-sql
  - https://ola.hallengren.com/sql-server-backup.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/databases/database-instant-file-initialization
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Backup throughput tuning

A backup is a pipeline: read data files -> buffers -> write backup devices. It runs at the speed
of the slowest stage. Measure, change one thing, measure again.

## Baseline
```sql
SELECT database_name, backup_start_date,
  DATEDIFF(second, backup_start_date, backup_finish_date) AS secs,
  backup_size/1048576.0 / NULLIF(DATEDIFF(second, backup_start_date, backup_finish_date),0) AS mb_per_sec
FROM msdb.dbo.backupset WHERE type = 'D' ORDER BY backup_start_date DESC;
```
Defaults to know (BACKUP statement page): MAXTRANSFERSIZE is 1 MB for disk backups of non-TDE databases and 64 KB for a TDE database with a single data file, VDI or tape; a database with several data files uses more than 64 KB.

## Knobs
```sql
BACKUP DATABASE bigdb
TO DISK = '<BACKUP_DIR1>/bigdb_1.bak', DISK = '<BACKUP_DIR2>/bigdb_2.bak',
   DISK = '<BACKUP_DIR1>/bigdb_3.bak', DISK = '<BACKUP_DIR2>/bigdb_4.bak'
WITH COMPRESSION, CHECKSUM, BUFFERCOUNT = 64, MAXTRANSFERSIZE = 4194304, STATS = 5;
```
| Knob | Effect |
|---|---|
| Multiple files (striping) | up to 64 devices; helps when a single file/target is the limit. The stripe count must stay the same for the media set, and restores need **all** stripes |
| `BUFFERCOUNT` | more buffers in flight can cut backup time. Memory used = BUFFERCOUNT x MAXTRANSFERSIZE (64 x 4 MB = 256 MB); too high risks out-of-memory errors |
| `MAXTRANSFERSIZE` | multiples of 64 KB up to 4 MB (10 MB is used for S3-compatible URL backups) |
| `BLOCKSIZE` | 512 to 65536 bytes; usually unnecessary because BACKUP picks it; matters mainly for tape (default 65536 for tape, 512 otherwise) |
| `COMPRESSION` | trades CPU for less write IO; usually a big win |

## Find the bottleneck
- Write-bound: backup target latency high in perfmon (`Avg. Disk sec/Write`), network saturated to the share.
- Read-bound: data volume read latency high; test with `BACKUP ... TO DISK = 'NUL'` (testing only, never production: it discards the output but still marks pages as backed up, so use `COPY_ONLY` to leave differential bases untouched).
- CPU-bound: compression maxes out cores; try another algorithm (ZSTD in SQL Server 2025, hardware QAT offload) or less compression.
Waits during backup include `BACKUPIO` and `ASYNC_IO_COMPLETION` (the latter commonly means waiting on the backup target).

## Restores
Same options apply to `RESTORE`. Instant file initialization removes the zeroing of data files
(log files are still zeroed, apart from small log autogrowth in SQL Server 2022) before restore starts, often the largest gain for big restores.

## Gotchas
- A backup can stripe to at most 64 devices; check the per-blob size limits in the backup-to-URL article before striping to URLs.
- Huge BUFFERCOUNT x MAXTRANSFERSIZE on a memory-constrained server can cause out-of-memory errors during backup.
- Ola Hallengren exposes `@NumberOfFiles`, `@BufferCount`, `@MaxTransferSize`.

## Verify
Throughput (MB/s) up versus the baseline, and a timed restore meets the RTO.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: BACKUP statement page for SQL Server 2025 (up to 64 devices, stripe count fixed per media set, BUFFERCOUNT x MAXTRANSFERSIZE memory formula and OOM warning, MAXTRANSFERSIZE 64 KB multiples to 4 MB and defaults incl. TDE and S3 10 MB, BLOCKSIZE values and defaults, NUL device testing only and still marks pages as backed up, COPY_ONLY semantics, ZSTD in 2025, QAT), Learn I/O troubleshooting guide (BACKUPIO, ASYNC_IO_COMPLETION), instant file initialization page (data files only), Ola Hallengren DatabaseBackup parameters (@NumberOfFiles, @BufferCount, @MaxTransferSize). Removed as unconfirmed: trace flags 3213/3605, per-device writer thread and per-volume reader thread claims, BACKUPBUFFER wait, the 200 GB per-URL figure and the 4 MB-suits-most advice.
Method: documentation only; no commands were run.
