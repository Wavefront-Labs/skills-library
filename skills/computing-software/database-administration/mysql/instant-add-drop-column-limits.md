---
id: computing-software.database-administration.mysql.instant-add-drop-column-limits
name: instant-add-drop-column-limits
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, online-schema-change, algorithm-instant, instant-add-column, row-versions, innodb-online-ddl]
level: practitioner
status: verified
description: "Use ALGORITHM=INSTANT for ADD/DROP COLUMN in MySQL 8.0.29+ and know its limits: 64 row versions, unsupported table types, and when it silently cannot apply."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html#online-ddl-column-operations
  - https://dev.mysql.com/doc/refman/8.4/en/information-schema-innodb-tables-table.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# INSTANT ADD / DROP COLUMN limits

## What INSTANT does
Changes only data-dictionary metadata; no table rebuild, completes in milliseconds after
acquiring a brief exclusive metadata lock. Since 8.0.29 columns can be added **at any
position** (`ADD COLUMN note ... AFTER a, ALGORITHM=INSTANT` ran on 9.7.4) and dropped instantly; 8.0.12-8.0.28 allowed only adding as the last column.
INSTANT is the default algorithm when supported (the 9.7 manual says so; on 9.7.4 a plain `ADD COLUMN` on a table with rows raised `total_row_versions`, but on an EMPTY table the same plain statement reset it to 0, so test on a populated table).

```sql
ALTER TABLE orders ADD COLUMN source VARCHAR(32) NULL, ALGORITHM=INSTANT;
ALTER TABLE orders DROP COLUMN legacy_flag, ALGORITHM=INSTANT;
```
Always state `ALGORITHM=INSTANT`: if it cannot be done instantly the statement **fails**
instead of quietly falling back to a rebuild.

## The row-version limit: 64 in 8.4, 255 from 9.1.0
Each instant ADD/DROP creates a new row version. The manuals give a maximum of 64 for 8.4 and 255 as of 9.1.0; on 9.7.4 `total_row_versions` reached 255 and the next add was refused (70 add/drop operations on one table all succeeded). The heading's old figure of 64 applies to 8.4 and earlier 8.0 servers. After the limit, instant column
changes are refused:
```
ERROR 4092 (HY000): Maximum row versions reached for table shop/orders. No more columns can be added or dropped instantly. Please use COPY/INPLACE.
```
(Text confirmed on 9.7.4 with the table named `ddl/lim2`.)
```sql
SELECT name, total_row_versions FROM information_schema.innodb_tables
WHERE name = 'shop/orders';
```
A rebuild (`OPTIMIZE TABLE`, `ALTER TABLE ... FORCE`, or any INPLACE/COPY rebuild) resets the
counter to 0 (an `ALGORITHM=INPLACE` ADD COLUMN took 255 back to 0 on 9.7.4). Plan an online rebuild before the limit for your version (for example when it passes about 50 on 8.4, or about 200 on 9.1 and later).

## Not instant
- Tables with `ROW_FORMAT=COMPRESSED` (error 1845 on 9.7.4), FULLTEXT indexes (rejected once one existed), or in the data dictionary tablespace (per the 9.7 manual).
- Temporary tables (error 1845; only COPY works).
- Combined in one statement with an operation that is not instant (e.g. adding an index: rejected with 1845).
- Changing column type (INT to BIGINT rejected INSTANT, and INPLACE too), and any `VARCHAR` extension (it ran INPLACE, not INSTANT).
- Adding a STORED generated column (error 1845); a VIRTUAL one ran INSTANT.
- Adding a NOT NULL column with no default **is** instant (existing rows read as 0); changing an existing column to NOT NULL is not (INPLACE).

## Other instant operations
Set/drop column default, rename column, modify ENUM/SET by
appending values, rename table (each ran with `ALGORITHM=INSTANT` on 9.7.4 except as noted; the version in which column rename became instant and any conditions were not checked, see the manual's online DDL table). Dropping a secondary index runs INPLACE, not INSTANT.

## Gotchas
- Even INSTANT needs the metadata lock: a long transaction on the table blocks it and
  everything queues behind (`Waiting for table metadata lock`). Use `lock_wait_timeout` low
  and retry.
- Backups and tools: check your backup tool's release notes for support of tables with instantly added/dropped columns (not tested here), and keep it current.
- Replicas apply the ALTER instantly too (statement in binlog), as long as the replica
  version supports it.

## Verify
The ALTER returns in milliseconds with `ALGORITHM=INSTANT`, and `total_row_versions`
increments for the table.
