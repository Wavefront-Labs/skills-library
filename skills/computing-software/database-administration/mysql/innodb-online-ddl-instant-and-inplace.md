---
id: computing-software.database-administration.mysql.innodb-online-ddl-instant-and-inplace
name: innodb-online-ddl-instant-and-inplace
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, online-schema-change, innodb-online-ddl, algorithm-instant, algorithm-inplace, lock-none, innodb-online-alter-log-max-size, replica-lag]
level: advanced
status: verified
description: "Run ALTER TABLE in MySQL 8 with ALGORITHM=INSTANT or INPLACE, LOCK=NONE, know which operations qualify, and avoid replica lag and row-log overflow."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html
  - https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-performance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InnoDB online DDL

**Goal:** schema changes that do not block writes, chosen deliberately, with the
statement failing fast if MySQL cannot do it the way you asked.

## Always state the algorithm and lock
```sql
ALTER TABLE orders ADD COLUMN note VARCHAR(255) NULL, ALGORITHM=INSTANT;
ALTER TABLE orders ADD INDEX idx_created (created_at), ALGORITHM=INPLACE, LOCK=NONE;
```
If the operation cannot run that way, MySQL errors instead of silently falling
back to a blocking COPY: for example `ADD INDEX ..., ALGORITHM=INSTANT` gives `ERROR 1845 ALGORITHM=INSTANT is not supported for this operation`, `ADD FULLTEXT ..., LOCK=NONE` gives error 1846 "Fulltext index creation requires a lock. Try LOCK=SHARED", and `MODIFY a INT -> BIGINT, ALGORITHM=INPLACE` gives error 1846 "Cannot change column type INPLACE. Try ALGORITHM=COPY" (all run on 9.7.4).

## What qualifies (8.0.29+ / 8.4)
| Operation | Algorithm | Rebuild | Concurrent DML |
|---|---|---|---|
| Add column (any position, 8.0.29+) / drop column | INSTANT | no | yes |
| Rename column, set/drop DEFAULT, extend ENUM/SET at end | INSTANT | no | yes |
| Add/drop secondary index, rename index | INPLACE | no | yes |
| Increase VARCHAR within same length-byte (<=255 or >255 both sides) | INPLACE (instant-ish) | no | yes |
| Change column type, change NULL to NOT NULL, add PK, change charset | INPLACE rebuild or COPY (INT to BIGINT was COPY only; NULL to NOT NULL ran INPLACE, LOCK=NONE; both rejected INSTANT) | yes | often yes for INPLACE; COPY blocks writes |
| Add a NOT NULL column with no default | INSTANT (ran; existing rows read as 0) | no | yes |
| Add FULLTEXT/SPATIAL index | INPLACE | maybe | no (LOCK=SHARED) |
Instant ADD/DROP COLUMN has a limit on row versions per table: 64 in 8.4, **255 from 9.1.0** (manuals for 8.4 and 9.7; 9.7.4 refused the 256th with error 4092). After that a
rebuild (`OPTIMIZE TABLE`, `ALTER ... FORCE` or an INPLACE add, which reset it to 0 in a test) resets the counter
(`information_schema.innodb_tables.total_row_versions`).

## INPLACE mechanics and failure modes
- Concurrent DML during the build goes to an online row log capped by
  `innodb_online_alter_log_max_size` (128 MB default); exceeded =
  `ERROR 1799 Creating index '%s' required more than 'innodb_online_alter_log_max_size' bytes of modification log. Please try again.` (message from the server error reference; not reproduced here)
  and the ALTER rolls back. Raise it for busy tables. Default is 134217728 (128 MB, checked).
- A brief exclusive metadata lock is still needed at start and end: a long
  transaction on the table blocks the ALTER, and everything queues behind it
  (see metadata-lock skill). Reproduced on 9.7.4: with one session holding an open transaction that had read the table, an `ALTER ... ALGORITHM=INSTANT` and then a plain `SELECT` both sat in `Waiting for table metadata lock`, and an `ALTER ... INPLACE` with `SET lock_wait_timeout=1` failed with error 1205. Set `lock_wait_timeout` low in the DDL session.
- Replication: the ALTER is written to the binlog when it finishes on the source and is then applied on the replica, where a rebuild takes about as long again: a 2-hour rebuild can mean about 2 hours of replica lag (reasoning from how statement replication works; not measured here). For big rebuilds use gh-ost
  or pt-online-schema-change instead (neither was run here).
- Rebuilds need free disk of roughly the table size plus the row log and temp sort files (`innodb_tmpdir`).

## Verify
`ALTER` returns quickly for INSTANT; `SHOW CREATE TABLE` reflects the change;
`performance_schema.events_stages_current` shows progress
(`stage/innodb/alter table (read PK and internal sort)` exists in `setup_instruments`, enabled by default) for long INPLACE operations.
