---
id: computing-software.database-administration.sql-server.file-io-latency-virtual-file-stats
name: file-io-latency-virtual-file-stats
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, dmv, wait-stats, virtual-file-stats, io-latency, pageiolatch, writelog, storage]
level: practitioner
status: docs-checked
description: "Measure SQL Server read/write latency per database file with sys.dm_io_virtual_file_stats deltas, and relate it to PAGEIOLATCH and WRITELOG waits."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/sys-dm-io-virtual-file-stats-transact-sql
  - https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/performance/troubleshoot-sql-io-performance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File I/O latency (sys.dm_io_virtual_file_stats)

The DMV holds cumulative counters since instance start per file: reads, writes, bytes, and
**stall** time (ms waited on I/O). Average latency = stall / count. Cumulative averages hide
spikes, so take two samples.

## Delta query
```sql
SELECT database_id, file_id, num_of_reads, num_of_writes, io_stall_read_ms, io_stall_write_ms,
       num_of_bytes_read, num_of_bytes_written, GETDATE() AS t
INTO #s1 FROM sys.dm_io_virtual_file_stats(NULL, NULL);
WAITFOR DELAY '00:05:00';
SELECT DB_NAME(s2.database_id) AS db, mf.physical_name, mf.type_desc,
       (s2.num_of_reads - s1.num_of_reads) AS reads,
       (s2.num_of_writes - s1.num_of_writes) AS writes,
       CAST((s2.io_stall_read_ms - s1.io_stall_read_ms) * 1.0
            / NULLIF(s2.num_of_reads - s1.num_of_reads, 0) AS decimal(10,1)) AS avg_read_ms,
       CAST((s2.io_stall_write_ms - s1.io_stall_write_ms) * 1.0
            / NULLIF(s2.num_of_writes - s1.num_of_writes, 0) AS decimal(10,1)) AS avg_write_ms
FROM sys.dm_io_virtual_file_stats(NULL, NULL) s2
JOIN #s1 s1 ON s1.database_id = s2.database_id AND s1.file_id = s2.file_id
JOIN sys.master_files mf ON mf.database_id = s2.database_id AND mf.file_id = s2.file_id
ORDER BY avg_read_ms DESC;
```

## Reading the numbers
Microsoft's I/O troubleshooting guide says `PAGEIOLATCH_*`, `WRITELOG` and `ASYNC_IO_COMPLETION` waits should generally stay below 10-15 ms per I/O request;
consistently above that is an I/O performance problem to investigate. Low counts make averages meaningless; ignore files with a handful of I/Os.

## Correlate with waits
- `PAGEIOLATCH_SH/EX` high (reads of pages from disk) + high data read latency -> slow storage **or** SQL Server issuing more I/O than the system can handle
  (check Buffer Manager Page Reads/sec, missing indexes, scans in plans).
- `WRITELOG` high + high log write latency -> log storage, the most common cause per Microsoft; also check data and log files sharing a volume and too many VLFs.
- High latency but low waits -> background work (backups, CHECKDB) during the sample.

## Next steps
- Compare with OS counters (`Avg. Disk sec/Read` and `Avg. Disk sec/Write` in Performance Monitor) to see if
  the delay is below SQL Server (storage, HBA, VM host).
- Keep data and log files on separate volumes.

## Verify
Repeat the delta during peak and off-peak; after a storage or query fix, `avg_read_ms` /
`avg_write_ms` and the matching wait types drop.

## Checked
2026-10-31. Confirmed against the Learn pages for `sys.dm_io_virtual_file_stats` and troubleshooting slow SQL Server I/O: columns `num_of_reads`, `num_of_writes`, `io_stall_read_ms`, `io_stall_write_ms`, counters reset at service start, PAGEIOLATCH_SH/EX and WRITELOG meaning and causes, the 10-15 ms guidance, Performance Monitor `Avg. Disk sec/Read`.
Removed as unconfirmed: the per-file latency threshold table, the 2 ms log figure, `iostat -x`, `sys.dm_io_pending_io_requests`, and the Azure VM disk caching advice.
Method: documentation only; no commands were run.
