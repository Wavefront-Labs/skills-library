---
id: computing-software.database-administration.query-optimisation.indexing-null-and-is-null-queries
name: indexing-null-and-is-null-queries
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, index-null, is-null, partial-index, indexing, null-handling]
level: practitioner
status: draft
description: "Make IS NULL and IS NOT NULL queries use indexes across engines: B-tree NULL handling, Oracle's missing NULL entries, partial/filtered indexes and NULLS FIRST/LAST order."
sources:
  - https://use-the-index-luke.com/sql/where-clause/null
  - https://www.postgresql.org/docs/current/indexes-partial.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/indexes/create-filtered-indexes
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Indexing NULL and IS NULL queries

## Engine behaviour
| Engine | NULLs in B-tree index? | `WHERE col IS NULL` can use index? |
|---|---|---|
| PostgreSQL | Yes | Yes |
| MySQL InnoDB | Yes | Yes (`ref_or_null` for `col = x OR col IS NULL`) |
| SQL Server | Yes | Yes |
| SQLite | Yes | Yes |
| Oracle | **No** entry if all indexed columns are NULL | Not with a single-column index |

## Oracle workaround
Add a non-null column or constant to the index so every row has an entry:
```sql
CREATE INDEX orders_shipped_ix ON orders (shipped_at, 0);    -- or (shipped_at, id)
SELECT * FROM orders WHERE shipped_at IS NULL;               -- can now range scan
```
Or a function-based index on `CASE WHEN shipped_at IS NULL THEN 1 END` (indexes only the NULL rows, tiny).

## "Queue" pattern: few NULL rows among many
`WHERE processed_at IS NULL` on a table where 99.9% are processed:
```sql
-- PostgreSQL / SQLite
CREATE INDEX ON events (created_at) WHERE processed_at IS NULL;
-- SQL Server
CREATE INDEX ix_events_pending ON dbo.events (created_at) WHERE processed_at IS NULL;
```
Small, hot index; the query must repeat the predicate literally. SQL Server filtered indexes need matching SET options and can be skipped with parameterised predicates.

## IS NOT NULL
Usually returns most rows → table scan is correct. Partial index `WHERE col IS NOT NULL` helps when non-NULL values are rare (sparse optional column).

## NULLs and ordering
Index order of NULLs matters for `ORDER BY col DESC NULLS LAST LIMIT 10`: PostgreSQL B-trees default `NULLS LAST` ascending (`NULLS FIRST` descending); create `CREATE INDEX ON t (col DESC NULLS LAST)` to match the query so the index provides the order.

## Design note
Many NULL-heavy columns indicate a sparse attribute: consider a separate table, or a status enum instead of nullable timestamps if queries filter by state.

## Verify
`EXPLAIN` for `WHERE processed_at IS NULL` shows the partial/filtered index; index size (`pg_relation_size`) is small relative to the table.
