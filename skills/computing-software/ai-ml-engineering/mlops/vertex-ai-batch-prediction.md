---
id: computing-software.ai-ml-engineering.mlops.vertex-ai-batch-prediction
name: vertex-ai-batch-prediction
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, vertex-batch-prediction, vertex-ai, batch-inference, bigquery, gcs]
level: practitioner
status: draft
description: "Run Vertex AI batch prediction jobs from GCS JSONL or BigQuery: instance config to keep keys, machine and replica sizing, explanations, error files and output joins."
sources:
  - https://cloud.google.com/vertex-ai/docs/predictions/get-batch-predictions
  - https://cloud.google.com/vertex-ai/docs/predictions/batch-prediction-instance-config
  - https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.Model#google_cloud_aiplatform_Model_batch_predict
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Vertex AI batch prediction

**Goal:** score millions of rows with a registered Vertex model without standing up an endpoint, and join results back to source records reliably.

## Submit
```python
from google.cloud import aiplatform
model = aiplatform.Model("projects/P/locations/us-central1/models/churn@3")
job = model.batch_predict(
    job_display_name="churn-2026-10-18",
    bigquery_source="bq://P.features.churn_scoring_20261018",
    bigquery_destination_prefix="bq://P.predictions",
    instances_format="bigquery", predictions_format="bigquery",
    machine_type="n1-standard-8", starting_replica_count=2, max_replica_count=20,
    instance_config={"key_field": "customer_id", "excluded_fields": ["customer_id"]},
    service_account=BATCH_SA, sync=False)
job.wait()
```
GCS form: `gcs_source=["gs://bucket/in/*.jsonl"]`, `instances_format="jsonl"`, `gcs_destination_prefix="gs://bucket/out/"`.

## Keep the join key
Without a key, output rows are matched by order, which is fragile. `instance_config.key_field` passes a key through to the output while `excluded_fields` keeps it out of the model input. Alternatively `included_fields` selects exactly the model features.

## Sizing and cost
- No endpoint needed; you pay for the job's machines only while it runs.
- Startup takes minutes (provisioning + model load), so batch prediction suits large jobs, not small frequent ones.
- `max_replica_count` bounds parallelism and cost; GPU models add `accelerator_type`/`accelerator_count`.
- Custom containers must implement the same predict route as online serving.

## Outputs and errors
- BigQuery: a `predictions_<timestamp>` table plus an errors table; GCS: `prediction.results-*` and `prediction.errors_stats-*` files.
- Always check error counts: the job can SUCCEED with some rows failed. Fail the pipeline if errors exceed a small threshold.
- `generate_explanation=True` adds feature attributions (model must have an explanation spec) at significant extra cost.

## In pipelines
Use the `ModelBatchPredictOp` component from Google Cloud Pipeline Components inside Vertex Pipelines, followed by a validation step (row counts, null predictions, score distribution) before publishing.

## Verify
- [ ] Output row count equals input row count minus logged errors.
- [ ] Results join to source by key without duplicates.
- [ ] Job metadata (model version, input table) recorded with the output table.
