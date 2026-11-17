---
id: computing-software.database-administration.postgresql.gin-indexes-for-jsonb-and-arrays
name: gin-indexes-for-jsonb-and-arrays
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, postgres-index-types, gin-index, jsonb-index, jsonb-path-ops, array-index, full-text-search, fastupdate, gin-pending-list]
level: advanced
status: verified
description: "Index jsonb, arrays and tsvector columns with GIN in PostgreSQL: pick jsonb_ops vs jsonb_path_ops, write queries that use it, and manage the pending list."
sources:
  - https://www.postgresql.org/docs/current/gin.html
  - https://www.postgresql.org/docs/current/datatype-json.html#JSON-INDEXING
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GIN indexes for jsonb and arrays

**Goal:** containment and key-existence queries on jsonb/array columns use an
index instead of scanning every row.

## Operator classes
```sql
CREATE INDEX ON events USING gin (payload);                  -- jsonb_ops: @>, ?, ?|, ?&, @?, @@
CREATE INDEX ON events USING gin (payload jsonb_path_ops);   -- only @>, @?, @@ ; smaller, faster
CREATE INDEX ON posts  USING gin (tags);                     -- arrays: @>, <@, &&, =
CREATE INDEX ON docs   USING gin (to_tsvector('english', body));
```
Prefer `jsonb_path_ops` unless you need key-existence (`?`) operators.

## Write queries the index can use
GIN supports **operators**, not arbitrary expressions:
```sql
-- uses the index
SELECT * FROM events WHERE payload @> '{"type":"signup","plan":"pro"}';
SELECT * FROM events WHERE payload @? '$.items[*] ? (@.sku == "A1")';
-- does NOT use a GIN index on payload
SELECT * FROM events WHERE payload->>'type' = 'signup';
```
For a single hot scalar key, a B-tree expression index is better:
`CREATE INDEX ON events ((payload->>'type'));`

## Write cost and the pending list
GIN inserts are expensive (one entry per key/element). With `fastupdate = on`
(default), new entries go to an unsorted pending list merged at vacuum or when
it exceeds `gin_pending_list_limit` (4MB default). Symptom: occasional single
inserts that take seconds (the one that triggered the merge), and slower
searches while the list is large. Options:
```sql
ALTER INDEX events_payload_idx SET (fastupdate = off);       -- steady insert cost
ALTER INDEX events_payload_idx SET (gin_pending_list_limit = 512);  -- smaller merges (kB)
SELECT gin_clean_pending_list('events_payload_idx');
```

## Gotchas
- GIN cannot do ordering or range scans; it returns a bitmap, so plans show
  `Bitmap Index Scan` + `Bitmap Heap Scan` with a recheck.
- Very common keys/values (present in most rows) make the index useless and
  large; the planner will (correctly) seq scan.
- Build time is long; raise `maintenance_work_mem` for the build, and use
  `CREATE INDEX CONCURRENTLY` on live tables.

## Verify
`EXPLAIN (ANALYZE, BUFFERS)` shows `Bitmap Index Scan on events_payload_idx`;
`pg_relation_size` of the index vs table is reasonable (path_ops typically much smaller).

## Checked
- PostgreSQL 17.6 with 200,000 rows: `jsonb_path_ops` index 1664 kB versus 2560 kB for `jsonb_ops`; `@>`, `@?`, `@@` use either, `?` only works with `jsonb_ops` (seq scan with just path_ops), `payload->>'type' = ...` never uses GIN; array `@>`, `<@`, `&&` and `=` use the GIN index; `fastupdate` and `gin_pending_list_limit` reloptions set as written, `gin_clean_pending_list()` returns a count, default limit 4MB. Insert-time stalls from pending-list merges were not measured.
