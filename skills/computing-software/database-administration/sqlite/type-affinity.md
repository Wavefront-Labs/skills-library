---
id: computing-software.database-administration.sqlite.type-affinity
name: type-affinity
category: computing-software
field: database-administration
product: sqlite
tags: [database-administration, sqlite, sqlite-alter-table, type-affinity, dynamic-typing, typeof, strict-tables, integer-vs-text, datatype-rules, comparison-affinity]
level: practitioner
status: verified
description: "Understand SQLite type affinity (how declared types map to INTEGER, TEXT, REAL, NUMERIC, BLOB) and the surprises it causes in comparisons and indexes, and when to use STRICT."
sources:
  - https://sqlite.org/datatype3.html
  - https://sqlite.org/stricttables.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type affinity

**Goal:** predict what SQLite actually stores and how values compare, so
`WHERE id = '42'` and sorting behave as intended.

## Values have types, columns have affinity
Each value is NULL, INTEGER, REAL, TEXT or BLOB. A column's declared type only
gives an **affinity**, decided by substring rules in this order:
1. contains `INT` → INTEGER (`BIGINT`, but also `POINT`, which contains "INT")
2. contains `CHAR`, `CLOB`, `TEXT` → TEXT (`VARCHAR(10)`: length ignored)
3. contains `BLOB` or no type → BLOB (none)
4. contains `REAL`, `FLOA`, `DOUB` → REAL
5. otherwise → NUMERIC (`DECIMAL`, `BOOLEAN`, `DATE`, `DATETIME`, `STRING`!)
`STRING` gets NUMERIC affinity: `'0123'` stored there becomes integer 123.

Affinity converts on insert when lossless: inserting `'42'` into an INTEGER column
stores integer 42; inserting `'abc'` stores text 'abc' (no error).

## Surprises
```sql
CREATE TABLE t(code TEXT, n INTEGER, x);
INSERT INTO t VALUES (007, '007', '7');
SELECT typeof(code), code, typeof(n), n, typeof(x) FROM t;   -- text '7', integer 7, text
```
- Comparisons apply affinity of a column operand to the other side, so
  `WHERE n = '7'` works, but comparing two expressions without column affinity
  (`'7' = 7`) is false.
- Mixed types in one column sort as NULL < numbers < text < blob.

## Find mixed types
```sql
SELECT typeof(amount), count(*) FROM orders GROUP BY 1;
```

## STRICT tables (3.37+)
```sql
CREATE TABLE orders(id INTEGER PRIMARY KEY, amount_cents INTEGER NOT NULL, note TEXT) STRICT;
```
Allowed types: INT, INTEGER, REAL, TEXT, BLOB, ANY. Wrong-type inserts fail with
`cannot store TEXT value in INTEGER column`. Use STRICT for new schemas, as long as every
SQLite library that opens the file is 3.37+ (older versions report the schema as malformed).

## Verify
`typeof()` group-by queries show one type per column; for STRICT tables,
`PRAGMA table_list` shows `strict = 1`.

## Checked
- SQLite 3.50.4 (Python): declared-type affinity for BIGINT, POINT, VARCHAR(10), CLOB, TEXT, BLOB, no type, REAL, FLOATING, DOUBLE, DECIMAL, BOOLEAN, DATE, DATETIME, STRING and INTEGER stores `'0123'` as the listed type; the `007` example output, `'7' = 7` false, `WHERE n = '7'` true, `'abc'` kept as text in an INTEGER column, mixed-type order null < number < text < blob; STRICT allows INT, INTEGER, REAL, TEXT, BLOB, ANY and rejects VARCHAR, NUMERIC and DATE (`unknown datatype`), its insert error text matches, `pragma_table_list` shows `strict = 1`. sqlite.org's STRICT page documents 3.37.0 and the older-reader backward-compatibility rule.
