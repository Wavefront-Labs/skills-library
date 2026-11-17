---
id: computing-software.database-administration.oracle-database.flashback-database-and-table
name: flashback-database-and-table
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, flashback-database, flashback-table, flashback-query, flashback-drop, recyclebin, guaranteed-restore-point, db-flashback-retention-target, flashback-pdb, logical-corruption]
level: advanced
status: docs-checked
description: "Undo logical mistakes in Oracle with Flashback Query, Table, Drop and Database, guaranteed restore points for upgrades, and the space and retention rules they need."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/using-flasback-database-restore-points.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/FLASHBACK-TABLE.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/adfns/flashback.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flashback database and table

Pick the smallest tool that undoes the mistake.

| Mistake | Tool | Depends on |
|---|---|---|
| Wrong UPDATE/DELETE, see old rows | Flashback Query `AS OF` | undo retention |
| Rewind one table | `FLASHBACK TABLE ... TO TIMESTAMP` | undo + row movement |
| Dropped table | `FLASHBACK TABLE ... TO BEFORE DROP` | recycle bin |
| Many objects / whole DB / failed upgrade | `FLASHBACK DATABASE` | flashback logs in FRA |
| Truncated table, beyond undo | RMAN `RECOVER TABLE` | backups |

## Flashback Query
```sql
SELECT * FROM app.orders AS OF TIMESTAMP SYSTIMESTAMP - INTERVAL '15' MINUTE WHERE order_id = 42;
INSERT INTO app.orders SELECT * FROM app.orders AS OF TIMESTAMP TO_TIMESTAMP('2026-10-16 09:00','YYYY-MM-DD HH24:MI')
  WHERE order_id IN (SELECT order_id FROM app.orders AS OF TIMESTAMP ... MINUS SELECT order_id FROM app.orders);
SELECT versions_starttime, versions_operation, o.* FROM app.orders VERSIONS BETWEEN TIMESTAMP SYSTIMESTAMP - INTERVAL '1' HOUR AND SYSTIMESTAMP o WHERE order_id = 42;
```
Timestamps map to SCNs at roughly 3-second granularity (use an SCN for precision). DDL that changes the table's structure (drop/modify column, move, truncate, add constraint, partition changes) invalidates earlier undo: querying data from before it raises ORA-01466.

## Flashback Table
```sql
ALTER TABLE app.orders ENABLE ROW MOVEMENT;
FLASHBACK TABLE app.orders TO TIMESTAMP SYSTIMESTAMP - INTERVAL '20' MINUTE;
FLASHBACK TABLE app.orders TO BEFORE DROP;                    -- from recycle bin
FLASHBACK TABLE app.orders TO BEFORE DROP RENAME TO orders_restored;
SELECT object_name, original_name, droptime FROM dba_recyclebin WHERE owner = 'APP';   -- PURGE removes recycle bin objects permanently
```
`TO TIMESTAMP`/`TO SCN`/`TO RESTORE POINT` use undo and need row movement; `TO BEFORE DROP` uses the recycle bin and does not (with the original name, the most recently dropped version is restored). Structural DDL (move, truncate, add constraint, modify/drop column, most partition operations) blocks flashback to before it; objects in a cluster, materialized views, AQ tables, object/nested tables, system and static data dictionary tables and single partitions cannot be flashed back; a purged table cannot be restored. Restored indexes, triggers and constraints keep system-generated recycle bin names: query `USER_RECYCLEBIN` first so you can rename them. A `FLASHBACK TABLE` cannot be rolled back except by another flashback, so record the current SCN first.

## Flashback Database
Needs ARCHIVELOG and a fast recovery area (on RAC, on ASM or a clustered file system); flashback logs live in the FRA:
```sql
ALTER SYSTEM SET db_flashback_retention_target = 1440 SCOPE=BOTH;   -- minutes (default 1440), a target not a guarantee
ALTER DATABASE FLASHBACK ON;
SELECT oldest_flashback_scn, oldest_flashback_time, retention_target, flashback_size, estimated_flashback_size FROM v$flashback_database_log;
```
`ALTER TABLESPACE name FLASHBACK OFF` excludes a tablespace. A top wait of `flashback buf free by RVWR` suggests slow flashback log storage.
Rewind:
```sql
SHUTDOWN IMMEDIATE; STARTUP MOUNT;
FLASHBACK DATABASE TO RESTORE POINT before_deploy;      -- or TO SCN n
ALTER DATABASE OPEN RESETLOGS;
```
Flashback Database cannot undo dropping a tablespace, shrinking a datafile or dropping a datafile (use RMAN restore and recover). Recreating or restoring the control file discards flashback log information. Rewinding across a NOLOGGING operation can leave corruption: back up the affected files afterwards. PDB restore points need `COMPATIBLE` 12.2.0 or higher.

## Guaranteed restore points (upgrades, risky deploys)
```sql
CREATE RESTORE POINT before_ru_19_25 GUARANTEE FLASHBACK DATABASE;
-- ... upgrade / deploy ...
DROP RESTORE POINT before_ru_19_25;    -- ALWAYS drop after success
SELECT name, guarantee_flashback_database, storage_size/1048576 mb FROM v$restore_point;
```
Guaranteed restore points never age out and must be dropped explicitly; `STORAGE_SIZE` is the FRA space retained. With flashback logging off you can flash back to the restore point but not to SCNs between it and now; with it on you can rewind to any SCN since. If the FRA fills, files required by a guaranteed restore point cannot be deleted and the database can halt: monitor FRA usage. While a guaranteed restore point exists you cannot raise `COMPATIBLE`.

## Data Guard
The Backup and Recovery guide notes Flashback Database can replace rebuilding a failed primary; see the Data Guard documentation for reinstatement requirements.

## Verify
- [ ] `flashback_on = YES` where needed and oldest flashback time meets the target.
- [ ] No stale guaranteed restore points; FRA usage under threshold.
- [ ] Recycle bin enabled (`SHOW PARAMETER recyclebin`).

## Checked
Date 2026-10-22. Oracle Database 19c Backup and Recovery User's Guide (Using Flashback Database and Restore Points; the
live URL contains the spelling "flasback"), SQL Language Reference (FLASHBACK TABLE), Development Guide (flashback query) and
Database Reference (V$FLASHBACK_DATABASE_LOG, DBA_RECYCLEBIN). Confirmed: ARCHIVELOG + FRA prerequisites,
DB_FLASHBACK_RETENTION_TARGET default and meaning, CREATE/DROP RESTORE POINT forms, V$RESTORE_POINT columns, guaranteed restore
point behaviour with logging on/off and FRA-full risk, COMPATIBLE restriction, FLASHBACK TABLE row movement and restrictions,
recycle bin naming note, flashback query timing, ORA-01466. Removed (not found in the pages read): "online since 11gR2",
OPEN READ ONLY check, FLASHBACK DATABASE TO TIMESTAMP and PDB flashback examples, ORA-01555/ORA-08180 meanings,
`recyclebin=off` and `DROP ... PURGE` remarks, the Data Guard reinstatement claim. Two original source URLs returned 404.
Method: documentation only; no commands were run.
