---
id: computing-software.database-administration.schema-design.json-columns-vs-relational-columns
name: json-columns-vs-relational-columns
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, data-type-selection, json-columns, jsonb, semi-structured-data, generated-columns, json-schema-validation, hybrid-schema]
level: advanced
status: verified
description: "Decide what goes in JSON/JSONB columns versus real columns in a relational schema, and keep JSON data queryable and valid with generated columns, indexes and check constraints."
sources:
  - https://www.postgresql.org/docs/current/datatype-json.html
  - https://dev.mysql.com/doc/refman/8.4/en/json.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/json/json-data-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON columns vs relational columns

**Goal:** use JSON for genuinely variable data without turning the database into
an untyped blob store.

## Put in real columns
- Anything filtered, joined, sorted or aggregated regularly.
- Anything with integrity rules: foreign keys, uniqueness, NOT NULL, ranges.
- Money, timestamps, status/enums, identifiers.
Columns get statistics, constraints, compact storage and clear types.

## JSON is right for
- Payloads you store and return whole (webhook bodies, API responses, audit snapshots).
- Sparse, variable attributes (product specs that differ per category) that
  would otherwise be dozens of mostly-NULL columns or EAV.
- Schema-on-read data from external systems you don't control.

## Keep JSON healthy
```sql
-- PostgreSQL: binary jsonb, validate shape, index access paths
CREATE TABLE products (
  id bigint PRIMARY KEY, category text NOT NULL, price numeric(12,2) NOT NULL,
  attrs jsonb NOT NULL DEFAULT '{}',
  CHECK (jsonb_typeof(attrs) = 'object'),
  brand text GENERATED ALWAYS AS (attrs->>'brand') STORED      -- promote a hot key
);
CREATE INDEX ON products (brand);
CREATE INDEX ON products USING gin (attrs jsonb_path_ops);
```
- MySQL 8: `JSON` type (validated), a generated column + index for hot keys (see the CREATE INDEX manual for functional-index syntax); `JSON_SCHEMA_VALID()` (added in 8.0.17, JSON Schema Draft 4) usable in a CHECK constraint.
- SQL Server: native `json` type in SQL Server 2025, Azure SQL Database and Azure SQL Managed Instance (it cannot be an index key column; JSON indexes exist there); on older versions `nvarchar(max)` + `ISJSON`, with a computed column over `JSON_VALUE` for indexing (not run here).
- When a JSON key becomes important, promote it to a column (generated first,
  then a real column via migration).

## Gotchas
- PostgreSQL `json` (text) keeps formatting and duplicate keys (`'{"a":1,"a":2}'::json::text` returns both) and reparses each access; `jsonb` keeps the last duplicate; use `jsonb`.
- Updating one key rewrites the whole document (large JSON rows → write amplification, TOAST churn).
- Planner has no statistics inside JSON values (except via expression indexes/extended stats): misestimates.
- Type drift: `"price": "12.50"` vs `12.5` in different rows; validate at write.

## Verify
Top queries (pg_stat_statements / digest tables) don't filter on unindexed JSON
paths; constraints reject malformed documents in a test insert.
