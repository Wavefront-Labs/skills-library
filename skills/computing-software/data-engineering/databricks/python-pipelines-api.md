---
id: computing-software.data-engineering.databricks.python-pipelines-api
name: python-pipelines-api
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, pyspark-pipelines, spark-declarative-pipelines, lakeflow-declarative-pipelines, dlt-python]
level: advanced
status: docs-checked
description: "Write Lakeflow/Spark Declarative Pipelines in Python with pyspark.pipelines: tables, materialized views, temporary views, append flows and expectations."
sources:
  - https://spark.apache.org/docs/latest/declarative-pipelines-programming-guide.html
  - https://docs.databricks.com/aws/en/dlt/expectation-patterns
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Python pipeline API (pyspark.pipelines / dlt)

**Goal:** declarative Python pipelines: define datasets as functions, let the engine handle dependencies, retries and incremental processing.

## Imports
```python
from pyspark import pipelines as dp     # Spark Declarative Pipelines
```

## Datasets
```python
@dp.table(comment="raw orders", table_properties={"quality": "bronze"})
def orders_bronze():
    return (spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", "json")
            .load("/Volumes/main/raw/landing/orders"))

@dp.materialized_view
def daily_sales():
    return spark.read.table("orders_silver").groupBy("order_date").sum("amount")

@dp.temporary_view
def orders_clean():
    return spark.readStream.table("orders_bronze").where("order_id IS NOT NULL")
```
- `@dp.table` with a function that performs a streaming read creates a **streaming table**; use `@dp.materialized_view` for a materialized view.
- Reference other datasets with `spark.read.table` / `spark.readStream.table`.

## Expectations
```python
@dp.table
@dp.expect_or_drop("has_id", "order_id IS NOT NULL")      # drop bad rows
@dp.expect_or_fail("known_currency", "currency IN ('EUR','USD')")
def orders_silver():
    return spark.readStream.table("orders_clean")
```

## CDC and flows
```python
# Auto CDC flows are described on the Databricks flows page; take the Python function name and arguments from there.
dp.create_streaming_table("all_events")
@dp.append_flow(target="all_events")
def eu_events(): return spark.readStream.table("events_eu")
```

## Rules
- Dataset functions must be pure: no `.collect()` or other side effects.

## Verify
Pipeline graph shows all datasets with correct dependencies.

## Checked

- 2026-10-28: confirmed on the Spark declarative pipelines programming guide (`pyspark.pipelines`, `@dp.materialized_view`, `@dp.temporary_view`, `@dp.table` with a streaming read, `dp.create_streaming_table`, `dp.append_flow`) and the Databricks expectation patterns page (`dp.expect_or_drop`, `dp.expect_or_fail`).
- Removed: the Auto CDC code (`create_auto_cdc_flow`, `apply_changes` history), `dp.expect`, the legacy `dlt` claims, the validate dry-run step and the factory-loop rule (not in the fetched pages).

Method: documentation only; no commands were run.
