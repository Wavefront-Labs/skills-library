---
id: computing-software.data-engineering.snowflake.snowpark-optimized-warehouses
name: snowpark-optimized-warehouses
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowpark-optimized-warehouse, warehouse-type, resource-constraint, memory-intensive, snowpark, ml-training, udf-memory, virtual-warehouse]
level: practitioner
status: docs-checked
description: "Use Snowpark-optimized warehouses for memory-heavy Python (ML training, big UDF state): when they help, RESOURCE_CONSTRAINT options, sizing, and cost vs standard."
sources:
  - https://docs.snowflake.com/en/user-guide/warehouses-snowpark-optimized
  - https://docs.snowflake.com/en/sql-reference/sql/create-warehouse
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snowpark-optimized warehouses

**Goal:** run Python workloads that exceed a standard warehouse node's memory (single-node ML training, big pandas in stored procedures, UDFs with large models) without out-of-memory failures.

## What they are
Warehouses with more memory per node (16x a standard warehouse node by default; the default constraint is `MEMORY_16X`).

```sql
create warehouse ml_wh
  warehouse_size = 'MEDIUM'
  warehouse_type = 'SNOWPARK-OPTIMIZED'
  resource_constraint = 'MEMORY_16X'      -- MEMORY_1X, MEMORY_16X, MEMORY_64X, each with an _x86 variant
  auto_suspend = 60 auto_resume = true initially_suspended = true;
```
`RESOURCE_CONSTRAINT` lets you choose memory multiples and CPU architecture. The minimum warehouse size depends on the constraint (the docs table lists XSMALL for `MEMORY_1X`, MEDIUM for `MEMORY_16X`, LARGE for `MEMORY_64X`).

## When to use
- Stored procedures doing `to_pandas()` of tens of GB, scikit-learn/XGBoost training on a single node.
- UDFs loading large model artifacts per process.
- Out-of-memory failures of Python procedures or UDFs on standard warehouses.

## When not to
- Regular SQL and Snowpark DataFrame operations (which push down to SQL): use standard warehouses; they're cheaper and parallelise across nodes.
- Distributed training: a single procedure runs on one node; bigger warehouse sizes add nodes that a single-node Python process doesn't use (except for UDF parallelism).

## Practice
- Keep a dedicated small Snowpark-optimized warehouse for ML jobs with aggressive auto-suspend; don't run BI on it.
- Measure: compare runtime x credit rate on standard vs optimized for the same job.
- In dbt Python models or Snowpark procedures, set the warehouse explicitly for that model/session.

## Verify
- [ ] Job that failed with memory errors on standard completes on the optimized warehouse.
- [ ] Cost per run recorded and compared before keeping it.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED', RESOURCE_CONSTRAINT values (MEMORY_1X/16X/64X and _x86), 16x default memory, default MEMORY_16X, per-constraint minimum sizes (warehouses-snowpark-optimized, create-warehouse pages).

Removed or corrected: credit-rate, local-cache and 'most regions' claims, and the quoted error message (not on the pages read).

Method: documentation only; no commands were run.
