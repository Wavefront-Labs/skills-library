---
id: computing-software.database-administration.sqlite.partial-and-expression-indexes-in-sqlite
name: partial-and-expression-indexes-in-sqlite
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-partial-index, expression-index, sqlite-indexes, sqlite-schema]
level: practitioner
status: verified
description: "Create SQLite partial indexes (WHERE clause) and indexes on expressions, with the exact query-matching rules the planner needs to use them."
sources:
  - https://sqlite.org/partialindex.html
  - https://sqlite.org/expridx.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial indexes and indexes on expressions

## Partial index
```sql
CREATE INDEX idx_jobs_pending ON jobs(run_at) WHERE status = 'pending';
CREATE UNIQUE INDEX uq_users_email_active ON users(email) WHERE deleted_at IS NULL;
```
Small index over the rows you query; the unique version enforces uniqueness only among active rows.

**Matching rule:** the planner uses the index only if the query's WHERE clause implies the index's WHERE clause, using simple logic:
- Terms must match exactly (`status = 'pending'` in both), or the index term is `col IS NOT NULL` and the query constrains `col` with a comparison.
- The documented rules (partialindex.html) are only the two above. `status = ?` is not literally `status = 'pending'`, yet on 3.50.4 and 3.54.1 the planner did use the index when the value was bound before the statement first ran (it re-prepares with the bound value), and `status = 'PENDING'` or `x IS NULL` against an `x IS NOT NULL` index gave `SCAN`. Do not depend on the bound-value case: write the literal in the query when the index must be used.
- The index's own WHERE clause may not contain bound parameters, subqueries, other tables or non-deterministic functions (`parameters prohibited in partial index WHERE clauses`).

## Index on expression (3.9.0+, release log: "Added support for indexes on expressions")
```sql
CREATE INDEX idx_users_lower_email ON users(lower(email));
SELECT * FROM users WHERE lower(email) = lower(?);
CREATE INDEX idx_events_type ON events(json_extract(payload, '$.type'));
SELECT count(*) FROM events WHERE json_extract(payload, '$.type') = 'click';
```
**Matching rule:** the query expression must match the index expression (same function, same arguments); `LOWER(email)`, `lower(email)` and `lower( email )` all used the `lower(email)` index in a test, but `email COLLATE NOCASE` did not (`SCAN`). A `json_extract(payload,'$.type')` index is not used by `payload ->> '$.type'` (`SCAN`): write the query in the indexed form.

Deterministic functions only: `create index ... (random())` failed with `non-deterministic functions prohibited in index expressions` and `datetime('now')` with `non-deterministic use of datetime() in an index`.

## Alternatives
- Case-insensitive lookups: `COLLATE NOCASE` on the column or index may be simpler than `lower()`.
- Generated columns (`GENERATED ALWAYS AS (json_extract(...)) VIRTUAL`) + normal index: clearer, the column can be referenced by name.

## Verify
```sql
EXPLAIN QUERY PLAN SELECT * FROM jobs WHERE status='pending' AND run_at < ?;
-- SEARCH jobs USING INDEX idx_jobs_pending (run_at<?)
```
If it shows `SCAN`, compare the WHERE clause to the index definition text.
