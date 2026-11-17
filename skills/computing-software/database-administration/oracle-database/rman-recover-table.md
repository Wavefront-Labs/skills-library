---
id: computing-software.database-administration.oracle-database.rman-recover-table
name: rman-recover-table
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, rman, rman-recover-table, auxiliary-instance, point-in-time-recovery, dropped-table, data-pump]
level: advanced
status: docs-checked
description: "Recover one dropped or damaged Oracle table to a point in time with RMAN RECOVER TABLE using an automatic auxiliary instance, when flashback cannot help."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-recovering-tables-partitions.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/rcmrf/RECOVER.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RMAN RECOVER TABLE

## When to use
Try the cheap options first:
1. `FLASHBACK TABLE t TO BEFORE DROP` (recycle bin, if not purged).
2. `FLASHBACK TABLE t TO TIMESTAMP ...` / flashback query (if undo still has the data).
3. Flashback Database (whole database rewinds: rarely acceptable for one table).
RMAN RECOVER TABLE works when undo/recycle bin are gone, as long as you have backups and
archived logs covering the target time.

## How it works
RMAN builds a temporary **auxiliary instance**, restores SYSTEM/SYSAUX/UNDO plus the
tablespaces containing the table to the auxiliary destination, recovers to the target time,
exports the table with Data Pump, imports it into the target database, then removes the
auxiliary instance.

## Command
```
RMAN> RECOVER TABLE app.orders
        UNTIL TIME "TO_DATE('2026-10-18 09:14:00','YYYY-MM-DD HH24:MI:SS')"
        AUXILIARY DESTINATION '/u05/rman_aux'
        REMAP TABLE app.orders:orders_0914;
```
Options:
- `UNTIL SCN n` / `UNTIL SEQUENCE n` instead of time.
- `REMAP TABLE` imports under a new name (recommended: compare and copy rows back yourself).
  `REMAP TABLESPACE` for a different target tablespace.
- `NOTABLEIMPORT` + `DATAPUMP DESTINATION '/u05/dp' DUMP FILE 'orders.dmp'`: only produce the
  dump file; import manually.

## Requirements and gotchas
- Free space in the auxiliary destination for SYSTEM, SYSAUX, UNDO and the table's tablespaces
  (whole tablespaces, not just the table).
- Database in ARCHIVELOG mode with all archives from the backup to the target time available.
- It takes as long as restoring those tablespaces; on multi-TB tablespaces consider a full
  duplicate to another host instead.

## After
```sql
SELECT COUNT(*) FROM app.orders_0914;
INSERT INTO app.orders SELECT * FROM app.orders_0914 o
  WHERE NOT EXISTS (SELECT 1 FROM app.orders x WHERE x.order_id = o.order_id);
```

## Verify
RMAN log ends with `Finished recover`, the remapped table exists with the expected rows as of the
target time, and the auxiliary destination is cleaned up.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: RECOVER TABLE with UNTIL, AUXILIARY DESTINATION, REMAP TABLE, REMAP TABLESPACE, DATAPUMP DESTINATION and NOTABLEIMPORT; auxiliary instance restores SYSTEM/SYSAUX/UNDO (Backup and Recovery User Guide, recovering tables and table partitions).

Removed or corrected: edition/release statement, TIMESTAMP_TO_SCN hint, partition and PDB syntax forms and the restriction and foreign-key remarks (not found in the cited pages).

Method: documentation only; no commands were run.
