---
id: computing-software.ai-ml-engineering.mlflow.dataset-tracking-with-mlflow-data
name: dataset-tracking-with-mlflow-data
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, experiment-tracking, mlflow-data, dataset-tracking, log-input, data-lineage, dataset-digest]
level: practitioner
status: gated
description: "Record which data trained and evaluated each MLflow run with mlflow.data: dataset sources, digests, contexts, log_input, querying by dataset and reloading the exact data."
sources:
  - https://mlflow.org/docs/latest/tracking/data-api.html
  - https://mlflow.org/docs/latest/python_api/mlflow.data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataset tracking with mlflow.data

**Goal:** for any run or registered model, answer "which data, which version, which split?" and reload it.

## Log datasets as run inputs
```python
import mlflow, pandas as pd
src = "s3://lake/churn/v12/train.parquet"
train_df = pd.read_parquet(src)
train_ds = mlflow.data.from_pandas(train_df, source=src, name="churn-train", targets="churned")
eval_ds  = mlflow.data.from_pandas(eval_df, source="s3://lake/churn/v12/eval.parquet", name="churn-eval", targets="churned")
with mlflow.start_run():
    mlflow.log_input(train_ds, context="training", tags={"version": "v12"})
    mlflow.log_input(eval_ds, context="evaluation")
```
Other constructors: `from_numpy` (ran), `from_spark(df, path=..., table_name=..., version=...)` (Delta tables record the version), `from_huggingface`, `mlflow.data.load_delta(table_name=..., version=...)` (Spark, Hugging Face and S3 sources were not run (gated: unconfirmed, source is paywalled or blocked)).

Each dataset stores name, **digest** (hash of content sample/metadata), source, schema and profile (row count). The digest changes when data changes even if the path does not (tested: appending a row to the CSV changed the digest of `from_pandas` on the same path) - a cheap drift/lineage signal. Tested profile for a 10x2 frame: `{'num_rows': 10, 'num_elements': 20}`; context is stored as the dataset tag `mlflow.data.context`, which is why the example reads it from `di.tags`.

## Query and reload
```python
run = mlflow.get_run(run_id)
for di in run.inputs.dataset_inputs:
    print(di.dataset.name, di.dataset.digest, [t.value for t in di.tags if t.key == "mlflow.data.context"])
src = mlflow.data.get_source(run.inputs.dataset_inputs[0])
local_path = src.load()   # downloads/returns a LOCAL FILE PATH (tested: a str path for a local CSV), not a DataFrame
df = pd.read_csv(local_path)   # then read it with the matching reader
mlflow.search_runs(filter_string="datasets.digest = 'a1b2c3d4' and datasets.context = 'training'")
```

## Gotchas
- MLflow stores metadata and a reference, not a copy. If the source path is overwritten, reload returns different data (tested: the original 10-row CSV reloaded as 11 rows after an append) - point at immutable, versioned locations (Delta/Iceberg version, lakeFS commit, dated partition, object versioning).
- `mlflow.evaluate(data=dataset)` and autologging for some flavors log datasets automatically; avoid double-logging with different names (gated: unconfirmed, source is paywalled or blocked).
- Large Spark datasets: digest computation samples data; it is a change indicator, not a cryptographic guarantee.

## Verify
- [ ] Registered model -> source run -> training dataset digest and source are visible.
- [ ] Reloading via `get_source(...).load()` reproduces the row count logged in the profile.
