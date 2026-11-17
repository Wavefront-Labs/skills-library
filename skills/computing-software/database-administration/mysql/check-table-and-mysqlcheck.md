---
id: computing-software.database-administration.mysql.check-table-and-mysqlcheck
name: check-table-and-mysqlcheck
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysqlcheck, check-table, repair-table, myisamchk, analyze-table, optimize-table, table-maintenance]
level: practitioner
status: verified
description: "Check and repair MySQL tables with CHECK TABLE, mysqlcheck and myisamchk, know what REPAIR can and cannot do for InnoDB, and run ANALYZE/OPTIMIZE safely."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/check-table.html
  - https://dev.mysql.com/doc/refman/8.4/en/mysqlcheck.html
  - https://dev.mysql.com/doc/refman/8.4/en/myisamchk.html
  - https://dev.mysql.com/doc/refman/8.4/en/optimize-table.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table maintenance and repair (CHECK TABLE / mysqlcheck / myisamchk)

## CHECK TABLE
```sql
CHECK TABLE shop.orders;                  -- InnoDB: checks pages, index consistency; holds a shared lock
CHECK TABLE shop.orders EXTENDED;         -- slower, more thorough
CHECK TABLE shop.orders FOR UPGRADE;      -- incompatibilities with the current version
```
`Msg_type error` / `status Corrupt` = act. For InnoDB, the 8.4 manual says that if `CHECK TABLE` meets a corrupt page the server exits to prevent error propagation (even for corruption confined to a secondary index), and it can cause a server exit on a corrupt `DB_TRX_ID`/`DB_ROLL_PTR`; it also does not detect problems confined to the first 3 header pages of an `.ibd` file (use `innochecksum` for the whole file). Run it on a replica or a restored copy when corruption is suspected. On 9.7.4 `CHECK TABLE`, `EXTENDED` and `FOR UPGRADE` each returned `status OK` for a healthy InnoDB table.

## mysqlcheck (client wrapper for CHECK/REPAIR/ANALYZE/OPTIMIZE)
```bash
mysqlcheck --all-databases --check --silent          # report only problems
mysqlcheck shop --analyze                             # refresh index statistics
mysqlcheck shop orders --optimize
mysqlcheck --all-databases --check-upgrade --auto-repair   # legacy upgrade path
```
Runs table by table online; still takes locks per table. Schedule at low traffic. All five invocations above ran against 9.7.4 (`--check` printed `OK` per table; `--analyze` on the MyISAM table said `Table is already up to date`; `--optimize` printed the InnoDB `Table does not support optimize, doing recreate + analyze instead` note).

## InnoDB corruption: REPAIR does not apply
`REPAIR TABLE` works for MyISAM, ARCHIVE, CSV only (on 9.7.4 `REPAIR TABLE` on an InnoDB table returned the note "The storage engine for the table doesn't support repair"; on a MyISAM table it returned `OK`). For InnoDB:
1. Corruption in a secondary index: drop and recreate the index (`ALTER TABLE t DROP INDEX i, ADD INDEX i (...)`) or `ALTER TABLE t ENGINE=InnoDB` (rebuild).
2. Corrupt clustered index / pages: restore from backup or a replica. As a last resort, start with `innodb_force_recovery` (1 upward), dump what can be read, rebuild.
3. Check the error log for InnoDB corruption messages and the hardware (disk, memory) behind it.

## myisamchk (offline MyISAM)
```bash
systemctl stop mysqld            # Linux example; or FLUSH TABLES WITH READ LOCK and no writes; never with the server writing the table
myisamchk --check /var/lib/mysql/legacy/*.MYI
myisamchk --recover --sort-buffer-size=256M /var/lib/mysql/legacy/t.MYI
```
Only for MyISAM; MySQL 8 system tables are InnoDB, so this applies to legacy user tables. `myisamchk.exe` ships in the 9.7.4 Windows zip; both `--check` and `--recover --sort-buffer-size=256M` ran on a copy of a small `.MYI`/`.MYD` pair (the `systemctl` line is Linux-only and was not run).

## OPTIMIZE / ANALYZE
- `OPTIMIZE TABLE` on InnoDB is an in-place online rebuild (the manual: an exclusive lock only briefly in the prepare and commit phases; heavy I/O, needs free space about the table size; FULLTEXT tables use the copy method instead). Reclaims space after mass deletes with file-per-table.
- `ANALYZE TABLE` refreshes index statistics quickly; run after bulk loads. Histograms are separate (`ANALYZE TABLE t UPDATE HISTOGRAM ON col`).

## Gotchas
- `mysqlcheck --auto-repair` on InnoDB does nothing useful and can mislead people into thinking tables were fixed (the same invocation on a healthy instance only printed `OK` per table).
- `OPTIMIZE` on a big table is written to the binlog and runs on replicas too (lag); `OPTIMIZE NO_WRITE_TO_BINLOG TABLE` (or `LOCAL`) is accepted and runs it on one node only (the keyword ran on 9.7.4; its binlog effect was not inspected).
