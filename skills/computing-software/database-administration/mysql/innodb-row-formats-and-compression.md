---
id: computing-software.database-administration.mysql.innodb-row-formats-and-compression
name: innodb-row-formats-and-compression
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, row-format, innodb-compression, dynamic-row-format, compressed-row-format, page-compression, key-block-size, mysql-storage]
level: practitioner
status: verified
description: "Choose InnoDB row formats (DYNAMIC, COMPACT, COMPRESSED, REDUNDANT), handle row size limits, and decide between table compression and page compression."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-row-format.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-compression.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-page-compression.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Row formats and table compression

## Row formats
| Format | Notes |
|---|---|
| `DYNAMIC` | default (`innodb_default_row_format = dynamic`, checked on 9.7.4); long variable-length columns stored fully off-page with a 20-byte pointer; index prefixes up to 3072 bytes |
| `COMPACT` | stores 768-byte prefix of long columns inline; prefix limit 767 bytes |
| `REDUNDANT` | oldest; avoid |
| `COMPRESSED` | DYNAMIC + zlib-compressed pages (`KEY_BLOCK_SIZE`) |

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, ROW_FORMAT, CREATE_OPTIONS FROM information_schema.TABLES WHERE ENGINE='InnoDB' AND ROW_FORMAT <> 'Dynamic';
ALTER TABLE legacy ROW_FORMAT=DYNAMIC, ALGORITHM=INPLACE, LOCK=NONE;   -- rebuild
```
`innodb_default_row_format` sets the default for new tables.

## Row size errors
`Row size too large (> 8126)` on CREATE/ALTER or INSERT (reproduced on 9.7.4: a `ROW_FORMAT=COMPACT` table with 26 `VARCHAR(255)` utf8mb4 columns failed at CREATE with error 1118 "... In current row format, BLOB prefix of 768 bytes is stored inline", while the identical `ROW_FORMAT=DYNAMIC` table was created): the inline part of all columns must fit in about half a 16 KB page. Fixes: DYNAMIC format (moves long columns fully off-page), change many `VARCHAR(255)` utf8mb4 columns to TEXT, or normalise. `innodb_strict_mode = ON` (default) reports at DDL time instead of failing on a future INSERT.

## Table compression (ROW_FORMAT=COMPRESSED)
```sql
ALTER TABLE logs ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
```
On 9.7.4 this worked on a 20,000-row table (`row_format=COMPRESSED KEY_BLOCK_SIZE=8` in `CREATE_OPTIONS`) and `INNODB_CMP` then showed the 8192 row with `compress_ops = compress_ops_ok = 443`. Going back needs `ALTER TABLE logs ROW_FORMAT=DYNAMIC, KEY_BLOCK_SIZE=0`; `ROW_FORMAT=DYNAMIC` alone failed with `ERROR 1478 ... does not support the create option 'KEY_BLOCK_SIZE'`.
- Pages stored compressed (8 KB on disk for a 16 KB page). Buffer pool may hold both compressed and uncompressed copies: more CPU and memory overhead.
- Watch `information_schema.INNODB_CMP`: the manual says a high `compress_ops_ok / compress_ops` ratio means the system is performing well, and a low ratio means MySQL is reorganising, recompressing and splitting B-tree nodes too often (it gives no percentage); then try a larger KEY_BLOCK_SIZE or stop compressing that table.
- Good for read-mostly, compressible data (text, JSON); poor for already-compressed blobs and hot OLTP tables.

## Page compression (transparent, hole punching)
```sql
CREATE TABLE logs (...) COMPRESSION='lz4';     -- 'zlib' or 'lz4' (and 'none'); needs sparse file and hole punching support
ALTER TABLE logs COMPRESSION='zlib'; OPTIMIZE TABLE logs;   -- existing pages compress only when rewritten
```
**`zstd` is not a valid page-compression algorithm**: the manual lists Zlib and LZ4, and `CREATE TABLE ... COMPRESSION='zstd'` failed on 9.7.4 with `ERROR 1031 Table storage engine ... doesn't have this option` (the same error for an arbitrary name). The manual lists Windows with NTFS and several Linux platforms as supported; on this test machine's scratch drive `COMPRESSION='lz4'` failed with `ERROR 4029 Punch hole not supported by the filesystem or the tablespace page size is not large enough`, so check the filesystem first; the space-saving behaviour was not measured here.
The manual presents it as page-level compression that depends on sparse files and hole punching. On Linux, `ls -l` then reports the apparent size and `du` the real usage, and copying with a tool that does not preserve sparse files inflates them (general sparse-file behaviour; not run here because hole punching failed on this host).

## Gotchas
- Changing row format rebuilds the table (online; `ALTER ... ROW_FORMAT=DYNAMIC, KEY_BLOCK_SIZE=0, ALGORITHM=INPLACE, LOCK=NONE` was accepted on 9.7.4); `ALTER ... COMPRESSION` only changes the attribute until `OPTIMIZE TABLE` rewrites the pages (manual).
- Backups: check your backup tool's documentation for page-compressed tables; files restored onto a filesystem without hole punching may use their full size (not tested here).
- Compression in the application (compress JSON before storing) often beats both.
