---
id: computing-software.database-administration.duckdb.duckdb-type-casting
name: duckdb-type-casting
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, cast, try-cast, implicit-casting, struct-cast, cast-to-type, typecasting]
level: practitioner
status: docs-checked
description: "DuckDB explicit and implicit casts: CAST and ::, TRY_CAST, lossy rounding, overflow errors, VARCHAR, list and struct casts, combination casting and cast_to_type."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/data_types/typecasting.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/expressions/cast.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: convert types predictably and know where DuckDB casts for you.

Explicit: `CAST(col AS VARCHAR)` or `col::VARCHAR`. Impossible casts (INTEGER to DATE) are errors; failing values raise e.g. `Conversion Error: Could not convert string 'hello' to INT32`. `TRY_CAST(expr AS type)` never throws and returns NULL instead.

Implicit: added automatically only where the cast cannot fail, e.g. INTEGER to DOUBLE (so `sin(1)` works) but not DOUBLE to INTEGER. Check with `can_cast_implicitly(source_value, target_value)`. Since v0.10.0 nothing is implicitly cast to VARCHAR (setting `old_implicit_casting` restores it, to be deprecated). NULL casts to any type.

Combination casting: for comparisons (`=`, `<`, `>`), set operations and nested constructors (`list_value`, `[...]`, `MAP`) the system picks a joint parent type, more leniently, e.g. `list_value(1::INT64, 1::UINT64)` gives `INT128[]`, and BOOL may become INT.

Behaviours:
- Lossy casts are allowed and round: `CAST(3.5 AS INTEGER)` is 4, `CAST(-1.7 AS INTEGER)` is -2.
- Overflow throws: `CAST(999 AS TINYINT)` gives `Conversion Error: ... out of range for the destination type INT8`; use `TRY_CAST` for NULL.
- Anything casts to VARCHAR, usually losslessly (`CAST(CAST([1,2,3] AS VARCHAR) AS INTEGER[])`); the reverse can fail at runtime.
- Lists cast child by child: `CAST([1,2,3] AS VARCHAR[])`. An `INTEGER[3]` array implicitly casts to `INTEGER[]`.
- Structs cast if they share at least one field. Missing target fields become NULL, extra source fields are dropped, and fields are matched by name regardless of order: `CAST({'a': 42, 'b': 84} AS STRUCT(b VARCHAR, a VARCHAR))`. In combination casting the result has the superset of fields, recursively.

`cast_to_type(expr, NULL::INTEGER)` casts to the type of another expression, mainly for generic macros:
```sql
CREATE MACRO conditional_add(col, nr) AS
  CASE WHEN typeof(col) == 'INTEGER' THEN cast_to_type(col::INTEGER + nr, col) ELSE col END;
SELECT conditional_add(COLUMNS(*), 100) FROM tbl;
```
The CASE branches must return the same type, hence the cast back.

## Checked

2026-11-07. Read the DuckDB 1.4 docs pages sql/data_types/typecasting.md and sql/expressions/cast.md in full. Confirmed: CAST and `::` syntax, impossible-cast example, the `hello` conversion error text, TRY_CAST returning NULL, implicit-cast rules, `sin(1)`, `can_cast_implicitly`, v0.10.0 VARCHAR change and `old_implicit_casting`, NULL casting, combination casting examples and contexts, lossy rounding examples, overflow error text, VARCHAR universality and round trip, list, array and struct rules, `cast_to_type` and the macro example. Removed: the invented Verify step.

Method: documentation only; no commands were run.
