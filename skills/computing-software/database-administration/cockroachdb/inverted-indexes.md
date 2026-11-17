---
id: computing-software.database-administration.cockroachdb.inverted-indexes
name: inverted-indexes
category: computing-software
field: database-administration
product: cockroachdb
tags: [inverted-indexes, gin-indexes, jsonb, array-containment, create-inverted-index]
level: practitioner
status: docs-checked
description: "Create and use CockroachDB inverted (GIN) indexes for JSONB, ARRAY, spatial, TSVECTOR and trigram columns, including containment queries and partial or multi-column GIN."
sources:
  - https://www.cockroachlabs.com/docs/stable/inverted-indexes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: speed up containment and membership searches inside container values.

GIN indexes in CockroachDB store the contents of: `JSONB`, `ARRAY`, spatial (`GEOMETRY`, `GEOGRAPHY`), `TSVECTOR` (full-text search) and `STRING` (trigram indexes). A normal index cannot answer queries like "rows whose JSON contains X" without a full table scan; GIN tokenizes JSONB objects (key-value pairs) and arrays (each element).

Create (PostgreSQL syntax or CockroachDB syntax at table creation):
```sql
CREATE INDEX {optional name} ON {table} USING GIN ({column});
CREATE INDEX {optional name} ON {table} USING GIN ({column} {opclass});
CREATE INVERTED INDEX {optional name} ON {table} ({column});
```
Partial GIN indexes are supported: `INVERTED INDEX idx_data(data) WHERE id > 10`. A multi-column inverted index can lead with ordinary columns, for example `INVERTED INDEX (user_type, user_profile)`.

Queries that use it include containment with `@>`:
```sql
SELECT * FROM users WHERE user_profile @> '{"location":"NYC"}';
```
The page also lists other supported JSONB and array operators.

Index selection: if the optimizer does not choose the index, you can force it with an index hint (the page links to Index Selection in CockroachDB for the syntax).

Gotchas: indexes slightly slow writes because new values have to be copied and sorted; on `REGIONAL BY ROW` tables an added index is automatically partitioned on the region column, and creating or modifying an index errors while a region add or drop runs on that database.

Verify: use `EXPLAIN` on the query and confirm the plan uses the inverted index rather than a full scan.

## Checked
2026-11-03. Confirmed on the inverted indexes page: GIN covers JSONB, ARRAY, spatial types, TSVECTOR and trigram STRING indexes, tokenizing, both create syntaxes, partial GIN example, multi-column example, `@>` query, index hint to override selection, write cost and REGIONAL BY ROW behaviour. Removed: the `table@index_name` form and the larger-index claim.
Method: documentation only; no commands were run.
