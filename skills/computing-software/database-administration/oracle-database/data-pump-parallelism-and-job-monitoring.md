---
id: computing-software.database-administration.oracle-database.data-pump-parallelism-and-job-monitoring
name: data-pump-parallelism-and-job-monitoring
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, data-pump, data-pump-parallel, data-pump-attach, expdp, impdp, dba-datapump-jobs]
level: practitioner
status: docs-checked
description: "Speed up Oracle Data Pump with PARALLEL and %U dump files, monitor and control running jobs with ATTACH, and clean up orphaned job master tables."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-data-pump-export-utility.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-data-pump-performance-tips.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data Pump parallelism and job monitoring

## Parallel export/import
```bash
expdp system@salespdb SCHEMAS=app DIRECTORY=dp_dir \
  DUMPFILE=app_%U.dmp FILESIZE=20G PARALLEL=8 \
  LOGFILE=app_exp.log METRICS=YES LOGTIME=ALL \
  COMPRESSION=ALL JOB_NAME=APP_EXP
impdp system@newpdb DIRECTORY=dp_dir DUMPFILE=app_%U.dmp PARALLEL=8 \
  LOGFILE=app_imp.log METRICS=YES LOGTIME=ALL JOB_NAME=APP_IMP \
  TRANSFORM=DISABLE_ARCHIVE_LOGGING:Y
```
- Supply at least one dump file per degree of parallelism (`%U` expands to 01-99); with too few files some workers sit idle or the job stops with ORA-39095.
- For maximum throughput do not set `PARALLEL` much above twice the number of CPUs. `PARALLEL` is valid only in Enterprise Edition. Gains apply when you have large quantities of data versus metadata: the Performance Tips page says metadata extraction and object creation perform about the same as original export/import.
- `COMPRESSION=ALL` needs the Advanced Compression option; `METADATA_ONLY` (the default) does not.
- `TRANSFORM=DISABLE_ARCHIVE_LOGGING:Y` reduces redo for TABLE and INDEX on import; it does nothing if the database is in FORCE LOGGING mode (e.g. with Data Guard).
- `EXCLUDE=STATISTICS` (export or import) then gathering stats with `DBMS_STATS` avoids importing statistics; Oracle suggests it mainly for dump files made before 12.1 that hold large statistics data.
- Data Pump uses parallelism to build indexes and load package bodies.

## Monitor
```sql
SELECT owner_name, job_name, operation, job_mode, state, degree, attached_sessions
FROM dba_datapump_jobs;
SELECT sid, opname, target_desc, sofar, totalwork, ROUND(sofar/totalwork*100,1) pct
FROM v$session_longops WHERE totalwork > 0 AND sofar < totalwork;
```

## Interactive control (ATTACH)
```bash
expdp system@salespdb ATTACH=APP_EXP
Export> STATUS              # per-worker progress
Export> PARALLEL=12         # increase takes effect immediately if files/resources allow; decrease after current tasks
Export> STOP_JOB=IMMEDIATE  # no data loss; some tasks redone at restart; restartable
Export> START_JOB           # resume after STOP_JOB or an unexpected failure (dump files + control table intact)
Export> KILL_JOB            # deletes the control table and dump files; cannot be restarted
```

## Orphaned jobs
`DBA_DATAPUMP_JOBS` also lists Data Pump control job tables that are not associated with an active job. If you will not restart such a job, attach to it and use `KILL_JOB` (it removes the control table and dump files). The manual's cleanup steps for orphaned tables beyond that are not in the pages checked.

## Gotchas
- `ORA-39095: Dump file space has been exhausted`: the FILESIZE limit was hit; attach and add files with `ADD_FILE`, then restart.
- Streams pool: Oracle recommends a minimum `STREAMS_POOL_SIZE` of 10 MB for Data Pump; it is set automatically if `SGA_TARGET` is set, otherwise it defaults to 10% of the shared pool, taken from the buffer cache, and a minimal SGA configuration can make Data Pump fail.

## Verify
Log shows all workers active (`METRICS=YES` timings per object type), job completes with
`successfully completed`, and object counts match between source and target.

## Checked
Date 2026-10-22. Oracle Database 19c Utilities (Data Pump Export, Import, Performance Tips) and Database Reference
(DBA_DATAPUMP_JOBS, V$SESSION_LONGOPS). Confirmed: PARALLEL ceiling of about twice CPU and file-per-degree rule, Enterprise
Edition requirement, COMPRESSION=ALL licence, DISABLE_ARCHIVE_LOGGING scope and FORCE LOGGING caveat, EXCLUDE=STATISTICS note,
interactive commands (STATUS, PARALLEL, STOP_JOB=IMMEDIATE, START_JOB, KILL_JOB), ORA-39095 and ADD_FILE, STREAMS_POOL_SIZE
guidance, DBA_DATAPUMP_JOBS and V$SESSION_LONGOPS columns. Corrected: the "parallel metadata from 12.2" claim (the Performance
Tips page says metadata performance is about the same as original export/import), KILL_JOB also deletes dump files, the
256M streams pool example. Removed (not found): CLUSTER=N, CONTINUE_CLIENT, Ctrl+C note, DROP TABLE cleanup of the master
table, ORA-04031 advice, "parallelizes across objects" claim.
Method: documentation only; no commands were run.
