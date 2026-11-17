---
id: computing-software.data-engineering.polars.sql-context-and-statements
name: sql-context-and-statements
category: computing-software
field: data-engineering
product: polars
tags: [polars, sql, sqlcontext, register, cte, create-table, show-tables, polars-sql-context, eager]
level: practitioner
status: docs-checked
description: "Run SQL on Polars frames with SQLContext: register frames, execute lazily or eagerly, join mixed sources, and use CTEs, CREATE TABLE AS and SHOW TABLES."
sources:
  - https://docs.pola.rs/user-guide/sql/intro/
  - https://docs.pola.rs/user-guide/sql/cte/
  - https://docs.pola.rs/user-guide/sql/create/
  - https://docs.pola.rs/user-guide/sql/show/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query Polars DataFrames/LazyFrames with SQL.

There is no separate SQL engine: SQL is translated to Polars expressions and run by the Polars engine. The page recommends the expression API for readability and new features, but SQL is supported. Polars aims to follow PostgreSQL syntax where possible and supports only a subset of SQL.

Register frames
```python
ctx = pl.SQLContext(register_globals=True)          # all global DataFrames/LazyFrames
ctx = pl.SQLContext(frames={"table_one": df, "table_two": lf})
ctx = pl.SQLContext(df=df, lf=lf)                   # kwargs
ctx = pl.SQLContext(df_pandas=pl.from_pandas(df_pandas))
```
Later changes: `register`, `register_globals`, `register_many`, `unregister`. A NumPy-backed Pandas frame triggers a potentially expensive conversion; Arrow-backed is much cheaper.

Execute
Queries always run lazily. Get a result by setting `eager=True` on `SQLContext(...)`, on `execute(..., eager=True)`, or by calling `.collect()`.
```python
with pl.SQLContext(register_globals=True, eager=True) as ctx:
    print(ctx.execute("SELECT * from pokemon LIMIT 5"))
```
Mixed sources: `pl.scan_csv`, `pl.scan_ndjson` and `pl.from_pandas(...)` frames can be joined, e.g. `LEFT JOIN products_categories USING (product_id)`. Lazy reading loads only needed rows and columns. Cloud datalakes: point a PyArrow dataset at it and use `scan_pyarrow_dataset`.

Statements
- CTE: `WITH older_people AS (SELECT * FROM my_table WHERE age > 30) SELECT * FROM older_people WHERE STARTS_WITH(name,'C')`.
- `CREATE TABLE older_people AS SELECT * FROM my_table WHERE age > 30`. The result is not the table; it is registered in the context. Read it back with `SELECT * FROM older_people`.
- `SHOW TABLES` returns a DataFrame of tables registered in the current `SQLContext` only.
- Also listed: `EXPLAIN SELECT ...`, `DROP TABLE [IF EXISTS] t`, `TRUNCATE TABLE [IF EXISTS] t`.

The compatibility list names these as not yet supported: `INSERT`, `UPDATE` or `DELETE` statements, and meta queries such as `ANALYZE`. The same page's Iceberg catalog section does describe `INSERT INTO` and other writes on catalog tables; see sql-iceberg-catalog.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/sql/intro/; https://docs.pola.rs/user-guide/sql/cte/; https://docs.pola.rs/user-guide/sql/create/; https://docs.pola.rs/user-guide/sql/show/. Corrected: Reworded the unsupported-statements line to say the compatibility list names INSERT, UPDATE, DELETE and ANALYZE, which the Iceberg section of the same page contradicts. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
