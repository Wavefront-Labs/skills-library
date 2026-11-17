---
id: computing-software.database-administration.oracle-database.transportable-tablespaces
name: transportable-tablespaces
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, data-pump, transportable-tablespaces, full-transportable-export, cross-platform-transport, endian-conversion, rman-convert, dbms-tts, xtts, incremental-xtts, migration]
level: advanced
status: docs-checked
description: "Move large Oracle tablespaces between databases and platforms with transportable tablespaces or full transportable export, including endian conversion and XTTS."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/transporting-data.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-data-pump-overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transportable tablespaces

**Goal:** move terabytes by copying datafiles plus a small metadata export, instead of
unloading and reloading rows.

## Check the set is self-contained
```sql
EXEC DBMS_TTS.TRANSPORT_SET_CHECK('APP_DATA,APP_IDX', incl_constraints => TRUE, full_check => TRUE);
SELECT * FROM transport_set_violations;      -- must be empty
```
Violations: an index in APP_IDX on a table outside the set, partitions spread across
tablespaces not in the set, LOBs elsewhere. Objects in SYSTEM/SYSAUX never transport.

## Same platform (endian) example
```sql
ALTER TABLESPACE app_data READ ONLY;
ALTER TABLESPACE app_idx  READ ONLY;
```
```bash
expdp system DIRECTORY=DP_DIR DUMPFILE=tts_app.dmp LOGFILE=tts_exp.log \
  TRANSPORT_TABLESPACES=APP_DATA,APP_IDX TRANSPORT_FULL_CHECK=YES
# copy datafiles + dump to target (scp, ASM asmcmd cp, DBMS_FILE_TRANSFER)
impdp system DIRECTORY=DP_DIR DUMPFILE=tts_app.dmp LOGFILE=tts_imp.log \
  TRANSPORT_DATAFILES='/u02/oradata/TGT/app_data01.dbf','/u02/oradata/TGT/app_idx01.dbf'
```
```sql
ALTER TABLESPACE app_data READ WRITE;   -- on target (and source, if it stays)
```
Owners of the objects must exist in the target first (or use `REMAP_SCHEMA`); the target
must have the same or compatible character set and national character set, and a
compatible `COMPATIBLE` setting. Downtime = the read-only window.

## Cross-platform: endian conversion
```sql
SELECT platform_name, endian_format FROM v$transportable_platform;   -- e.g. AIX big vs Linux little
SELECT platform_name FROM v$database;
```
Different endian requires conversion of datafiles: run RMAN CONVERT on the source or the target, or use `DBMS_FILE_TRANSFER.GET_FILE`/`PUT_FILE`, which convert automatically:
```
RMAN> CONVERT DATAFILE '/stage/app_data01.dbf' FROM PLATFORM 'AIX-Based Systems (64-bit)'
      FORMAT '+DATA';        -- on target
```

## Full transportable export/import (12c+)
Moves a whole database (user tablespaces as files, everything else as metadata) into
a fresh database, e.g. 11.2.0.3+ non-CDB into a 19c PDB:
```bash
expdp system FULL=Y TRANSPORTABLE=ALWAYS VERSION=12 DIRECTORY=DP_DIR DUMPFILE=full_tts.dmp
impdp system@newpdb FULL=Y DIRECTORY=DP_DIR DUMPFILE=full_tts.dmp TRANSPORT_DATAFILES=...
```
`VERSION=12` is needed when the source is 11.2.0.3/11.2.0.4.

## Minimising downtime: incremental XTTS
Oracle publishes cross-platform incremental-backup XTTS procedures and scripts on My Oracle
Support (login required; search for the current note). The idea: copy a level 0 backup while the
source is open, roll it forward with repeated converted incrementals, and keep only the last
incremental plus metadata export in the read-only window.

## Gotchas
- `TRANSPORT_DATAFILES` must name the copied datafiles exactly.
- Encrypted tablespaces need `ENCRYPTION_PASSWORD` on expdp and the keys at the target.
- Tables with TIMESTAMP WITH TIME ZONE columns cannot be transported across platforms with different time zone file versions: the operation skips them, so move them with a conventional export/import.

## Checked
2026-11-01. Confirmed on the 19c Administrator's Guide Transporting Data page: 11.2.0.3 source for full transportable, VERSION=12, endian conversion by DBMS_FILE_TRANSFER or RMAN CONVERT (source or target), V$TRANSPORTABLE_PLATFORM, ENCRYPTION_PASSWORD, SYSTEM/SYSAUX handling, TSTZ restriction. Removed: BACKUP TO PLATFORM, ORA error numbers, MOS note number and title (MOS is login-only), statistics claim.
Method: documentation only; no commands were run.

## Verify
- [ ] `TRANSPORT_SET_VIOLATIONS` empty before the window.
- [ ] Rehearsal timed: copy, convert, import within the downtime budget.
- [ ] Row counts / object counts match after import; tablespaces READ WRITE.
