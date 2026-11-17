---
id: computing-software.database-administration.oracle-database.database-and-tablespace-point-in-time-recovery
name: database-and-tablespace-point-in-time-recovery
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, dbpitr, tspitr, point-in-time-recovery, auxiliary-instance, logical-corruption, incarnation]
level: advanced
status: draft
description: "Undo a logical error in Oracle with RMAN database point-in-time recovery (DBPITR) or tablespace PITR (TSPITR) using an automatic auxiliary instance."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-performing-flashback-dbpitr.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-tspitr.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database and tablespace point-in-time recovery

Choose the smallest tool: Flashback Query/Table (seconds, needs undo), `RECOVER TABLE` (one table
from backup), TSPITR (a self-contained set of tablespaces), Flashback Database (whole DB, needs flashback logs),
DBPITR (whole database from backups; everything after the target time is lost).

## Find the target time or SCN
LogMiner, the application log, or the alert log; convert: `SELECT TIMESTAMP_TO_SCN(TIMESTAMP '2026-10-18 09:55:00') FROM dual;`.
Choose a point **just before** the bad transaction.

## DBPITR
```
RMAN> SHUTDOWN IMMEDIATE;
RMAN> STARTUP MOUNT;
RMAN> RUN {
  SET UNTIL TIME "TO_DATE('2026-10-18 09:54:00','YYYY-MM-DD HH24:MI:SS')";   -- or UNTIL SCN / UNTIL SEQUENCE n THREAD 1
  RESTORE DATABASE;
  RECOVER DATABASE;
}
RMAN> ALTER DATABASE OPEN RESETLOGS;
```
Set `NLS_DATE_FORMAT` in the environment or use `TO_DATE` explicitly. Not sure of the time? Open
read-only to check before RESETLOGS: `ALTER DATABASE OPEN READ ONLY;` then, if more recovery is needed, shut down, mount and `RECOVER DATABASE UNTIL ...` again.
PDB-level PITR (12c+): `RECOVER PLUGGABLE DATABASE pdb1 UNTIL TIME ... AUXILIARY DESTINATION '/aux';` with the PDB closed, then `ALTER PLUGGABLE DATABASE pdb1 OPEN RESETLOGS;`.
Take a new backup afterwards. To go back to the abandoned future: `RESET DATABASE TO INCARNATION n`.

## TSPITR
Recovers chosen tablespaces to an earlier time while the rest of the database stays current and open.
```
RMAN> RECOVER TABLESPACE app_data, app_idx
      UNTIL TIME "TO_DATE('2026-10-18 09:54:00','YYYY-MM-DD HH24:MI:SS')"
      AUXILIARY DESTINATION '/u05/aux';
```
RMAN builds an auxiliary instance (restores SYSTEM, SYSAUX, UNDO plus the targets), recovers it,
exports the tablespaces' metadata with Data Pump transportable, and plugs them back. Afterwards the
tablespaces are OFFLINE: back them up, then `ALTER TABLESPACE app_data ONLINE;`.
Checks first:
```sql
EXEC DBMS_TTS.TRANSPORT_SET_CHECK('APP_DATA,APP_IDX', TRUE);
SELECT * FROM transport_set_violations;
SELECT owner, name, creation_time FROM ts_pitr_objects_to_be_dropped
WHERE tablespace_name IN ('APP_DATA','APP_IDX')
  AND creation_time > TO_DATE('2026-10-18 09:54:00','YYYY-MM-DD HH24:MI:SS');   -- lost by TSPITR
```

## Gotchas
- Auxiliary destination needs space for SYSTEM/SYSAUX/UNDO plus recovered tablespaces.
- A tablespace dropped can be recovered with TSPITR only with a recovery catalog (or 12c+ in some cases).
- TSPITR cannot recover tablespaces containing SYS objects, undo, or objects with dependencies outside the set.
- DBPITR loses all work after the target for every user: confirm with the business before running.

## Verify
The erroneous data is back as of the target time; a fresh backup exists; `LIST INCARNATION` shows the new incarnation after DBPITR.
