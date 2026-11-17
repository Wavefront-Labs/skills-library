---
id: computing-software.database-administration.sql.implicit-conversion-pitfalls
name: implicit-conversion-pitfalls
category: computing-software
field: database-administration
product: sql
tags: [sql, implicit-conversion-pitfalls]
level: practitioner
status: docs-checked
description: "Spot implicit casts and affinity rules that change comparison results in SQLite and PostgreSQL."
sources: ["https://www.sqlite.org/datatype3.html", "https://www.postgresql.org/docs/current/typeconv-oper.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicit conversions and comparison traps

- SQLite orders by storage class: an INTEGER or REAL is less than any TEXT or BLOB, so with two literals `'10' < 9` is false (the TEXT is greater). Conversions happen only through column affinity: if one operand has INTEGER, REAL or NUMERIC affinity and the other has TEXT, BLOB or no affinity, NUMERIC affinity is applied to the other. A bare literal has no affinity, so `'10' < 9` is compared as is; a TEXT-affinity column compared with a number gets the number converted to text.
- In SQLite any operator applied to a column, even unary `+`, removes that column's affinity from the expression, and the right side of `IN (list)` has no affinity.
- PostgreSQL resolves an operator by exact type match first; an unknown-type literal (quoted `'5'`) is assumed to be the same type as the other operand, so `WHERE int_col = '5'` resolves to the integer operator. Otherwise candidates that cannot be reached by implicit conversion are discarded.
- Practice: compare like with like, and cast the parameter side rather than wrapping the column in a function or cast (this keeps plain column comparisons; whether an index is used is for EXPLAIN to show).
- Self-check: EXPLAIN the query and confirm the condition is the one you intended.

## Checked

Date: 2026-11-07. Read SQLite datatype3 sections 3 to 4.2 (affinity rules, expression affinity, sort order, conversions before comparison) and the PostgreSQL Operator Type Resolution steps. Removed: SQL Server and MySQL claims (including `'abc' = 0` in MySQL; no SQL Server or MySQL page was read), the claim that `int_col = text_col` errors in PostgreSQL (the page gives resolution steps but no such error text), and the index-defeating claim as stated. Corrected the SQLite sentence to say where affinity, not storage class alone, decides.
Method: documentation only; no commands were run.
