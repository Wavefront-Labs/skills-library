---
id: computing-software.database-administration.mysql.restoring-a-single-table-import-tablespace
name: restoring-a-single-table-import-tablespace
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, xtrabackup, import-tablespace, discard-tablespace, transportable-tablespace, partial-restore, backup-restore]
level: advanced
status: docs-checked
description: "Restore one InnoDB table from a physical backup or another server with FLUSH TABLES FOR EXPORT and ALTER TABLE DISCARD/IMPORT TABLESPACE."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-table-import.html
  - https://docs.percona.com/percona-xtrabackup/8.4/restore-individual-tables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring a single table (IMPORT TABLESPACE)

Use when one table was damaged or wrongly modified and a full restore is overkill. Requires
`innodb_file_per_table=ON` (default), the same InnoDB page size, and an identical table
definition (same `DATA DIRECTORY` clause; same `innodb_default_row_format` if `ROW_FORMAT` is not explicit).
When the table comes from another server, both must be GA releases of the same version. The
table must be in a file-per-table tablespace (not the system or a general tablespace).

## Source A: a prepared XtraBackup
```bash
xtrabackup --prepare --export --target-dir=/backups/full   # writes .cfg files next to .ibd
```
For encrypted tables add `--keyring-file-data=<keyring file>`; the export also produces a `.cfp` file,
which is copied along with the `.ibd` and `.cfg`.

## Source B: a running server (copy a table between servers)
```sql
-- source session (keep it open until copy finishes)
FLUSH TABLES shop.orders FOR EXPORT;      -- quiesces, writes orders.cfg, locks the table
-- copy orders.ibd and orders.cfg out of the datadir now; UNLOCK TABLES deletes the .cfg
UNLOCK TABLES;
```

## Import on the target
```sql
-- 1. table must exist with the exact same definition (columns, row format, indexes)
CREATE TABLE shop.orders_restore LIKE shop.orders;     -- or from SHOW CREATE TABLE of the backup
ALTER TABLE shop.orders_restore DISCARD TABLESPACE;    -- deletes its empty .ibd
```
```bash
cp /backups/full/shop/orders.ibd /var/lib/mysql/shop/orders_restore.ibd
cp /backups/full/shop/orders.cfg /var/lib/mysql/shop/orders_restore.cfg
chown mysql:mysql /var/lib/mysql/shop/orders_restore.*
```
```sql
ALTER TABLE shop.orders_restore IMPORT TABLESPACE;
SELECT count(*) FROM shop.orders_restore;
```
Importing into a differently named table works (as shown); then copy the needed rows back
(`INSERT INTO orders SELECT ... FROM orders_restore WHERE ...`) or swap with `RENAME TABLE`.

## Partitioned tables
Discard/import per partition: `ALTER TABLE t DISCARD PARTITION p2026 TABLESPACE;` then copy
`t#p#p2026.ibd` and `.cfg`, and `IMPORT PARTITION p2026 TABLESPACE`.

## Gotchas
- Without the `.cfg` file, import skips schema verification (a warning is issued); a table with
  columns added or dropped using `ALGORITHM=INSTANT` needs the `.cfg` (otherwise behaviour is undefined).
- A definition that differs from the source (including `DATA DIRECTORY` or default row format)
  raises a schema mismatch error. Partition type or definition differences are not detected for
  partitioned tables.
- Foreign keys: `foreign_key_checks` must be disabled before `DISCARD TABLESPACE`; import does not
  enforce foreign keys on the data, so export related tables at the same point in time.
- `FLUSH TABLES ... FOR EXPORT` does not support tables with a FULLTEXT index; run `OPTIMIZE TABLE`
  after importing such a table (or drop the index before export and recreate it).
- Create databases and tables in lowercase to avoid case problems on Linux (`lower_case_table_names`).

## Verify
`CHECK TABLE shop.orders_restore;` returns OK, counts and spot-checked rows match the
backup point in time.

## Checked
2026-11-01. Confirmed against the MySQL 8.4 manual page Importing InnoDB Tables (prerequisites, FLUSH TABLES ... FOR EXPORT and .cfg behaviour, DISCARD/IMPORT PARTITION, limitations, usage notes) and the Percona XtraBackup 8.4 page Restore single tables between databases (`--prepare --export`, `--keyring-file-data`, `.cfp`). Removed: the 8.0.29 row-version claim, quoted error strings, keyring master-key and replication-of-IMPORT statements (not on these pages).
Method: documentation only; no commands were run.
