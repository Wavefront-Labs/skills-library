---
id: computing-software.database-administration.oracle-database.full-transportable-export-import
name: full-transportable-export-import
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, full-transportable, data-pump, cross-platform-migration, endian-conversion, rman-convert, xtts, migration]
level: sme
status: docs-checked
description: "Migrate a whole Oracle database with full transportable export/import, including cross-endian conversion and incremental-backup XTTS to cut downtime."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/transporting-data.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-data-pump-export-utility.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full transportable export/import

Moves an entire database (11.2.0.3+ source, 12c+ target) by copying the user tablespace datafiles
and exporting only metadata with Data Pump: far faster than a conventional export for large databases.
Common use: non-CDB to PDB, platform change (AIX/Solaris SPARC to Linux), version upgrade in one step.

## Prepare
```sql
-- source: which platform/endian
SELECT d.platform_name, tp.endian_format FROM v$database d JOIN v$transportable_platform tp ON tp.platform_name = d.platform_name;
-- self-contained check for all user tablespaces
EXEC DBMS_TTS.TRANSPORT_SET_CHECK('USERS,APP_DATA,APP_IDX', TRUE);
SELECT * FROM transport_set_violations;
```
Target must have the same or a superset character set. Tables with TIMESTAMP WITH TIME ZONE columns cannot be transported across platforms with different time zone file versions (they are skipped).

## Run
```sql
-- source: read-only (downtime starts)
ALTER TABLESPACE app_data READ ONLY; ALTER TABLESPACE app_idx READ ONLY; ALTER TABLESPACE users READ ONLY;
```
```bash
expdp system FULL=Y TRANSPORTABLE=ALWAYS VERSION=12 DIRECTORY=dp_dir DUMPFILE=full_tts.dmp LOGFILE=full_tts_exp.log METRICS=Y
# VERSION=12 is required when the source is 11.2.0.3/4
```
Copy datafiles listed at the end of the export log, plus the dump file, to the target.
Cross-endian: convert (on either side):
```
RMAN> CONVERT DATAFILE '/stage/app_data01.dbf' FROM PLATFORM 'AIX-Based Systems (64-bit)' FORMAT '+DATA';
```
or `DBMS_FILE_TRANSFER.GET_FILE`/`PUT_FILE`, which convert automatically.
```bash
# target (new PDB created empty)
impdp system@pdb1 FULL=Y DIRECTORY=dp_dir DUMPFILE=full_tts.dmp LOGFILE=full_tts_imp.log METRICS=Y \
  TRANSPORT_DATAFILES='+DATA/app_data01.dbf','+DATA/app_idx01.dbf','+DATA/users01.dbf'
```
Then `ALTER TABLESPACE ... READ WRITE` on the target, recompile (`utlrp.sql`), gather dictionary stats, compare object counts.

## Network mode (no dump file)
`impdp ... NETWORK_LINK=src_link FULL=Y TRANSPORTABLE=ALWAYS VERSION=12 TRANSPORT_DATAFILES=...` pulls metadata over a database link.

## Reduce downtime: incremental XTTS
Oracle's cross-platform incremental-backup XTTS scripts are on My Oracle Support (login required;
search for the current note): copy and convert a level 0 backup while the source is open, roll
forward with repeated incrementals, and only the final incremental plus metadata export happens in
the read-only window.

## Gotchas
- SYSTEM/SYSAUX objects owned by users (rare, but happens) are not transported; check `transport_set_violations` and move them first.
- Encrypted tablespaces need `ENCRYPTION_PASSWORD` on expdp and the keys at the target.
- Read-only tablespaces on the source mean the application is down for the whole copy unless you use XTTS.

## Checked
2026-11-01. Confirmed on the 19c Administrator's Guide Transporting Data page: 11.2.0.3 source, VERSION=12, endian conversion by DBMS_FILE_TRANSFER or RMAN CONVERT, V$TRANSPORTABLE_PLATFORM, ENCRYPTION_PASSWORD, TSTZ restriction. Removed: MOS note number, ENCRYPTION_PWD_PROMPT, LOGTIME and METRICS advice, time zone >= claim (replaced by documented TSTZ restriction).
Method: documentation only; no commands were run.

## Verify
Object counts and invalid objects per schema match, row counts on key tables match, and the application smoke test passes on the target.
