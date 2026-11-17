---
id: computing-software.database-administration.sql.sqlite-storage-classes-typeof
name: sqlite-storage-classes-typeof
category: computing-software
field: database-administration
product: sql
tags: [sql, sqlite-storage-classes-typeof]
level: intro
status: docs-checked
description: "Inspect SQLite storage classes with typeof() and understand comparison order."
sources: ["https://www.sqlite.org/datatype3.html", "https://www.sqlite.org/lang_corefunc.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage classes and typeof()

- Five storage classes: NULL, INTEGER, REAL, TEXT, BLOB. There is no separate boolean or date class: booleans are integers 0 and 1, dates are TEXT, REAL or INTEGER values.
- `SELECT typeof(col), count(*) FROM t GROUP BY 1;` finds stray types. `typeof()` returns null, integer, real, text or blob.
- Sort order across classes: NULL first, then INTEGER and REAL in numeric order, then TEXT in collating order, then BLOB in memcmp() order. No storage class conversions happen before the sort.
- Column affinity (TEXT, NUMERIC, INTEGER, REAL, BLOB) is a recommended type, not a requirement; on insert SQLite converts the value only when the conversion loses nothing. BLOBs and NULLs are never converted.
- Affinity of a non-STRICT column comes from the declared type, by the first matching rule: contains "INT" gives INTEGER; contains "CHAR", "CLOB" or "TEXT" gives TEXT; contains "BLOB" or no type gives BLOB; contains "REAL", "FLOA" or "DOUB" gives REAL; otherwise NUMERIC. Length arguments such as VARCHAR(255) are ignored.
- Expressions have no affinity, except a plain column reference and `CAST(expr AS type)`. Any operator, even unary `+`, removes a column's affinity.
- `CAST(x AS type)` gives the expression the affinity of that declared type. CAST(4.0 AS INT) returns integer 4, CAST(4.0 AS NUMERIC) leaves 4.0.
- Default string comparison is BINARY (memcmp). NOCASE folds only the 26 ASCII upper-case letters; RTRIM ignores trailing spaces.
- Self-check: audit mixed-type columns with the typeof query above.

## Checked

2026-11-08. Confirmed against Datatypes In SQLite (storage classes, boolean and date notes, affinity rules and the declared-type rule order, expression affinity, sort order, collating sequences). The list of typeof() return values is from the core functions page. Removed the claim that CAST "forces a class" in favour of the documented affinity wording, and the PostgreSQL docs root source.

Method: documentation only; no commands were run.
