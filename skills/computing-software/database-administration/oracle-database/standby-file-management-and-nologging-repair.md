---
id: computing-software.database-administration.oracle-database.standby-file-management-and-nologging-repair
name: standby-file-management-and-nologging-repair
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, standby-file-management, data-guard, unnamed-file, ora-01274, nologging, ora-26040, physical-standby]
level: advanced
status: docs-checked
description: "Keep Oracle physical standbys in step with primary file changes: STANDBY_FILE_MANAGEMENT, fixing UNNAMED files after ORA-01274, and repairing NOLOGGING blocks."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/managing-oracle-data-guard-physical-standby-databases.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/STANDBY_FILE_MANAGEMENT.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standby file management and NOLOGGING repair

## STANDBY_FILE_MANAGEMENT
```sql
ALTER SYSTEM SET standby_file_management = AUTO SCOPE = BOTH;   -- on standby AND primary (for role changes)
```
With AUTO, datafiles added on the primary are created on the standby (OMF, or renamed via
`db_file_name_convert`). Drops are applied too. With MANUAL, a new datafile on the primary stops redo apply.

## Recover from an UNNAMED placeholder file (file added while MANUAL or conversion failed)
The standby creates a placeholder datafile:
```sql
SELECT file#, name FROM v$datafile WHERE name LIKE '%UNNAMED%';
-- e.g. $ORACLE_HOME/dbs/UNNAMED00012
ALTER SYSTEM SET standby_file_management = MANUAL;
ALTER DATABASE CREATE DATAFILE '/u01/app/oracle/product/19/dbs/UNNAMED00012' AS '+DATA' ;   -- or a full path
ALTER SYSTEM SET standby_file_management = AUTO;
ALTER DATABASE RECOVER MANAGED STANDBY DATABASE DISCONNECT;   -- or DGMGRL: EDIT DATABASE stby SET STATE = 'APPLY-ON'
```
Other manual operations on the standby with AUTO (renaming files, adding/dropping online/standby redo) need it temporarily set to MANUAL.

## NOLOGGING on the primary
Direct-path NOLOGGING loads put no data redo into the stream; the standby marks those blocks
invalid. Queries on those blocks fail, and after failover the data is gone.
Detect:
```sql
-- on the standby
SELECT * FROM v$nonlogged_block;
```
Prevent: `ALTER DATABASE FORCE LOGGING;` on the primary (standard), or 18c+ `ALTER DATABASE SET STANDBY NOLOGGING FOR DATA AVAILABILITY`.
Repair:
```sql
-- 18c+, on the standby, apply stopped
RECOVER STANDBY DATABASE NONLOGGED BLOCK;      -- fetches blocks from the primary
-- 12.2 and older: restore the affected datafiles from the primary over the network
```
```
RMAN> RESTORE DATAFILE 7 FROM SERVICE prim_tns;   -- connected to the standby as target
```
Restart apply after either fix.

## Gotchas
- `db_file_name_convert` strings are simple substring replacements; a missing mapping puts new files in `$ORACLE_HOME/dbs`.
- Check after any bulk load by vendors: they often use NOLOGGING without telling anyone.

## Verify
No `UNNAMED` files, `v$nonlogged_block` empty on the standby, and apply lag back to normal.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: V$NONLOGGED_BLOCK, RECOVER ... NONLOGGED BLOCK, FORCE LOGGING and STANDBY NOLOGGING modes, UNNAMED placeholder files, db_file_name_convert semantics (Data Guard Concepts; RMAN reference).

Removed or corrected: ORA-01274 and ORA-28365 attributions, v$datafile first_nonlogged columns, version tag on V$NONLOGGED_BLOCK and the online-move-on-ADG remark (not found in the cited pages).

Method: documentation only; no commands were run.
