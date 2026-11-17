---
id: computing-software.ai-ml-engineering.mlops.distributed-batch-scoring-ray-data-spark
name: distributed-batch-scoring-ray-data-spark
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, batch-inference, ray-data, spark-batch-scoring, map-batches, pandas-udf, gpu-batch-inference]
level: practitioner
status: draft
description: "Score large datasets offline with Ray Data map_batches (stateful GPU actors) or Spark pandas UDFs: load models once, size batches, control parallelism and write idempotent outputs."
sources:
  - https://docs.ray.io/en/latest/data/batch_inference.html
  - https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.map_batches.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed batch scoring with Ray Data or Spark

## Ray Data (GPU models, Python-native pipelines)
```python
import ray, numpy as np
ds = ray.data.read_parquet("s3://lake/events/dt=2026-10-15/")

class Scorer:
    def __init__(self):                       # runs once per actor: load model here
        self.model = load_model("s3://models/churn/v7").to("cuda").eval()
    def __call__(self, batch: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        with torch.inference_mode():
            batch["score"] = self.model(to_tensor(batch)).cpu().numpy()
        return batch

out = ds.map_batches(Scorer, concurrency=8, num_gpus=1, batch_size=512)   # 8 GPU actors
out.select_columns(["id", "score"]).write_parquet("s3://lake/scores/model=v7/dt=2026-10-15/")
```
- Passing a **class** gives stateful actors (model loaded once); a function reloads per batch.
- `batch_size` trades GPU utilisation vs memory; increase until GPU memory is ~80% used.
- CPU preprocessing in a separate `map_batches` (function, CPU) lets Ray stream and overlap stages.
- LLM batch inference: Ray Data LLM processors wrap vLLM engines with the same pattern.

## Spark (data already in the lakehouse, CPU models)
```python
from pyspark.sql.functions import pandas_udf
from typing import Iterator
import pandas as pd

@pandas_udf("double")
def score(batches: Iterator[pd.DataFrame]) -> Iterator[pd.Series]:
    model = joblib.load("/dbfs/models/churn_v7.pkl")      # once per task, not per batch
    for pdf in batches:
        yield pd.Series(model.predict_proba(pdf[FEATURES])[:, 1])

df.withColumn("score", score(struct(*FEATURES))).write.mode("overwrite").partitionBy("dt").parquet(OUT)
```
- Iterator-of-DataFrames UDFs load the model once per task; scalar UDFs reload per batch.
- Tune `spark.sql.execution.arrow.maxRecordsPerBatch` (default 10,000) and repartition so each task is a few minutes.
- MLflow models: `mlflow.pyfunc.spark_udf(spark, model_uri, env_manager="local")` does the same.

## Output discipline
- Write to a path/partition keyed by model version and data date; overwrite that partition only (idempotent reruns).
- Include `model_version` and `scored_at` columns.
- Check row counts in = out, and score distribution vs previous run before publishing.

## Verify
- [ ] GPU utilisation during the job is high (not data-loader bound).
- [ ] Rerunning the same date produces the same row count and no duplicates.
