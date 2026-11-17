---
id: computing-software.data-engineering.databricks.quarantining-invalid-records-in-pipelines
name: quarantining-invalid-records-in-pipelines
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, dlt-quarantine, expectations, data-quality, lakeflow-declarative-pipelines]
level: advanced
status: docs-checked
description: "Quarantine invalid records in Lakeflow Declarative Pipelines (DLT) instead of dropping them: inverted rules, flagged tables, monitoring."
sources:
  - https://docs.databricks.com/aws/en/dlt/expectation-patterns
  - https://docs.databricks.com/aws/en/dlt/expectations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarantining invalid records

**Goal:** bad rows are kept, explainable and reprocessable, while good rows flow downstream.

## Rules in one place
```python
from pyspark import pipelines as dp
from pyspark.sql import functions as F

rules = {
    "valid_id": "order_id IS NOT NULL",
    "valid_amount": "amount >= 0",
    "valid_date": "order_date <= current_date()",
}
quarantine_expr = "NOT ({})".format(" AND ".join(f"({r})" for r in rules.values()))
```

## Pattern A: split into two tables
```python
@dp.table
@dp.expect_all_or_drop(rules)
def orders_silver():
    return spark.readStream.table("orders_bronze")

@dp.table
def orders_quarantine():
    return spark.readStream.table("orders_bronze").where(quarantine_expr)
```

## Pattern B: one flagged table
```python
@dp.table(partition_cols=["is_quarantined"])
@dp.expect_all(rules)                          # metrics only
def orders_flagged():
    return spark.readStream.table("orders_bronze").withColumn("is_quarantined", F.expr(quarantine_expr))

@dp.view
def orders_valid():
    return spark.readStream.table("orders_flagged").where("NOT is_quarantined")
```

## Operate
- Track drop/quarantine rate in the pipeline UI (Data quality tab) or by querying the pipeline event log (`flow_progress` events); for SQL-created standalone pipelines query the event log. Alert when a threshold is exceeded.
- Reprocess: fix upstream or rules, then full-refresh the affected tables, or write a backfill that re-reads quarantined rows.
- Nulls: write explicit `IS NOT NULL` rules for required columns, as the Databricks examples do, instead of relying on how a comparison treats NULL.

## Verify
Feed rows violating each rule: they appear in the quarantine output, and silver excludes them.

## Checked

2026-11-09. Confirmed on the Databricks pipeline expectations and expectation patterns pages: `from pyspark import pipelines as dp`, `dp.table`, `dp.view`, `dp.expect_all`, `dp.expect_all_or_drop`, rules as a Python dictionary, the quarantine pattern with `NOT(...)` over joined rules and a table partitioned by `is_quarantined` with valid and invalid views on top, expectation metrics in the pipeline UI and `flow_progress` events. Removed: the per-rule `failed_rules` column and `array_compact` (not on the pages), `dp.temporary_view` (pages use `dp.view`), the event log field path and the NULL-evaluation claim.

Method: documentation only; no commands were run.

