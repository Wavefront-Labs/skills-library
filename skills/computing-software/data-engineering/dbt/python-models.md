---
id: computing-software.data-engineering.dbt.python-models
name: python-models
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-python-models, snowpark, pyspark, dataproc, databricks, dbt-ref-python, python-packages, incremental-python]
level: advanced
status: docs-checked
description: "Write dbt Python models: def model(dbt, session), dbt.ref/config, returning a DataFrame, packages, incremental Python, and when to prefer SQL."
sources:
  - https://docs.getdbt.com/docs/build/python-models
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dbt Python models

**Goal:** use Python (the open-source ecosystem, data science and statistics packages) inside the dbt DAG, with the same testing, documentation and lineage as any model.

## Support
Only data platforms with a fully featured Python runtime support them; check the adapter's page. Snowflake (Snowpark), BigQuery (BigFrames, or Spark via Dataproc) and Databricks (PySpark) are supported in dbt v2. All Python runs remotely on the platform, never locally in dbt.

## Shape
A `.py` file in `models/` defining `model(dbt, session)`, which must return a single DataFrame:
- Snowpark: Snowpark or pandas DataFrame. BigQuery: BigFrames, pandas or Spark. Databricks: Spark, pandas or pandas-on-Spark.
- `session` is the platform connection, always passed explicitly (even for PySpark).
```python
def model(dbt, session):
    dbt.config(materialized="table", packages=["numpy==1.23.1", "scikit-learn"])
    orders = dbt.ref("fct_orders")      # DataFrame; dbt.source("src", "tbl") for raw tables
    ...
    return final_df
```
- `dbt.ref()` and `dbt.source()` return DataFrames. Downstream SQL models can `ref()` the Python model. Referencing ephemeral models is not supported.
- Context available: `dbt.this` (also `.database`, `.schema`, `.identifier`), `dbt.is_incremental`, `dbt.config.meta_get()`. No Jinja renders the code, so context is limited.
- `dbt.config()` accepts only literals (strings, booleans, numbers) because dbt statically analyzes it at parse time. Put complex config in a properties YAML file.
- To use `var`, `env_var` or `target` in Python, set them in the YAML `config:` (for example `target_name: "{{ target.name }}"`) and read with `dbt.config.get("target_name")`.
- Declare `packages` (versions optionally pinned) so dbt tracks them; required on some platforms. Packages must be installed on the platform runtime.
- Functions defined in one model cannot be imported by other models.

## Materializations and incremental
`table` (default) and `incremental` only; not view, ephemeral, tests or snapshots. Incremental Python models support the same strategies as SQL on that adapter (BigQuery with Dataproc: `merge` yes, `insert_overwrite` not yet).
```python
    dbt.config(materialized="incremental")
    df = dbt.ref("upstream_table")
    if dbt.is_incremental:
        max_from_this = f"select max(updated_at) from {dbt.this}"
        df = df.filter(df.updated_at >= session.sql(max_from_this).collect()[0][0])
    return df
```

## When not to
- If a transformation can be written equally well in SQL, prefer SQL: more accessible and easier to make performant.
- Python models run slower and can cost more than SQL models.
- `print()` output does not appear in dbt logs; use platform logs, return a debug column in the DataFrame, or develop locally with DuckDB.
- pandas runs single-node and does not use distributed compute; pandas-on-Spark keeps the pandas API while parallelizing.

## Verify
- [ ] `dbt build -s <model>` runs and downstream SQL models can `ref` it.
- [ ] Data tests on the Python model's output pass.

## Checked

2026-11-09. Pages read in full against this skill:
- https://docs.getdbt.com/docs/build/python-models

Confirmed: the model signature, return types per platform, ref/source/this/is_incremental/config rules, materializations, incremental example, packages, limitations.
Removed or reworded: the Snowflake stored-procedure and Dataproc/serverless execution details, Postgres/Redshift claim, `python_version`, `create_dataframe`, `unique_key`, Snowflake memory limits and startup-time figures (not on the page), and the second source (snowflake-configs anchor), which was not read.

Method: documentation only; no commands were run.
