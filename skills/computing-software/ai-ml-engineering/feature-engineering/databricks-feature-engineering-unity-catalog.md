---
id: computing-software.ai-ml-engineering.feature-engineering.databricks-feature-engineering-unity-catalog
name: databricks-feature-engineering-unity-catalog
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, databricks-feature-store, unity-catalog, feature-engineering-client, feature-lookup, online-tables, databricks]
level: practitioner
status: draft
description: "Use Databricks Feature Engineering in Unity Catalog: feature tables with primary and timeseries keys, FeatureLookup training sets, point-in-time joins, online serving and lineage."
sources:
  - https://docs.databricks.com/en/machine-learning/feature-store/index.html
  - https://docs.databricks.com/en/machine-learning/feature-store/time-series.html
  - https://docs.databricks.com/en/machine-learning/feature-store/train-models-with-feature-store.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Databricks Feature Engineering in Unity Catalog

Any Delta table in Unity Catalog with a primary key constraint can serve as a feature table. The `databricks-feature-engineering` client builds training sets, logs models with feature metadata and enables automatic lookup at serving time.

## Create a feature table
```python
from databricks.feature_engineering import FeatureEngineeringClient
fe = FeatureEngineeringClient()
fe.create_table(name="ml.features.customer_daily", primary_keys=["customer_id", "ts"], timeseries_column="ts",
                df=features_df, description="Daily customer aggregates")
fe.write_table(name="ml.features.customer_daily", df=new_df, mode="merge")     # upsert
```
SQL alternative: `ALTER TABLE ... ADD CONSTRAINT pk PRIMARY KEY (customer_id, ts TIMESERIES)`.

## Training set with point-in-time lookup
```python
from databricks.feature_engineering import FeatureLookup
lookups = [FeatureLookup(table_name="ml.features.customer_daily", lookup_key="customer_id",
                         timestamp_lookup_key="event_ts",
                         feature_names=["spend_30d", "orders_30d"]),
           FeatureLookup(table_name="ml.features.customer_static", lookup_key="customer_id")]
ts = fe.create_training_set(df=labels_df, feature_lookups=lookups, label="churned", exclude_columns=["customer_id"])
train_pdf = ts.load_df().toPandas()
```
- With `timestamp_lookup_key`, each label row gets the latest feature values at or before its timestamp (AS OF join). `lookback_window` limits staleness.
- On-demand features: Python UDFs in Unity Catalog via `FeatureFunction` compute request-time features in training and serving.

## Log the model with feature metadata
```python
fe.log_model(model=clf, artifact_path="model", flavor=mlflow.sklearn, training_set=ts,
             registered_model_name="ml.models.churn")
preds = fe.score_batch(model_uri="models:/ml.models.churn/3", df=ids_df)   # looks up features automatically
```
Lineage (feature table -> model -> endpoint) appears in Catalog Explorer.

## Online serving
- Publish features to online storage (Databricks Online Tables / Lakebase-backed online feature stores, depending on workspace generation) synced from the Delta table (snapshot, triggered or continuous).
- Model Serving endpoints for models logged with `fe.log_model` look up online features by primary key automatically; requests only need the keys.
- Feature Serving endpoints expose feature lookups to non-ML applications.

## Practices
- Enable Change Data Feed on source tables for incremental sync.
- Separate catalogs/schemas for dev/prod; grant `SELECT` on feature tables to training principals.
- Workspace Feature Store (legacy, `hive_metastore`) is superseded; migrate to Unity Catalog tables.

## Verify
For sample label rows, check joined feature timestamps are <= label timestamps, and compare `score_batch` predictions with the online endpoint for the same keys.
