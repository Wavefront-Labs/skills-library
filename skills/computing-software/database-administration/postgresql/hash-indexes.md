---
id: computing-software.database-administration.postgresql.hash-indexes
name: hash-indexes
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, hash-index, index-types, equality-lookups, wal-logged]
level: practitioner
status: verified
description: "Know when a PostgreSQL hash index beats B-tree (large keys, equality only), its limits (no uniqueness, ranges or sorting), and how to compare sizes."
sources:
  - https://www.postgresql.org/docs/current/hash-index.html
  - https://www.postgresql.org/docs/current/indexes-types.html#INDEXES-TYPES-HASH
  - https://www.postgresql.org/docs/current/sql-createindex.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash indexes

Since PG10 hash indexes are WAL-logged, crash-safe and replicated. Before PG10, never use them.

## What they do
Store a 32-bit hash of the key per entry, so index size does not depend on key width. They support only `=`.

```sql
CREATE INDEX sessions_token_hash ON sessions USING hash (token);
EXPLAIN SELECT * FROM sessions WHERE token = 'f3a9...';   -- Index Scan using sessions_token_hash
```

## When they win
- Long keys looked up by equality only: URLs, tokens, SHA-256 hex strings, long text IDs. A B-tree stores the full key; hash stores 4 bytes + TID.
- Very high-cardinality columns where you never range-scan.

Compare before committing:
```sql
CREATE INDEX CONCURRENTLY t_btree ON t (url);
CREATE INDEX CONCURRENTLY t_hash  ON t USING hash (url);
SELECT indexrelname, pg_size_pretty(pg_relation_size(indexrelid)) FROM pg_stat_user_indexes WHERE relname = 't';
```
Then benchmark the lookup, keep one, drop the other.

## Limits
- No `UNIQUE`, no primary keys, no multi-column, no `INCLUDE`.
- No `<`, `>`, `BETWEEN`, `LIKE 'x%'`, `ORDER BY`.
- No index-only scans (the key value is not stored).
- Heavily duplicated values make bucket overflow chains long: bad for low-cardinality columns.
- B-tree deduplication (PG13+) has narrowed the size advantage for repeated values; the gain is mainly with long unique-ish keys.

## Alternative pattern
For uniqueness on a long key, a B-tree unique index on `md5(url)` or a generated `sha256` bytea column keeps both uniqueness and a small index.

## Gotchas
- Hash indexes build slowly on big tables; set `maintenance_work_mem` high for the build.
- They grow by splitting buckets and do not shrink; REINDEX after mass deletes.

## Checked
- PostgreSQL 17.6, 200,000 rows with long keys: hash index 6.5 MB versus 27 MB B-tree on a 100+ character URL; equality uses the hash index; `UNIQUE`, multi-column, `INCLUDE` and primary-key use are rejected with the quoted errors; `<` and `LIKE 'x%'` fall back to a sequential scan; `SELECT url ... WHERE url = ...` shows Index Scan (no index-only scan); a unique B-tree on `md5(url)` builds. PG10 release notes add WAL logging for hash indexes and PG13 notes B-tree duplicate storage. Bucket-overflow behaviour with heavily duplicated values was not measured.
