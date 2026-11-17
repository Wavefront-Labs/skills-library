---
id: computing-software.data-engineering.apache-spark.temp-views-and-parameterized-sql
name: temp-views-and-parameterized-sql
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark-sql, temp-views, parameterized-sql, global-temp-view, sql-injection, spark-sql-args, identifier-clause]
level: practitioner
status: docs-checked
description: "Mix Spark SQL and DataFrames safely: temp vs global temp views, spark.sql with named parameters and IDENTIFIER() instead of f-strings, and view lifetime gotchas."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.sql.html
  - https://spark.apache.org/docs/latest/sql-ref-syntax-ddl-create-view.html
  - https://spark.apache.org/docs/latest/sql-ref-identifier-clause.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temp views and parameterized Spark SQL

**Goal:** expose DataFrames to SQL and run SQL with user/config values without string formatting bugs or injection.

## Views
```python
df.createOrReplaceTempView("orders_v")          # session-scoped
df.createOrReplaceGlobalTempView("orders_g")    # app-scoped, query as global_temp.orders_g
spark.sql("select count(*) from orders_v")
spark.catalog.dropTempView("orders_v")
```
- Temp views store the **plan**, not data. Re-running the view recomputes from source each time; `cache()` the DataFrame if reused.
- Temp views die with the SparkSession; global temp views with the application. Neither is visible to other clusters or jobs. Use a real table/view for that.

## Parameterized queries
```python
spark.sql(
    "select * from orders where order_date >= :start and region = :region",
    args={"start": "2026-10-01", "region": "EMEA"},
)
# positional markers
spark.sql("select * from orders where amount > ?", args=[100])
```
Values are bound as literals: no quoting issues, no injection.

## Table and column names
Parameters cannot stand in for identifiers directly. Use `IDENTIFIER()`:
```python
spark.sql("select * from IDENTIFIER(:tbl) where dt = :dt", args={"tbl": "prod.sales.orders", "dt": "2026-10-17"})
```
If you must build identifiers from strings, validate against an allow-list or `spark.catalog.tableExists`.

## DataFrames as SQL inputs without views
```python
spark.sql("select * from {src} where amount > {m}", src=df, m=100)
```
This kwargs form is string templating for DataFrames/literals; prefer `args=` for user input.

## Gotchas
- f-strings with dates: `f"... dt = {d}"` produces `dt = 2026-10-17` (arithmetic: 1999), not a date. Bind parameters.
- `createTempView` (no replace) fails if the name exists, common in rerun notebooks.
- A temp view shadows a permanent table of the same name in unqualified queries.
- `spark.sql("SET var=...")` / `${var}` substitution (`spark.sql.variable.substitute`) is legacy; `DECLARE VARIABLE` session variables are the newer alternative.

## Verify
- [ ] No SQL built with f-strings from external input; grep for `spark.sql(f"`.
- [ ] Views used across steps are either cached intentionally or materialised as tables.

## Checked

2026-10-28. Confirmed: named and positional parameters on the SparkSession.sql page; IDENTIFIER() and DECLARE on the identifier-clause page. Removed: version gates and an isolation claim not in the pages.

Method: documentation only; no commands were run.
