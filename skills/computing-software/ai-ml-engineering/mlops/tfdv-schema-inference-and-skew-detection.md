---
id: computing-software.ai-ml-engineering.mlops.tfdv-schema-inference-and-skew-detection
name: tfdv-schema-inference-and-skew-detection
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, data-validation, tfdv, schema-inference, training-serving-skew, drift-comparator, tfx]
level: practitioner
status: docs-checked
description: "Use TensorFlow Data Validation: statistics, inferring a schema, validating new data, skew and drift comparators, and environments for serving data."
sources:
  - https://www.tensorflow.org/tfx/data_validation/get_started
  - https://www.tensorflow.org/tfx/tutorials/data_validation/tfdv_basic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TFDV schema inference and skew detection

**Goal:** catch schema anomalies, training-serving skew and drift on datasets. TFDV computes statistics with Apache Beam.

## Statistics and schema
```python
import tensorflow_data_validation as tfdv
train_stats = tfdv.generate_statistics_from_csv("train.csv")     # also generate_statistics_from_dataframe, generate_statistics_from_tfrecord
schema = tfdv.infer_schema(train_stats)
tfdv.display_schema(schema)
tfdv.write_schema_text(schema, "schema.pbtxt")
```
The inferred schema is a starting point to review: use `tfdv.get_feature(schema, name)` and `tfdv.get_domain(schema, name)` to edit presence (`min_fraction`) and expected domains, capturing domain knowledge TFDV cannot infer.

## Validate new data
```python
eval_stats = tfdv.generate_statistics_from_csv("new_batch.csv")
anomalies = tfdv.validate_statistics(statistics=eval_stats, schema=schema)
tfdv.display_anomalies(anomalies)
```
The result is an `Anomalies` protocol buffer.

## Environments
Features can be tied to environments with `default_environment`, `in_environment` and `not_in_environment`. Without an environment, a label missing from serving data shows up as an anomaly. The tutorial sets the default environment to both TRAINING and SERVING, marks the label feature as `not_in_environment` SERVING, and validates serving statistics with `environment="SERVING"`.

## Skew and drift
```python
tfdv.get_feature(schema, "payment_type").skew_comparator.infinity_norm.threshold = 0.01
anoms = tfdv.validate_statistics(train_stats, schema, serving_statistics=serving_stats)
```
- Skew compares training against serving statistics (`serving_statistics`); drift compares against an earlier span (`previous_statistics`) using `drift_comparator`.
- The L-infinity norm only detects skew for categorical features. Setting a `jensen_shannon_divergence` threshold on `skew_comparator` detects skew for both numeric and categorical features.
- Thresholds are set per feature on the schema.

## In TFX
The get-started page names the TFX components `StatisticsGen`, `SchemaGen` and `ExampleValidator` for running these steps in a pipeline.

## Checked
Method: docs-checked 2026-11-09 against the TFDV get-started guide and the tfdv_basic tutorial (downloaded HTML, searched for each function and read the skew, drift and environment sections). Dropped the example threshold values for specific features, the append-to-domain example, ImportSchemaGen, the blocking-downstream claim, and the ExampleValidator guide source (not read in detail).
