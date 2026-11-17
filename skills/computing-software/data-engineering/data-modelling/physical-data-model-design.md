---
id: computing-software.data-engineering.data-modelling.physical-data-model-design
name: physical-data-model-design
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, physical-data-model, indexes, constraints, data-types]
level: advanced
status: docs-checked
description: "Turn a logical model into a physical design: Postgres data types and indexes, and how Snowflake constraints differ between standard and hybrid tables."
sources:
  - https://www.postgresql.org/docs/current/datatype-numeric.html
  - https://www.postgresql.org/docs/current/datatype-datetime.html
  - https://www.postgresql.org/docs/current/indexes.html
  - https://www.postgresql.org/docs/current/indexes-multicolumn.html
  - https://www.postgresql.org/docs/current/indexes-partial.html
  - https://www.postgresql.org/docs/current/indexes-index-only-scans.html
  - https://docs.snowflake.com/en/sql-reference/constraints-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Physical data model design

**Goal:** a schema that stores data correctly, enforces what it can, and performs for the expected access patterns.

## Data types (PostgreSQL)
- Money and other exact quantities: `numeric`, which the manual recommends for monetary amounts; `real` and `double precision` are inexact (approximations, equality comparisons may surprise). numeric is much slower than integer or float types. Declared precision and scale are maximums, not allocations; excess scale is rounded and excess integer digits raise an error.
- Timestamps: plain `timestamp` means `timestamp without time zone` (SQL standard); `timestamptz` abbreviates `timestamp with time zone`. A literal with a zone offset is still treated as without time zone unless given an explicit type. The manual calls `time with time zone` of questionable usefulness.
- Choose key and code types by the data, not appearance (the pages give no rule for identifiers or booleans).

## Keys and constraints (Snowflake)
| Constraint | Snowflake standard table | Snowflake hybrid table |
|---|---|---|
| PRIMARY KEY | optional, not enforced | required, enforced |
| FOREIGN KEY | optional, not enforced | optional, enforced |
| UNIQUE | optional, not enforced | optional, enforced |
| NOT NULL | optional, enforced | optional, enforced |
| CHECK | optional, enforced | optional, enforced; only at table creation |
- Snowflake does not enforce PK, UNIQUE and FK on standard tables because checking them on very large distributed columnar tables would slow loads and DML. They still serve as metadata: DDL migration, BI and modelling tools discover keys and relationships, and people see how tables relate.
- `RELY` on a constraint lets the optimizer use it for join elimination; set it only if you have ensured the data complies.
- CHECK constraints in Snowflake: a failing record fails the whole batch; COPY INTO and pipes targeting such tables fail; the expression cannot be changed (drop and recreate).
- Enforce the unenforced keys with pipeline tests. Other warehouses are not covered by the cited pages.

## Indexes (PostgreSQL)
- Indexes speed retrieval but add overhead, so use them sensibly.
- Multicolumn B-tree: equality constraints on leading columns plus an inequality on the first column without equality limit the scanned portion; the index is most efficient with constraints on the leftmost columns. Max 32 columns including INCLUDE columns.
- Partial indexes cover a subset defined by a predicate; useful to avoid indexing common values, which shrinks the index and reduces update work.
- Covering indexes: `CREATE INDEX tab_x_y ON tab(x) INCLUDE (y);` allows index-only scans for queries touching only indexed columns; for a unique index the uniqueness applies only to the key columns.

## Verify
`EXPLAIN` of the top queries uses the intended indexes; constraint tests pass on loaded data.

## Checked
Method: docs-only read on 2026-11-09 via text extraction of the cited Postgres numeric, datetime, multicolumn, partial and index-only-scan pages (targeted sections of each; the datatype and indexes chapter pages are only tables of contents, so datatype.html was replaced by the numeric and datetime pages) and the full Snowflake constraints overview. Removed as unstated: scale guidance for currency/FX, UTC storage convention, BIGINT/UUID advice, string length and boolean advice, the warehouse comparison for BigQuery and Redshift, composite-index "equality then range" shorthand beyond the documented rule, pg_stat_user_indexes idx_scan, warehouse layout and naming sections.
