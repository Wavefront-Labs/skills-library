---
id: computing-software.database-administration.oracle-database.block-media-recovery
name: block-media-recovery
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, block-media-recovery, recover-block, recover-corruption-list, ora-01578, v-database-block-corruption, dbverify, automatic-block-repair, active-data-guard, db-block-checking]
level: advanced
status: docs-checked
description: "Detect corrupt Oracle blocks (ORA-01578, RMAN VALIDATE, DBVERIFY) and repair them online with RMAN RECOVER BLOCK or automatic block repair from a standby."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-block-media-recovery.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/oracle-dbverify-utility.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Block media recovery

**Goal:** fix a few corrupt blocks while the datafile and database stay online,
instead of restoring a whole datafile.

## Detection
- User error: `ORA-01578: ORACLE data block corrupted (file # 7, block # 12345)` with
  `ORA-01110: data file 7: ...`; also in the alert log.
- Proactive scan (reads all blocks, records findings, changes nothing):
```
RMAN> VALIDATE CHECK LOGICAL DATABASE;      -- BACKUP VALIDATE takes the same options; VALIDATE can also check single blocks
RMAN> VALIDATE DATAFILE 7;
```
```sql
SELECT file#, block#, blocks, corruption_change#, corruption_type FROM v$database_block_corruption;
```
`corruption_type`: `ALL ZERO`, `FRACTURED`, `CHECKSUM`, `CORRUPT` (physical) or `LOGICAL` (block passes physical checks but is internally inconsistent; block recovery may not fix it, and tablespace point-in-time recovery may be needed). `corruption_change#` = 0 means media corruption. See `V$NONLOGGED_BLOCK` for nonlogged block ranges.
- DBVERIFY works on offline or online files and backup copies: `dbv file=/u01/oradata/ORCL/users01.dbf blocksize=8192` (`BLOCKSIZE` needed unless the file uses 2 KB blocks; `USERID` for ASM files). On an open database blocks in flux are reported as "Influx".

## Repair with RMAN
```
RMAN> RECOVER DATAFILE 7 BLOCK 12345;
RMAN> RECOVER DATAFILE 7 BLOCK 12345 DATAFILE 9 BLOCK 200;
RMAN> RECOVER CORRUPTION LIST;          -- everything in v$database_block_corruption
```
By default RMAN searches for a good copy of each block in this order: a real-time query physical standby, flashback logs (Flashback Database must be enabled), then full or level 0 backups; it then applies archived redo. Limit the search with `FROM TAG`, `FROM BACKUPSET` or `EXCLUDE FLASHBACK LOG`. Requirements: ARCHIVELOG mode, full or level 0 backups (incrementals and proxy copies do not qualify), and the archived logs since the backup.

## Automatic block repair (Active Data Guard)
On a real-time query physical standby the database automatically attempts repair in the background and ORA-01578 appears only if repair fails. This needs an Active Data Guard licence and either `LOG_ARCHIVE_CONFIG` with a `DG_CONFIG` list and a primary `LOG_ARCHIVE_DEST_n` using `DB_UNIQUE_NAME`, or `FAL_SERVER` naming the primary. Corruption found by `VALIDATE` does not trigger automatic recovery.

## Which object is hit
```sql
SELECT owner, segment_name, segment_type, partition_name
FROM dba_extents WHERE file_id = 7 AND 12345 BETWEEN block_id AND block_id + blocks - 1;
```
If it is an index, rebuild or recreate it from the table instead of recovering the block. If no backup can fix a table block, see the `DBMS_REPAIR` package documentation for the last-resort options (data in the block is lost).

## Prevention and root cause
- `DB_BLOCK_CHECKSUM = TYPICAL` (default; documented overhead about 1-2%, `FULL` about 4-5%) verifies checksums on read.
  `DB_ULTRA_SAFE = DATA_ONLY` sets `DB_BLOCK_CHECKING=MEDIUM`, `DB_BLOCK_CHECKSUM=FULL`, `DB_LOST_WRITE_PROTECT=TYPICAL`;
  `DATA_AND_INDEX` sets `DB_BLOCK_CHECKING=FULL` with the same other two (default `OFF`; not modifiable dynamically).
- Recurring corruption = storage, HBA, multipath or firmware problem; collect OS logs and
  open a hardware case.
- Schedule weekly `BACKUP VALIDATE CHECK LOGICAL` (or `VALIDATE CHECK LOGICAL`) so corruption is found while backups
  that predate it are still retained.

## Verify
- [ ] After repair, `VALIDATE DATAFILE 7` returns no corrupt blocks and
      `v$database_block_corruption` is empty.
- [ ] Query on the affected object succeeds; root cause ticket opened.

## Checked
Date 2026-10-22. Oracle Database 19c Backup and Recovery User's Guide (block media recovery), Utilities (DBVERIFY),
Database Reference (V$DATABASE_BLOCK_CORRUPTION, DB_BLOCK_CHECKSUM, DB_ULTRA_SAFE). Confirmed: `RECOVER ... BLOCK`
and `RECOVER CORRUPTION LIST`, ORA-01578/ORA-01110 form, corruption types, search order and requirements, automatic
repair conditions, dbv parameters. Corrected: search order (standby, flashback logs, then full/level 0 backups; the
skill listed image copies and backup sets generically), corruption_type list was missing ALL ZERO, automatic repair is
documented for a real-time query standby (the "vice versa" claim and the alert log message were removed as unconfirmed),
NOLOGGING claim replaced with V$NONLOGGED_BLOCK. Replaced block-range forms (`BLOCK n TO m`), whose grammar is only in an image diagram, with documented single-block and whole-file forms; `VALIDATE CHECK LOGICAL DATABASE` and `VALIDATE DATAFILE` are from the RMAN reference VALIDATE page.
Method: documentation only; no commands were run.
