---
id: computing-software.database-administration.sqlite.skip-scan-and-or-optimizations
name: skip-scan-and-or-optimizations
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, skip-scan, or-optimization, sqlite-query-planner, multi-index-or]
level: practitioner
status: verified
description: "Understand when SQLite uses skip-scan on a composite index, how it handles OR terms (IN rewrite, multi-index OR), and how ANALYZE data enables these choices."
sources:
  - https://sqlite.org/optoverview.html#skipscan
  - https://sqlite.org/optoverview.html#or_optimizations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Skip-scan and OR optimizations

## Skip-scan
Index `(gender, birth_year)` and query `WHERE birth_year = 1990` (no condition on the first column). SQLite can "skip" through each distinct value of `gender` and seek `birth_year = 1990` within it.

Requirements:
- `ANALYZE` has been run, and `sqlite_stat1` shows the leading column has few distinct values (docs: profitable at about 18 or more duplicates per leading value; without ANALYZE the default guess is 10). Reproduced on 3.50.4: 20 rows per leading value gave the skip-scan plan, 10 gave `SCAN`.
- Without stats, skip-scan is never used (docs; reproduced: `SCAN people` before ANALYZE).

```sql
CREATE INDEX idx_people_g_y ON people(gender, birth_year);
ANALYZE;
EXPLAIN QUERY PLAN SELECT * FROM people WHERE birth_year = 1990;
-- SEARCH people USING INDEX idx_people_g_y (ANY(gender) AND birth_year=?)
```
`ANY(gender)` marks a skip-scan. If the leading column has high cardinality, skip-scan is slower than a dedicated index on `birth_year`; build one instead.

## OR terms
1. **Same column, equality → IN:** `a = 1 OR a = 5 OR a = 9` becomes `a IN (1,5,9)` and uses an index on `a`.
2. **Different columns → multi-index OR:** `WHERE a = ? OR b = ?` with separate indexes on `a` and `b`: SQLite runs each lookup, collects rowids into a temporary set and deduplicates.
```text
`--MULTI-INDEX OR
   |--INDEX 1
   |  `--SEARCH t USING INDEX idx_a (a=?)
   `--INDEX 2
      `--SEARCH t USING INDEX idx_b (b=?)
```
3. If any OR branch lacks a usable index, the whole query scans. Index every branch or rewrite as `UNION`.

## Tips
- Rerun `ANALYZE` (or `PRAGMA optimize`) after big data changes so these decisions reflect reality.
- Composite index column order still matters most; skip-scan is a fallback, not a design target.

## Verify
Compare timings for the skip-scan plan vs an index on the second column alone on production-like data.
