---
id: computing-software.database-administration.oracle-database.rman-incrementally-updated-backups
name: rman-incrementally-updated-backups
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, incrementally-updated-backup, block-change-tracking, image-copy, switch-to-copy, merged-incremental]
level: advanced
status: docs-checked
description: "Run RMAN incrementally updated image copies with block change tracking for fast daily backups and near-instant recovery via SWITCH TO COPY."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/backing-up-database-advanced.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/rman-backup-concepts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incrementally updated backups with block change tracking

An image copy of every datafile is kept in the FRA and rolled forward daily with a level 1
incremental. Restore time collapses: instead of restoring terabytes, you **switch** the database to use the copies.

## Block change tracking (BCT)
Without BCT, a level 1 reads every block to find changes. With it, RMAN reads only changed blocks
from a bitmap file.
```sql
ALTER DATABASE ENABLE BLOCK CHANGE TRACKING USING FILE '+DATA';   -- or a path; OMF if omitted with db_create_file_dest
SELECT status, filename, bytes/1048576 mb FROM v$block_change_tracking;
```

## The daily script
```
RUN {
  RECOVER COPY OF DATABASE WITH TAG 'incr_upd' UNTIL TIME 'SYSDATE - 1';
  BACKUP INCREMENTAL LEVEL 1 FOR RECOVER OF COPY WITH TAG 'incr_upd' DATABASE;
  BACKUP ARCHIVELOG ALL NOT BACKED UP 1 TIMES;
}
```
- Day 1: no copy exists, so the BACKUP creates a level 0 image copy; RECOVER does nothing.
- Day 2: BACKUP takes a level 1; RECOVER still has nothing older than a day.
- Day 3+: RECOVER applies yesterday's level 1 to the copy; copy is always 24 h behind (a window to recover from logical errors).
Drop `UNTIL TIME` to keep the copy current (minimum restore time).
Keep a periodic backup set to other media too: the image copies sit in the FRA on the same storage tier.

## Recover by switching
```
RMAN> SQL 'ALTER DATABASE DATAFILE 7 OFFLINE';
RMAN> SWITCH DATAFILE 7 TO COPY;
RMAN> RECOVER DATAFILE 7;
RMAN> SQL 'ALTER DATABASE DATAFILE 7 ONLINE';
```
The database now runs on files in the FRA. Afterwards, create a new copy in the original location
(`BACKUP AS COPY DATAFILE 7 FORMAT '+DATA'`) and switch back during a quiet period, or the FRA becomes your data area.

## Gotchas
- FRA must hold a full copy of the database plus incrementals and archive logs: size it accordingly.
- Retention policy `REDUNDANCY 1` with image copies may delete things you need for point-in-time beyond the copy: use a recovery window and understand `UNTIL TIME` behaviour.
- Different tags make RMAN create new level 0 copies; keep the tag constant.

## Verify
`LIST COPY OF DATABASE` shows copies with recent checkpoint times; a drill of `SWITCH DATAFILE ... TO COPY` on a test database works.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: BACKUP ... FOR RECOVER OF COPY with RECOVER COPY, image copies (BACKUP AS COPY), block change tracking (Backup and Recovery User Guide, incremental backups).

Removed or corrected: edition/standby requirement for BCT, the V$BACKUP_DATAFILE check query, the hidden _bct_bitmaps_per_file parameter and its 8-backup claim, and the whole-database SWITCH example (not found in the cited pages).

Method: documentation only; no commands were run.
