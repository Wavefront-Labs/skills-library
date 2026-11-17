---
id: computing-software.ai-ml-engineering.mlflow.batch-scoring-with-spark-udf
name: batch-scoring-with-spark-udf
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-deployment, spark-udf, batch-inference, pyspark, env-manager, distributed-scoring]
level: practitioner
status: docs-checked
description: "Score large tables with mlflow.pyfunc.spark_udf: column-to-signature mapping, result types, env_manager for executor dependencies, partition sizing and GPU models."
sources:
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html#mlflow.pyfunc.spark_udf
  - https://github.com/mlflow/mlflow/blob/master/mlflow/pyfunc/__init__.py
  - https://spark.apache.org/docs/latest/configuration.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Batch scoring with spark_udf

**Goal:** apply any MLflow model to millions of rows in parallel on a Spark cluster.

## Basic use
```python
import mlflow
from pyspark.sql.functions import struct, col
predict = mlflow.pyfunc.spark_udf(spark, model_uri="models:/churn@champion",
                                  result_type="double", env_manager="local")
scored = df.withColumn("churn_score", predict(struct(*[col(c) for c in feature_cols])))
scored.write.mode("overwrite").saveAsTable("ml.churn_scores")
```
- Pass columns as a `struct` so the model receives a DataFrame with those column names; plain positional arguments arrive as ordinal column names (0, 1, ...). If the model has a signature, the UDF can be called with no column arguments and then uses the signature's column names, so the DataFrame's column names must match it. Tensor inputs need a one-dimensional array column per tensor spec.
- `result_type`: a Spark `DataType` or DDL type string. Only primitive types, arrays of primitives, or a struct of those are allowed. If omitted it is inferred from the model signature's output schema, else `double`. For a non-array type the leftmost matching prediction column is returned; array types return all matching columns.
- Implemented as a Spark pandas UDF, so `predict` receives pandas DataFrames.

## Dependencies on executors
- `env_manager="local"` (the default when `prebuilt_env_uri` is not set): use the executors' current Python environment. MLflow warns that it may differ from the training environment and give errors or invalid predictions, so the library versions must match.
- `env_manager="virtualenv"`, `"uv"` or `"conda"`: MLflow recreates the model's logged environment inside the UDF only (the environment outside the UDF is unaffected). This takes extra time during execution and needs package access from the workers.
- `extra_env={...}` passes environment variables to the executors (for example `MLFLOW_SCORING_SERVER_REQUEST_TIMEOUT`); `params={...}` passes inference parameters to the model.

## Performance
- Repartition so that work is spread over all executor cores before scoring; one giant partition means one Python worker does everything.
- GPU models: request GPUs per task with Spark's task resource setting `spark.task.resource.gpu.amount`, so tasks do not oversubscribe a GPU.
- Databricks Serverless runs UDFs in a sandbox with a combined 1 GB memory and local disk limit and no GPUs, so models with large weights or GPU needs do not fit there.
- Very large models: consider a dedicated serving endpoint called in batches.

## Gotchas
- Column dtypes must satisfy the signature (int vs long vs double); cast before scoring.
- Signature enforcement errors appear in executor logs - check the Spark UI task errors when a job fails with a generic Python exception.
- Record model version in the output table (a literal column) for lineage.

## Verify
- [ ] A sample's scores equal local `pyfunc.load_model(...).predict` results.
- [ ] Output includes model version and scoring timestamp.
- [ ] Job time scales with cluster size (partitions not the bottleneck).

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- `spark_udf` signature and parameters (`result_type`, `env_manager` values virtualenv/uv/conda/local, `params`, `extra_env`, `prebuilt_env_uri`): mlflow/pyfunc/__init__.py docstring and code (default is local when `prebuilt_env_uri` is unset, though the docstring text says virtualenv).
- Struct/ordinal column naming, signature-name behaviour, tensor array columns, leftmost-column result rules and the Serverless 1 GB sandbox limit: same docstring.
- `spark.task.resource.{resourceName}.amount` exists: Apache Spark docs/configuration.md.
- Removed as unconfirmed: the 2-4x partition ratio, the `spark.sql.execution.arrow.maxRecordsPerBatch` default and advice, per-worker model-load claims, and the `mapInPandas` suggestion.

Method: documentation only; no commands were run.
