---
id: computing-software.database-administration.schema-design.array-columns-vs-child-tables
name: array-columns-vs-child-tables
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, array-columns, child-tables, postgres-arrays, one-to-many, data-types]
level: practitioner
status: verified
description: "Decide between array columns (PostgreSQL arrays, JSON arrays) and child tables for multi-valued attributes, covering integrity, indexing with GIN, updates and query patterns."
sources:
  - https://www.postgresql.org/docs/current/arrays.html
  - https://www.postgresql.org/docs/current/gin.html
  - https://www.postgresql.org/docs/current/functions-array.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array columns vs child tables

## Arrays (PostgreSQL)
```sql
CREATE TABLE articles (id bigint PRIMARY KEY, title text, tags text[] NOT NULL DEFAULT '{}');
CREATE INDEX ON articles USING gin (tags);
SELECT * FROM articles WHERE tags @> ARRAY['postgres'];          -- contains (uses GIN)
SELECT * FROM articles WHERE tags && ARRAY['mysql','sqlite'];    -- overlaps (uses GIN)
SELECT * FROM articles WHERE 'postgres' = ANY(tags);              -- does NOT use the GIN index
UPDATE articles SET tags = array_append(tags, 'new') WHERE id = 1;
```

## Child table
```sql
CREATE TABLE article_tags (article_id bigint REFERENCES articles ON DELETE CASCADE, tag_id int REFERENCES tags,
  PRIMARY KEY (article_id, tag_id));
CREATE INDEX ON article_tags (tag_id);
```

## Decision table
| Criterion | Array | Child table |
|---|---|---|
| Referential integrity of elements | No FK on elements | FKs enforce valid values |
| Element attributes (added_by, added_at, order) | Awkward | Natural |
| Queries "items with X" | GIN `@>` fast | Index on child column |
| Counting/aggregating per element across rows | `unnest` + group | Direct GROUP BY |
| Updating one element under concurrency | Rewrites whole row; lost-update risk | Row-level insert/delete |
| Unbounded growth (thousands of elements) | Row bloat, TOAST, slow updates | Scales |
| Ordered small lists read with the parent | Excellent (one fetch) | Join |
| Portability | PostgreSQL (and JSON arrays elsewhere) | Everywhere |

Rule of thumb: arrays for small, bounded, value-only lists that are read and written with the parent (tags snapshot, ordered list of preferred contact methods); child tables when elements are entities, need integrity, have their own attributes, or grow large.

## JSON arrays in other engines
MySQL JSON arrays with multi-valued indexes (added in 8.0.17; the manual's example is `INDEX zips ((CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))`, queried with `MEMBER OF()`, `JSON_CONTAINS()` or `JSON_OVERLAPS()`; character arrays are limited to utf8mb4 with `utf8mb4_0900_as_cs`, or binary). For SQL Server, shred arrays with `OPENJSON` or use a child table; check its docs for index options. Comma-separated strings are never the answer (jaywalking).

## Gotchas
- Array equality is order-sensitive (`'{a,b}' <> '{b,a}'`); sort elements on write if sets.
- Arrays are 1-based (`(ARRAY[1,2,3])[0]` is NULL); multidimensional arrays must be rectangular (`'{{1,2},{3}}'::int[]` raises `malformed array literal`).
- `NULL` vs empty array: default `'{}'` and NOT NULL.

## Verify
EXPLAIN for the main "contains" query shows `Bitmap Index Scan` on the GIN index (checked on PostgreSQL 18 with 20,000 rows after ANALYZE: `@>` and `&&` use it, `= ANY(tags)` is a Seq Scan); for child table design, the FK and indexes exist and integrity tests reject unknown tags.
