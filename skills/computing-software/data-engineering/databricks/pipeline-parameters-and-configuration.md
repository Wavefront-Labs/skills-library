---
id: computing-software.data-engineering.databricks.pipeline-parameters-and-configuration
name: pipeline-parameters-and-configuration
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, pipeline-parameters, lakeflow-declarative-pipelines, delta-live-tables, configuration]
level: practitioner
status: docs-checked
description: "Parameterise Lakeflow Declarative Pipelines (DLT) with configuration key-values: reading them in Python and SQL, per-environment values via bundles, and limits."
sources:
  - https://docs.databricks.com/aws/en/dlt/parameters
  - https://docs.databricks.com/aws/en/dev-tools/bundles/resources#pipelines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline parameters and configuration

**Goal:** one pipeline definition that runs in dev, staging and prod with different paths, catalogs and thresholds.

## Define in the pipeline settings
```yaml
# databricks.yml (bundle)
variables:
  source_path: {default: /Volumes/dev/raw/landing/orders}
  catalog: {default: dev}
resources:
  pipelines:
    orders:
      name: orders-${bundle.target}
      catalog: ${var.catalog}
      schema: sales
      configuration:
        orders.source_path: ${var.source_path}
        orders.min_amount: "0"
targets:
  prod:
    variables:
      catalog: prod
      source_path: /Volumes/prod/raw/landing/orders
```

## Read in Python
```python
from pyspark import pipelines as dp
src = spark.conf.get("orders.source_path")
min_amount = float(spark.conf.get("orders.min_amount", "0"))

@dp.table
def orders_bronze():
    return spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").load(src)
```

## Read in SQL
```sql
CREATE OR REFRESH STREAMING TABLE orders_bronze AS
SELECT * FROM STREAM read_files('${orders.source_path}', format => 'json');
```

## Rules
- Keys are strings; namespace them (`orders.`) to avoid clashing with Spark confs.
- Configuration values are read with `${key}` in SQL or `spark.conf.get("key")` in Python. Newer pipeline *parameters* use named parameter syntax and are SQL only; use configuration for Python.
- Values are read when an update runs: changing them needs a new update.
- Do not put secrets in configuration; keep them in a secret scope and read them in code.

## Gotchas
- `spark.conf.get` without a default raises if the key is missing; give defaults for optional keys.
- Configuration also carries Spark configuration values that control pipeline behaviour (for example `pipelines.enzyme.enabled`); see the pipeline properties reference.

## Verify
Dev and prod targets read from their respective paths and catalogs.

## Checked

- 2026-10-28: confirmed on the pipeline parameters page (configuration key-value pairs, `${key}` in SQL, `spark.conf.get` in Python, parameters are SQL only, configuration also sets Spark configuration values) and the bundle resources page.
- Fixed: the bundle example used `${var.catalog}` without defining it.
- Removed: serverless Spark conf claim, the secrets API name and the streaming-table full refresh advice.

Method: documentation only; no commands were run.
