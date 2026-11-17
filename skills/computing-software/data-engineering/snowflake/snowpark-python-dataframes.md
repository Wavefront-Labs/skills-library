---
id: computing-software.data-engineering.snowflake.snowpark-python-dataframes
name: snowpark-python-dataframes
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowpark, snowpark-python, snowpark-dataframe, session-builder, lazy-evaluation, pushdown, to-pandas, save-as-table, snowpark-pandas]
level: practitioner
status: docs-checked
description: "Transform data with Snowpark Python DataFrames: creating a Session, lazy evaluation, common transforms and writes, avoiding to_pandas pulls, and the Snowpark pandas API."
sources:
  - https://docs.snowflake.com/en/developer-guide/snowpark/python/index
  - https://docs.snowflake.com/en/developer-guide/snowpark/python/working-with-dataframes
  - https://docs.snowflake.com/en/developer-guide/snowpark/python/pandas-on-snowflake
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowpark Python DataFrames

**Goal:** write Python transformations that execute inside Snowflake, with no data leaving unless you ask.

## Session
```python
from snowflake.snowpark import Session
session = Session.builder.config("connection_name", "prod").create()   # profile from connections.toml
```
Snowflake's pages show `connection_name` with a `connections.toml` profile; keep credentials in that file or a secrets manager, never in code.

## Transform (lazy)
```python
from snowflake.snowpark import functions as F
orders = session.table("raw.orders")
daily = (orders.filter(F.col("status") != "cancelled")
               .with_column("order_date", F.to_date("ordered_at"))
               .group_by("order_date", "country")
               .agg(F.sum("amount").alias("revenue")))
daily.write.mode("overwrite").save_as_table("analytics.daily_revenue")
```
DataFrames are evaluated lazily: nothing is sent to Snowflake until an action such as `collect`, `show` or `save_as_table` runs. `session.table`, `filter`, `with_column`, `group_by`, `write.mode("overwrite")` and `save_as_table` all appear in the Snowflake DataFrame guide.

## Keep data in Snowflake
- `to_pandas()` and `collect()` bring results to the client: fine for small results, wrong for transformations.
- Joining DataFrames that share column names needs aliasing; the guide shows `.alias(...)` for this.
- A large `create_dataframe` from local data uploads through the client.

## Snowpark pandas API
`import modin.pandas as pd` with `import snowflake.snowpark.modin.plugin` runs pandas syntax as Snowflake queries. Check the page's API coverage for the operations you use.

## Verify
- [ ] No `to_pandas` on large tables.
- [ ] Output table row counts match a SQL reference query.

## Checked
2026-11-01. Confirmed against the Snowflake pages Snowpark Python developer guide, Working with DataFrames (lazy evaluation, session.table, with_column, group_by, save_as_table, alias, create_dataframe) and pandas on Snowflake (modin imports, connection_name and connections.toml). Removed: the key-pair session config, the generated-SQL inspection call, query_tag, transient table_type, the merge call, cache_result, and the UDF sandbox and warehouse sizing claims.
Method: documentation only; no commands were run.
