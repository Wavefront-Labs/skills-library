---
id: computing-software.database-administration.mysql.innodb-tablespaces-and-reclaiming-space
name: innodb-tablespaces-and-reclaiming-space
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, innodb, innodb-file-per-table, optimize-table, general-tablespace, ibdata1, disk-space, fragmentation]
level: practitioner
status: docs-checked
description: "Reclaim disk space in MySQL InnoDB after big deletes with OPTIMIZE TABLE (online rebuild), and know when it is worth it and what replicates."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-tablespace.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-file-defragmenting.html
  - https://dev.mysql.com/doc/refman/8.4/en/optimize-table.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InnoDB tablespaces and reclaiming space

## When OPTIMIZE TABLE helps
After substantial insert, update or delete activity on an InnoDB table that has its own `.ibd`
file (`innodb_file_per_table` enabled), `OPTIMIZE TABLE` reorganizes the table and indexes and
disk space can be returned to the operating system. InnoDB allocates pages and does not
fragment like MyISAM; some fragmentation is expected, and deletes can leave sparsely filled
pages that make a rebuild worthwhile. It does not work on views.

## Measure
```sql
SELECT table_schema, table_name,
       round(data_length/1024/1024)  AS data_mb,
       round(index_length/1024/1024) AS index_mb,
       round(data_free/1024/1024)    AS free_mb
FROM information_schema.tables
WHERE engine = 'InnoDB' ORDER BY data_free DESC LIMIT 20;
```
Compare with the `.ibd` size on disk; `data_free` is an estimate.

## Rebuild
```sql
OPTIMIZE TABLE shop.events;
```
- For InnoDB it is mapped to `ALTER TABLE ... FORCE`: the table is rebuilt in place to update index
  statistics and free unused space in the clustered index (output shows "doing recreate + analyze").
- It uses online DDL: concurrent DML continues; an exclusive lock is taken only briefly in the
  prepare and commit phases.
- The table copy method is used instead when `old_alter_table` is enabled, when the server runs with
  `--skip-new`, or when the table has FULLTEXT indexes.
- It is written to the binary log and replicates by default; `NO_WRITE_TO_BINLOG` (alias `LOCAL`,
  needs the `OPTIMIZE_LOCAL_TABLE` privilege) suppresses that. Plan for replica lag on big tables.
- Needs `SELECT` and `INSERT` privileges on the table.
- For FULLTEXT-heavy tables set `innodb_optimize_fulltext_only=1` and use
  `innodb_ft_num_word_optimize` to bound each pass.

## Verify
After the rebuild the `.ibd` file is smaller, `data_free` drops, and replica lag is back to normal.

## Checked
2026-11-01. Confirmed against the MySQL 8.4 manual page OPTIMIZE TABLE Statement (InnoDB mapping to ALTER TABLE ... FORCE, online DDL, copy-method conditions, FULLTEXT, binary logging, privileges) and Defragmenting a Table. Removed: the tablespace-type table (system, general, undo, temporary file names), ibdata1 shrink advice, moving-tablespace statements, innodb_online_alter_log_max_size and gh-ost advice (not confirmed on the fetched pages).
Method: documentation only; no commands were run.
