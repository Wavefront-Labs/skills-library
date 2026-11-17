---
id: computing-software.database-administration.schema-design.random-row-selection
name: random-row-selection
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, random-selection, order-by-random, tablesample, sampling, schema-patterns]
level: practitioner
status: verified
description: "Select random rows efficiently instead of ORDER BY RANDOM(): random id probing, TABLESAMPLE, precomputed random columns and reservoir sampling, with bias trade-offs."
sources:
  - https://pragprog.com/titles/bksap1/sql-antipatterns-volume-1/
  - https://www.postgresql.org/docs/current/sql-select.html#SQL-FROM
  - https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql#tablesample-clause
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Random row selection

## The antipattern
```sql
SELECT * FROM products ORDER BY random() LIMIT 1;      -- other engines: their random function
```
Generates a random value for every row and sorts the whole table: O(n log n) per request. Fine for thousands of rows, terrible for millions.

## Options
**1. Random id probe (dense integer keys)**
```sql
SELECT * FROM products
WHERE id >= (SELECT floor(random() * (SELECT max(id) FROM products))::bigint)
ORDER BY id LIMIT 1;
```
One index seek. Biased when ids have gaps (rows after big gaps are picked more often); acceptable for "show something random", not for statistics. Retry or wrap around if no row is found near max.

**2. TABLESAMPLE (approximate percentage)**
```sql
SELECT * FROM products TABLESAMPLE SYSTEM (0.1) LIMIT 10;      -- block sampling, fast, clustered
SELECT * FROM products TABLESAMPLE BERNOULLI (0.1) LIMIT 10;   -- row sampling, scans, less clustered
-- PostgreSQL tsm_system_rows extension: TABLESAMPLE SYSTEM_ROWS(10)
```
Other engines' TABLESAMPLE semantics differ: check their docs. Good for analytics samples. (Checked on PostgreSQL 18: `SYSTEM (10)` returned 452 of 5000 rows, `SYSTEM_ROWS(10)` returned 10.)

**3. Precomputed random column**
```sql
ALTER TABLE products ADD COLUMN rnd double precision NOT NULL DEFAULT random();
CREATE INDEX ON products (rnd);
SELECT * FROM products WHERE rnd >= random() ORDER BY rnd LIMIT 1;
```
Uniform enough and index-friendly; re-randomise periodically if the same items should not keep neighbours.

**4. Random offset with known count** (OK for small/medium tables)
```sql
SELECT * FROM products OFFSET floor(random() * (SELECT count(*) FROM products)) LIMIT 1;
```
OFFSET still walks rows: O(n) but no sort.

**5. Application-side**: cache the id list (or a sample) in memory or a cache and fetch by id.

## Filtering
Random among a filtered subset (in-stock only): combine method 3 with a composite or partial index (`WHERE in_stock`), or sample ids from the filtered set in the application.

## Verify
EXPLAIN shows an index scan with `LIMIT` (no full sort); run 10,000 picks on test data and check the distribution is acceptable for the use case.
