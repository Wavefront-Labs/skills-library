---
id: computing-software.database-administration.oracle-database.data-pump-export-and-import
name: data-pump-export-and-import
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, data-pump, expdp, impdp, directory-object, flashback-scn, parallel-export, schema-export, logical-backup]
level: practitioner
status: docs-checked
description: "Run Oracle Data Pump expdp/impdp correctly: directory objects, consistent exports with FLASHBACK_TIME, parallel dump files, filtering, and monitoring or attaching to jobs."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-data-pump-export-utility.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/datapump-import-utility.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data Pump export and import

**Goal:** a consistent logical copy of a schema, moved and imported fast.

## Directory object (server-side files)
```sql
CREATE OR REPLACE DIRECTORY dp_dir AS '/u01/exports';
GRANT READ, WRITE ON DIRECTORY dp_dir TO dp_user;
```
Directory privileges are independent of operating system permissions: the OS directory must also be accessible to the Oracle Database processes. The creator of a directory automatically has READ, WRITE and EXECUTE on it.

## Consistent parallel export
```bash
expdp dp_user@//dbhost/salespdb schemas=SALES directory=dp_dir \
  dumpfile=sales_%U.dmp filesize=20G parallel=8 \
  flashback_time=systimestamp logfile=sales_exp.log \
  compression=all metrics=yes logtime=all
```
- `flashback_time=systimestamp` starts a consistent export based on the current system time (Flashback Query only; `FLASHBACK_TIME` and `FLASHBACK_SCN` are mutually exclusive). With a time literal use `FLASHBACK_TIME="TO_TIMESTAMP('...','...')"` in a parameter file to avoid shell quoting.
- `PARALLEL` should be <= the number of dump files; `%U` (01-99) creates them so workers each get a file, otherwise the job can stop with ORA-39095.
- `FILESIZE` default 0 means 16 TB; minimum is 10 times the default block size.
- `compression=all` requires the Advanced Compression option; `metadata_only` is the default and doesn't.

## Import
```bash
impdp dp_user@//dbhost2/testpdb directory=dp_dir dumpfile=sales_%U.dmp parallel=8 \
  schemas=SALES table_exists_action=replace transform=disable_archive_logging:y \
  logfile=sales_imp.log
```
- `transform=disable_archive_logging:y` applies to TABLE and INDEX objects (both if none is named): logging is disabled during the load and restored afterwards. It does nothing if the database is in FORCE LOGGING mode (for example Data Guard). It does not apply to transportable tablespace imports.
- `table_exists_action` is SKIP (default; APPEND when `CONTENT=DATA_ONLY`), APPEND, TRUNCATE or REPLACE. SKIP and REPLACE are not valid with `CONTENT=DATA_ONLY`.
- `sqlfile=ddl.sql` writes the DDL impdp would run instead of executing it (not combinable with `CONTENT=ALL` or `DATA_ONLY`).
- Listing schemas other than your own needs the `DATAPUMP_IMP_FULL_DATABASE` role.

## Control running jobs
```bash
expdp dp_user attach=SYS_EXPORT_SCHEMA_01
Export> status                  # cumulative status; STATUS=300 refreshes every 5 min
Export> parallel=4              # increase takes effect immediately, decrease after current tasks
Export> stop_job=immediate      # no data loss; some tasks redone; restart with attach + start_job
```
```sql
SELECT owner_name, job_name, state, degree FROM dba_datapump_jobs;
```

## Gotchas
- `ORA-39095` (dump file space exhausted): attach to the stopped job, `ADD_FILE`, restart.
- Version: a dump file made with `VERSION=12` imports only into 12.1 or later; set `VERSION` on export to the oldest target release.
- `START_JOB` works only while the dump file set and control table are undisturbed; `KILL_JOB` cannot be restarted. `DBA_DATAPUMP_JOBS` also lists control tables not associated with an active job.

## Verify
Log ends with `successfully completed`; compare object counts per type
(`dba_objects` group by object_type) and invalid objects after import.

## Checked
Date 2026-10-22. Oracle Database 19c Utilities, Data Pump Export and Import, and Database Reference (DBA_DATAPUMP_JOBS).
Confirmed: FLASHBACK_TIME=systimestamp, FILESIZE, LOGTIME, METRICS, PARALLEL/%U rule, COMPRESSION=ALL licence,
TABLE_EXISTS_ACTION, SQLFILE, TRANSFORM=DISABLE_ARCHIVE_LOGGING scope and FORCE LOGGING caveat, interactive commands
(STATUS, PARALLEL, STOP_JOB=IMMEDIATE, START_JOB), ATTACH, DBA_DATAPUMP_JOBS columns. Removed (not in the pages read):
the "12c+" gate, undo-retention claim, the ORA-39002/39070 note, and the utlrp step.  CREATE DIRECTORY and the READ/WRITE grant
are from the SQL Language Reference; `exclude=statistics` was removed from the export example as unconfirmed.
Method: documentation only; no commands were run.
