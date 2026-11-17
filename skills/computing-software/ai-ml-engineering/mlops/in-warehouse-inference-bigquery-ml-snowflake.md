---
id: computing-software.ai-ml-engineering.mlops.in-warehouse-inference-bigquery-ml-snowflake
name: in-warehouse-inference-bigquery-ml-snowflake
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, bigquery-ml, snowflake-ml, in-database-inference, ml-predict, batch-inference]
level: practitioner
status: draft
description: "Score data where it lives: BigQuery ML trained, imported (ONNX/XGBoost/TensorFlow) and remote models with ML.PREDICT, and Snowflake Model Registry inference."
sources:
  - https://cloud.google.com/bigquery/docs/bqml-introduction
  - https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict
  - https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx
  - https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# In-warehouse inference (BigQuery ML, Snowflake)

**Goal:** batch predictions run as SQL next to the data, avoiding export pipelines, with model versions tracked.

## BigQuery ML native models
```sql
CREATE OR REPLACE MODEL `ml.churn_bt`
OPTIONS (model_type = 'BOOSTED_TREE_CLASSIFIER', input_label_cols = ['churned'],
         data_split_method = 'CUSTOM', data_split_col = 'is_eval') AS
SELECT * EXCEPT(customer_id) FROM `features.churn_training`;

SELECT * FROM ML.EVALUATE(MODEL `ml.churn_bt`);
SELECT customer_id, predicted_churned, predicted_churned_probs
FROM ML.PREDICT(MODEL `ml.churn_bt`, (SELECT * FROM `features.churn_scoring` WHERE dt = '2026-10-18'));
```
`TRANSFORM` clause in `CREATE MODEL` bakes preprocessing into the model so predict applies it automatically. `ML.EXPLAIN_PREDICT` adds per-row attributions.

## Imported models
Train anywhere, score in BigQuery:
```sql
CREATE OR REPLACE MODEL `ml.churn_onnx` OPTIONS (model_type = 'ONNX', model_path = 'gs://ml/churn/v7/model.onnx');
```
Also `model_type='XGBOOST'`, `'TENSORFLOW'`, `'TENSORFLOW_LITE'`. Size limits apply (check current docs); input column names must match the model's input names. sklearn pipelines convert via `skl2onnx`; verify predictions match the original on a sample.

## Remote models
`CREATE MODEL ... REMOTE WITH CONNECTION `us.vertex_conn` OPTIONS (endpoint = '<vertex endpoint url>')` calls a Vertex endpoint per batch of rows; LLM remote models are used with `ML.GENERATE_TEXT`. Remote calls cost endpoint time and are subject to quotas - throttle large tables.

## Snowflake
```python
from snowflake.ml.registry import Registry
reg = Registry(session=session, database_name="ML", schema_name="MODELS")
mv = reg.log_model(sk_pipeline, model_name="churn", version_name="v7", sample_input_data=X_sample)
preds = mv.run(session.table("FEATURES.CHURN_SCORING"), function_name="predict_proba")
preds.write.save_as_table("PREDICTIONS.CHURN_20261018", mode="overwrite")
```
Logged models become warehouse functions callable from SQL as well; set a default version so SQL callers do not hard-code versions.

## Operating it
- Schedule with scheduled queries / Snowflake tasks or the orchestrator; write to dated partitions.
- Record model name and version in the output table.
- Warehouse compute cost scales with data scanned and model complexity; partition and filter inputs.

## Verify
- [ ] Imported model predictions equal the original framework's on a sample (within float tolerance).
- [ ] Output tables carry model version and run date.
