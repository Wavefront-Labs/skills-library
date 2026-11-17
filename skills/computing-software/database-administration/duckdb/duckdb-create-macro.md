---
id: computing-software.database-administration.duckdb.duckdb-create-macro
name: duckdb-create-macro
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, macro, create-macro, table-macro, overloading, function]
level: practitioner
status: docs-checked
description: "Define DuckDB scalar and table macros with default and typed parameters, overloads and temporary scope, and avoid the recursion, subquery and chaining limits."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/create_macro.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: package reusable SQL expressions or queries as macros (`CREATE FUNCTION` is an alias; macros are schema-dependent).

Scalar macro returns one value; a table macro uses `AS TABLE` and can return any shape. `TEMP` macros live for the connection only. Modifiers: `OR REPLACE`, `IF NOT EXISTS`.

```sql
CREATE MACRO add(a, b) AS a + b;
CREATE MACRO one() AS (SELECT 1);
CREATE FUNCTION main.my_avg(x) AS sum(x) / count(x);
CREATE MACRO add_default(a, b := 5) AS a + b;        -- default / named param
SELECT triple_add(40, c := 1, b := 1);                -- named order is free
CREATE MACRO is_maximal(a INTEGER) AS a = 2^31 - 1;   -- typed param

CREATE MACRO dynamic_table(c1, c2) AS TABLE SELECT c1 AS column1, c2 AS column2;
CREATE MACRO get_users(i) AS TABLE SELECT * FROM users WHERE uid IN (SELECT unnest(i));
SELECT * FROM get_users([1, 5]);
```

Generic table access: `CREATE MACRO checksum(tbl) AS TABLE SELECT bit_xor(md5_number(COLUMNS(*)::VARCHAR)) FROM query_table(tbl); SELECT * FROM checksum('tbl');`

Overloads must be declared together in one statement (by arity or by type); you cannot define the same name twice without dropping it:

```sql
CREATE MACRO add_x (a, b) AS a + b, (a, b, c) AS a + b + c;
CREATE OR REPLACE MACRO is_maximal (a TINYINT) AS a = 2^7 - 1, (a INT) AS a = 2^31 - 1;
```

How it works: macros are expanded textually, with parameters replaced by the arguments. So `CREATE MACRO add(a) AS a + b;` fails with `Binder Error: Referenced column "b" not found`, and untyped `add('hello', 3)` may fail with "Could not choose a best candidate function".

Limitations: (1) subquery-based scalar macros and table macros cannot be used in arguments of table functions (`Table function cannot contain subqueries`); (2) recursion is unsupported (a `fibo` macro hits `Max expression depth limit of 1000 exceeded`); (3) dot-chaining on the first argument is not allowed: `AS s.lower()` fails, write `lower(s)`.

Verify: `SELECT add_x(21, 42), add_x(21, 42, 21);` returns 63 and 84.

## Checked

2026-11-07. Read the CREATE MACRO Statement page in full and confirmed scalar and table macros, TEMP, OR REPLACE and IF NOT EXISTS, the FUNCTION alias, default, named and typed parameters, query_table checksum example, overloading (including the 63 and 84 result), textual expansion, the quoted Binder Errors, and the subquery, overload, recursion and function-chaining limitations. Nothing removed.

Method: documentation only; no commands were run.
