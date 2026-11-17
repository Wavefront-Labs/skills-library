---
id: computing-software.database-administration.mysql.innodb-crash-recovery-and-force-recovery
name: innodb-crash-recovery-and-force-recovery
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, innodb, innodb-force-recovery, crash-recovery, corruption, data-salvage, redo-log, mysqld-wont-start]
level: advanced
status: docs-checked
description: "Get a crashed MySQL server with a corrupted InnoDB tablespace started with innodb_force_recovery levels, dump what can be saved, and rebuild instead of running on it."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/forcing-innodb-recovery.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-recovery.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InnoDB crash recovery and innodb_force_recovery

**Goal:** when mysqld will not start because InnoDB is corrupt, salvage the data
with the least risk, then rebuild clean.

## First: is it really corruption?
Normal crash recovery (redo apply, undo rollback) is automatic and can take a
long time after a crash with a big redo log: watch the error log for progress
before intervening. Disk full, permissions, wrong `innodb_redo_log_capacity`
after an upgrade, or a missing file produce errors that look scary but are not corruption.

## Before touching anything
**Copy the whole data directory** (stopped) to another disk. Every recovery step
can make things worse; you want to be able to start over. Check for a replica or
backup + binlogs that make salvage unnecessary: restoring is usually faster and safer.

## Force recovery levels
In my.cnf `[mysqld] innodb_force_recovery = N`, start with 1 and go up only if needed:
| N | Skips |
|---|---|
| 1 (SRV_FORCE_IGNORE_CORRUPT) | Corrupt pages (keeps running despite them) |
| 2 (SRV_FORCE_NO_BACKGROUND) | Master thread and purge threads |
| 3 | Transaction rollback after recovery |
| 4 | Insert buffer merge operations; table statistics (can corrupt data files permanently; be ready to drop and recreate secondary indexes) |
| 5 | Undo logs (treats incomplete transactions as committed) |
| 6 | Redo log roll-forward |
Levels >= 4 can permanently damage data files and put InnoDB in read-only mode; any value above 0 blocks INSERT, UPDATE and DELETE. Only SELECT, dump and DROP are the goal here.

## Salvage
With the server up at the lowest working level:
```bash
mysqldump --all-databases --routines --events --triggers > salvage.sql
# or per table to skip the broken one:
mysqldump appdb orders > orders.sql
```
A table that crashes the server on dump: dump around the bad range (SELECT with a key-range WHERE into OUTFILE) to skip corrupt pages. A table whose rollback crashes the server can be dropped after starting at level 3.

## Rebuild
Initialise a fresh data directory (`mysqld --initialize`), start normally, load
the dumps, recreate users, and verify. Never keep running production on a
force-recovery instance.

## Gotchas
- Page-corruption messages in the error log name the tablespace and page: check the disk and storage layer first.

## Verify
Restored instance starts without force_recovery; `CHECK TABLE` on key tables is
OK; row counts match the salvage dump.

## Checked

2026-11-01. Confirmed against MySQL 8.4 manual pages forcing-innodb-recovery (levels 1-6 names and effects, read-only behaviour, 3-or-less safety statement), innodb-recovery. Removed unconfirmed tool and error-message references and the MariaDB/Galera note.

Method: documentation only; no commands were run.
