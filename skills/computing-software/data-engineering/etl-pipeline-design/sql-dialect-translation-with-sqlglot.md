---
id: computing-software.data-engineering.etl-pipeline-design.sql-dialect-translation-with-sqlglot
name: sql-dialect-translation-with-sqlglot
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, data-migration, sql-translation, sqlglot, dialect-conversion, bigquery-migration-service, snowconvert, transpile]
level: practitioner
status: gated
description: "Translate SQL between warehouse dialects with sqlglot: transpile, unsupported-feature errors, AST rewrites, batch conversion, and verifying semantics rather than just syntax."
sources:
  - https://sqlglot.com/sqlglot.html
  - https://github.com/tobymao/sqlglot
  - https://cloud.google.com/bigquery/docs/batch-sql-translator
  - https://docs.snowflake.com/en/migrations/snowconvert-docs/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL dialect translation with sqlglot

**Goal:** convert hundreds of queries from one dialect to another automatically, find the ones that cannot be converted, and prove translated queries return the same results.

## 1. Basic transpile
```python
import sqlglot
sql = "SELECT TOP 10 ISNULL(name, 'n/a') AS n, DATEADD(day, 7, created) FROM dbo.users"
print(sqlglot.transpile(sql, read="tsql", write="snowflake", pretty=True)[0])
```
Run with sqlglot 30.24: output is `SELECT COALESCE(name, 'n/a') AS n, DATEADD(DAY, 7, created) FROM dbo.users LIMIT 10` (pretty-printed over several lines). All 13 dialect names below were accepted by `transpile(..., read=d, write=d)`.
Dialect names: `tsql`, `snowflake`, `bigquery`, `databricks`, `spark`, `redshift`, `postgres`, `mysql`, `oracle`, `teradata`, `duckdb`, `trino`, `hive`.

## 2. Make failures loud
By default unsupported constructs may degrade silently (warnings). Raise instead:
```python
from sqlglot.errors import UnsupportedError, ErrorLevel
sqlglot.transpile(sql, read="teradata", write="bigquery", unsupported_level=ErrorLevel.RAISE)
```
Procedural code is not translated: with `ErrorLevel.RAISE` a T-SQL `DECLARE ... WHILE` block raised `UnsupportedError: Unsupported While block syntax` (other procedural input may raise `ParseError` instead) — typically T-SQL loops (T-SQL `DECLARE`/`WHILE`, PL/SQL blocks, Teradata BTEQ commands). Those need manual rewrite or a vendor tool.

## 3. Batch conversion with a report
```python
import pathlib, sqlglot
from sqlglot.errors import ErrorLevel
ok, bad = 0, []
for p in pathlib.Path("legacy_sql").rglob("*.sql"):
    try:
        out = sqlglot.transpile(p.read_text(), read="tsql", write="snowflake",
                                pretty=True, unsupported_level=ErrorLevel.RAISE)
        pathlib.Path("converted", p.name).write_text(";\n".join(out) + ";\n"); ok += 1
    except Exception as e:
        bad.append((p.name, type(e).__name__, str(e)[:120]))
print(ok, "converted;", len(bad), "need manual work")
```
The share that converts automatically depends entirely on your code base (not measured here); count the remainder early for the plan. A two-file test run of this loop converted the plain SELECT and listed the T-SQL WHILE script as needing manual work.

## 4. AST rewrites for house rules
```python
from sqlglot import exp, parse_one
tree = parse_one(sql, read="tsql")
for t in tree.find_all(exp.Table):            # dbo.x → raw.legacy.x
    if t.db == "dbo": t.set("db", exp.to_identifier("legacy")); t.set("catalog", exp.to_identifier("raw"))
print(tree.sql(dialect="snowflake"))
```
`sqlglot.optimizer.qualify` adds explicit table/column qualification — useful before lineage or rewrites.

## 5. Semantic traps syntax translation cannot fix
- Integer division: sqlglot 30.24 left `5/2` unchanged from T-SQL to Snowflake and BigQuery (checked), so the semantics are yours to verify; T-SQL/Postgres give 2, Snowflake/BigQuery 2.5 (gated: unconfirmed, source is paywalled or blocked).
- NULL/empty string (Oracle treats `''` as NULL (gated: unconfirmed, source is paywalled or blocked)).
- Case sensitivity of identifiers and string comparison collations.
- Implicit casts, date arithmetic and week-start defaults; `DATEDIFF` boundary semantics.
- Function defaults (e.g. `ROUND` tie-breaking differs by engine and type; DuckDB `round(2.5)` returned 3 for DECIMAL).
Run every translated query on both platforms against identical data and diff the results (see migration reconciliation).

## 6. Vendor alternatives
(Vendor tool coverage lists below are unchecked (gated: unconfirmed, source is paywalled or blocked).)
BigQuery Migration Service batch/interactive SQL translator (Teradata, Redshift, Oracle, SQL Server, Snowflake → BigQuery), Snowflake SnowConvert (incl. procedures), Databricks Lakebridge (BladeBridge-based converter). Use them for procedural code; use sqlglot for scripting, custom rules and dialects they don't cover.

## Verify
- [ ] Conversion runs with `unsupported_level=RAISE`; failures are listed, not hidden.
- [ ] Each converted query's result was diffed against the original on the same data.
- [ ] Manual-rewrite backlog size is in the migration plan.
