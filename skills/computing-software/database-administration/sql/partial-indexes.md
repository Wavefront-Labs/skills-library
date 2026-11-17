---
id: computing-software.database-administration.sql.partial-indexes
name: partial-indexes
category: computing-software
field: database-administration
product: sql
tags: [sql, partial-indexes]
level: practitioner
status: docs-checked
description: "Index only the rows queries need with a WHERE clause."
sources: ["https://www.postgresql.org/docs/current/indexes-partial.html", "https://www.sqlite.org/partialindex.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial indexes

- `CREATE INDEX ON orders (cid) WHERE status = 'open';` (PostgreSQL, SQLite).
- A query can use it only if its WHERE condition implies the index predicate; PostgreSQL recognises only simple implications, otherwise the predicate must match part of the query's WHERE condition.
- Unique partial: `CREATE UNIQUE INDEX ON users (email) WHERE deleted_at IS NULL;` for soft deletes.
- Parameterized query clauses do not work with a partial index in PostgreSQL (matching happens at planning time); SQLite's index WHERE may not contain bound parameters, subqueries or non-deterministic functions.
- Self-check: compare index size and plan with and without.

## Checked

2026-11-02. Confirmed in the PostgreSQL partial indexes page and the SQLite partial indexes page: implication rule, parameterized clauses, SQLite WHERE restrictions. Removed: the 'faster to maintain' claim.
Method: documentation only; no commands were run.
