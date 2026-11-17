---
id: computing-software.database-administration.sql.float-rounding-errors
name: float-rounding-errors
category: computing-software
field: database-administration
product: sql
tags: [sql, float-rounding-errors]
level: practitioner
status: docs-checked
description: "Avoid float rounding surprises by choosing numeric over real and double precision."
sources: ["https://www.postgresql.org/docs/current/datatype-numeric.html", "https://www.sqlite.org/datatype3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Floating point versus exact numerics

- PostgreSQL `real` and `double precision` are inexact, variable-precision IEEE 754 binary floating-point types: some values cannot be converted exactly and are stored as approximations. For exact storage and calculations (the page names monetary amounts) use `numeric(p,s)`.
- Comparing two floating-point values for equality might not always work as expected; compare `abs(a-b) < eps` instead of `=`.
- SQLite stores a REAL value as an 8-byte IEEE floating point number, and its storage classes are NULL, INTEGER, REAL, TEXT and BLOB (no exact decimal type), so money is commonly kept as integer minor units.
- `numeric` calculations yield exact results where possible (addition, subtraction, multiplication) but are very slow compared with the integer and floating-point types. PostgreSQL `numeric` can also hold `NaN` (and infinity in an unconstrained column).
- Self-check: sum 0.1 ten times in a float8 column and in a numeric column and compare each total with 1.

## Checked

Date: 2026-11-07. Read the PostgreSQL Numeric Types page (datatype-numeric: the type table, the Arbitrary Precision Numbers passages, and the Floating-Point Types section in full; the integer sections by search) and SQLite datatype3 (storage class list and the REAL definition, by search; the rest of the page not read in full). Confirmed: inexact IEEE 754 types, numeric for exact values, the equality warning, numeric speed warning, NaN support, SQLite REAL as 8-byte IEEE. Removed: the specific `0.1::float8 + 0.2::float8 = 0.3::float8` result (not shown on the page); the "integer minor units" line is now flagged as common practice rather than a documented rule. The five storage class names were read on the SQLite page.
Method: documentation only; no commands were run.
