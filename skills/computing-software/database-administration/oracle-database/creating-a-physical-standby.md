---
id: computing-software.database-administration.oracle-database.creating-a-physical-standby
name: creating-a-physical-standby
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, data-guard, standby-creation, active-database-duplication, force-logging, standby-redo-logs]
level: advanced
status: docs-checked
description: "Build an Oracle Data Guard physical standby with RMAN DUPLICATE FOR STANDBY FROM ACTIVE DATABASE: primary prerequisites, parameters, network and verification."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/creating-oracle-data-guard-physical-standby.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-duplicating-databases.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/rcmrf/DUPLICATE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a physical standby

**Goal:** a standby receiving and applying redo. The Data Guard guide documents a backup-and-copy method and DBCA
`createDuplicateDB`; the Backup and Recovery guide documents RMAN `DUPLICATE ... FOR STANDBY`, used here.

## Primary prerequisites
```sql
ALTER DATABASE FORCE LOGGING;      -- the default logging mode lets loads go unlogged and miss the standby
ALTER DATABASE ARCHIVELOG;         -- if not already (needs the database mounted)
ALTER DATABASE ADD STANDBY LOGFILE ('/oracle/dbs/slog1.rdo') SIZE 500M;   -- repeat per group
```
- Alternatives to `FORCE LOGGING` are `STANDBY NOLOGGING FOR DATA AVAILABILITY` and
  `STANDBY NOLOGGING FOR LOAD PERFORMANCE` (database at least mounted to enable).
- Standby redo logs on the primary are a best practice so it can receive redo after a role change; the guide points
  to its "Configuring an Oracle Database to Receive Redo Data" section for log size and group count.
- Parameters in the guide's example (primary Chicago, standby Boston): `DB_UNIQUE_NAME` (unchanged by role
  reversal), `LOG_ARCHIVE_CONFIG='DG_CONFIG=(chicago,boston)'`, `LOG_ARCHIVE_DEST_2='SERVICE=boston ASYNC
  VALID_FOR=(ONLINE_LOGFILES,PRIMARY_ROLE) DB_UNIQUE_NAME=boston'`, `REMOTE_LOGIN_PASSWORDFILE=EXCLUSIVE`, and for
  the standby role `FAL_SERVER`, `DB_FILE_NAME_CONVERT`, `LOG_FILE_NAME_CONVERT`, `STANDBY_FILE_MANAGEMENT=AUTO`.
  The standby uses the primary's `DB_NAME`.
- Redo transport is authenticated by SSL or a remote login password file; with a password file every physical
  standby needs an up-to-date copy of the primary's file. With RMAN `FROM ACTIVE DATABASE` for a standby, RMAN
  always copies the password file.

## Network
- Create Oracle Net service names for primary and standby on both systems (dedicated server connect descriptor),
  and a listener on the standby host.
- For RMAN duplication the auxiliary instance is reached through a statically registered listener entry.

## Duplicate
Start the auxiliary instance `NOMOUNT` with a minimal parameter file, then:
```
rman TARGET sys@orcl AUXILIARY sys@orcl_stby
DUPLICATE TARGET DATABASE FOR STANDBY FROM ACTIVE DATABASE
  USING COMPRESSED BACKUPSET SECTION SIZE 32G
  SPFILE
    SET db_unique_name='orcl_stby'
    SET fal_server='orcl'
  NOFILENAMECHECK;
```
Active duplication needs one of `USING BACKUPSET`, `USING COMPRESSED BACKUPSET` or `SECTION SIZE`. `NOFILENAMECHECK`
is for a remote host; on the local host it overwrites the source's files. Add `DORECOVER` to recover the standby
after the copy (it is left mounted). Use `SET` clauses for other parameters (control files, `db_create_file_dest`,
and so on) as the DUPLICATE reference describes.

## Verify
On the standby, with redo apply started (`ALTER DATABASE RECOVER MANAGED STANDBY DATABASE DISCONNECT FROM SESSION;`
after `STARTUP MOUNT`):
```sql
SELECT ROLE, THREAD#, SEQUENCE#, ACTION FROM V$DATAGUARD_PROCESS;
```
A `recovery logmerger` row showing `APPLYING_LOG` means redo is being applied. Oracle prefers `V$DATAGUARD_PROCESS`
to the deprecated `V$MANAGED_STANDBY`.

## Checked
2026-11-09. Read the 19c Data Guard Concepts and Administration chapter on creating a physical standby (logging
modes, redo transport authentication, standby redo logs, parameter table, standby environment and Redo Apply,
`V$DATAGUARD_PROCESS`), the RMAN duplication chapter (`FOR STANDBY`, active duplication clause requirement,
password file, static listener, `NOFILENAMECHECK` caution; read by search and by section, not every line) and the
`DUPLICATE` reference. Removed because they are not stated there: the Data Guard broker (`DGMGRL`) section and
`dg_broker_start`, the "groups per thread + 1" rule and 1G log size, the `GLOBAL_DBNAME ... _DGMGRL` listener entry,
the `VALIDATE DATABASE` gotchas, `ORA-01578` and unrecoverable-change advice, NTP/lag-reading advice and the `v$dataguard_stats`
and `v$archived_log` checks.
Method: documentation only; no commands were run.
