---
id: computing-software.database-administration.query-optimisation.keyset-pagination
name: keyset-pagination
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, sql, query-anti-patterns, keyset-pagination, seek-method, offset-pagination, cursor-pagination, row-value-comparison, infinite-scroll]
level: practitioner
status: gated
description: "Replace slow LIMIT/OFFSET paging with keyset (seek) pagination using a unique sort key and row-value comparison, with the index it needs and its trade-offs."
sources:
  - https://use-the-index-luke.com/no-offset
  - https://use-the-index-luke.com/sql/partial-results/fetch-next-page
  - https://www.postgresql.org/docs/16/functions-comparisons.html#ROW-WISE-COMPARISON
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyset pagination

**Goal:** page 10,000 of a feed is as fast as page 1, and rows don't repeat or
vanish while users page through changing data.

## Why OFFSET is slow
`ORDER BY created_at DESC LIMIT 20 OFFSET 200000` must produce and discard
200,000 rows first: cost grows linearly with page number. Concurrent inserts also
shift rows between pages (duplicates/skips).

## Seek instead
Remember the last row of the current page and ask for rows after it. The sort
key must be **unique**: add the PK as a tie-breaker.
```sql
-- first page
SELECT id, created_at, title FROM posts
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- next page: pass last row's (created_at, id)
SELECT id, created_at, title FROM posts
WHERE (created_at, id) < ('2026-10-16 09:12:00', 98231)     -- row-value comparison
ORDER BY created_at DESC, id DESC
LIMIT 20;
```
Index exactly matching the order: `CREATE INDEX ON posts (created_at DESC, id DESC);`
(or ascending; B-trees scan both ways).

Row-value comparison works in PostgreSQL (run on 16.4) and SQLite (run on 3.50.4), and in MySQL 8, Oracle 23ai (gated: unconfirmed, source is paywalled or blocked); SQL Server
lacks it (gated: unconfirmed, source is paywalled or blocked), so expand it:
```sql
WHERE created_at < @ts OR (created_at = @ts AND id < @id)
```
(In PostgreSQL 16.4 the row-value form showed `Index Cond: (ROW(created_at, id) < ROW(...))`, while the expanded OR form showed only a `Filter` on an index-only scan, so it read the index from the top instead of seeking; prefer the row-value form on PostgreSQL. MySQL may not use the index well for the row-value form in older versions; check EXPLAIN and use the expanded form if needed.)

With filters, put equality filters first in the index: `(tenant_id, created_at, id)`.

## API shape
Return an opaque cursor (base64 of the last sort values) instead of page numbers.

## Trade-offs
- No "jump to page 57"; fine for feeds/infinite scroll/exports, not for numbered pagers (cap OFFSET depth there).
- Sorting by a non-unique column without a tie-breaker loses or repeats rows at page boundaries.
- Changing sort order means a different cursor and index.

## Verify
`EXPLAIN (ANALYZE)` for a deep cursor shows an index scan reading ~20 rows, and
timing is flat across page depth.
