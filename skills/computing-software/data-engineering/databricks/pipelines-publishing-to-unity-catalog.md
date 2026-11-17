---
id: computing-software.data-engineering.databricks.pipelines-publishing-to-unity-catalog
name: pipelines-publishing-to-unity-catalog
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, dlt-unity-catalog, lakeflow-declarative-pipelines, multi-schema, publishing-mode]
level: advanced
status: docs-checked
description: "Publish Lakeflow Declarative Pipeline (DLT) tables to Unity Catalog: default catalog and schema, writing to multiple schemas, LIVE keyword migration, ownership and grants."
sources:
  - https://docs.databricks.com/aws/en/dlt/unity-catalog
  - https://docs.databricks.com/aws/en/dlt/target-schema
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing pipelines to Unity Catalog and multiple schemas

**Goal:** pipeline tables land in the right catalogs/schemas with correct ownership and access.

## Default publishing mode
Pipelines created before February 5, 2025 might use the legacy publishing mode; the current default publishing mode works like this: the pipeline has a default `catalog` and `schema`, and datasets can be written to **any schema** by fully qualifying names:
```sql
CREATE OR REFRESH STREAMING TABLE bronze.orders AS SELECT * FROM STREAM read_files('/Volumes/raw/landing/orders');
CREATE OR REFRESH MATERIALIZED VIEW main.gold.daily_sales AS
SELECT order_date, sum(amount) FROM silver.orders GROUP BY ALL;
```
```python
@dp.table(name="main.silver.orders")
def orders(): return spark.readStream.table("bronze.orders").where("amount > 0")
```
Unqualified names go to the default schema.

## Legacy LIVE schema
Older pipelines referenced datasets with `LIVE.table` and published to one target schema. In default publishing mode `LIVE` is not needed; see the LIVE schema (legacy) section of the Unity Catalog pipelines page for migration. Test in a copy.

## Ownership and permissions
- Grant consumers SELECT on streaming tables / MVs as with normal tables.

## Gotchas
- Existing Hive metastore pipelines cannot be upgraded to Unity Catalog, and a single pipeline cannot write to both; create a new UC pipeline (the docs describe cloning a Hive metastore pipeline) and backfill.

## Verify
Consumers can SELECT the published tables with only the privileges granted to them.

## Checked

- 2026-10-28: confirmed on the Unity Catalog pipelines page (default publishing mode, pipelines created before February 5, 2025 may use legacy mode and the LIVE virtual schema, Hive metastore pipelines cannot be upgraded or write to Unity Catalog) and the target schema page.
- Removed: owner and run-as privilege lists, table ownership and pipeline deletion claims, and the `DESCRIBE EXTENDED` check (not in the fetched pages).

Method: documentation only; no commands were run.
