---
id: computing-software.data-engineering.data-warehouse-architecture.serving-ml-features-with-feature-stores
name: serving-ml-features-with-feature-stores
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-serving, feature-store, feast, point-in-time-join, online-store, offline-store, training-serving-skew, materialization]
level: practitioner
status: docs-checked
description: "Serve ML features consistently for training and inference: offline vs online stores, point-in-time joins, Feast definitions, materialization, skew checks."
sources:
  - https://docs.feast.dev/getting-started/concepts/overview
  - https://docs.feast.dev/getting-started/concepts/point-in-time-joins
  - https://docs.feast.dev/getting-started/concepts/data-ingestion
  - https://docs.feast.dev/reference/feast-cli-commands
  - https://docs.feast.dev/reference/online-stores
  - https://docs.databricks.com/aws/en/machine-learning/feature-store/
  - https://docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serving ML features (feature stores)

**Goal:** the model sees the same feature values in training as it will at inference, and online lookups are fast.

## 1. Two stores, one definition
- **Offline store** (warehouse/lakehouse tables: BigQuery, Delta, Parquet files) — full history for training with point-in-time joins.
- **Online store** (Feast supports Redis, DynamoDB, Bigtable, Cassandra, Postgres and others; Databricks Online Feature Store) — latest value per entity key for low-latency inference.
- One feature definition generates both, so logic is not reimplemented in the serving service — reimplementation is the classic cause of training/serving skew.

## 2. Point-in-time correctness
Training rows must use feature values known **at the label's timestamp**, not today's values (leakage).
```sql
-- for each label event, latest feature row at or before event time
SELECT l.*, f.orders_30d
FROM labels l
LEFT JOIN customer_features f
  ON f.customer_id = l.customer_id AND f.feature_ts <= l.event_ts
QUALIFY ROW_NUMBER() OVER (PARTITION BY l.label_id ORDER BY f.feature_ts DESC) = 1;
```
Add a TTL: ignore feature rows older than the feature's validity window (`f.feature_ts > l.event_ts - INTERVAL 7 DAY`). In Feast the TTL is relative to each entity-dataframe timestamp, not to the time you run the query. Feature stores implement this join; Feast also offers `filter_by_created_timestamp=True` on `get_historical_features` so backfilled or corrected values created after the event do not leak into training (not every offline store supports it; unsupported ones raise an error, and rows with a NULL created timestamp are excluded).

## 3. Feast example
```python
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64
customer = Entity(name="customer", join_keys=["customer_id"])
src = FileSource(path="s3://lake/features/customer_daily.parquet", timestamp_field="feature_ts")
customer_stats = FeatureView(name="customer_stats", entities=[customer], ttl=timedelta(days=7),
    schema=[Field(name="orders_30d", dtype=Int64), Field(name="avg_basket", dtype=Float32)], source=src)
```
```bash
feast apply                                             # register definitions
feast materialize-incremental $(date -u +%Y-%m-%dT%H:%M:%S)   # offline → online
```
```python
store.get_historical_features(entity_df=labels_df, features=["customer_stats:orders_30d"]).to_df()  # training
store.get_online_features(features=["customer_stats:orders_30d"], entity_rows=[{"customer_id": 42}]).to_dict()  # serving
```
Managed equivalents:
- **Databricks Feature Store** (Unity Catalog workspaces): Feature Views (recommended for new work, Databricks manages the pipelines) or feature tables you populate yourself; both can publish to the Online Feature Store. Model Serving can look up features automatically at inference, which avoids reimplementing feature logic.
- **Vertex AI Feature Store** (now documented under Gemini Enterprise Agent Platform): BigQuery tables or views are the offline store; an online store instance holds feature views served via Bigtable online serving. Optimized online serving is deprecated (sunset 17 Feb 2027), so choose Bigtable online serving. Resources must be in the same region as the BigQuery source.

## 4. Freshness and streaming features
- Batch features: materialize after the feature pipeline; monitor online-store age per feature view.
- Real-time features (last 5 min clicks): compute in a stream processor and push to the online store; log them at serve time so training uses what was actually served.
- On-demand features (computed from the request) live in the serving code but should be shared functions.

## 5. Skew and drift checks
- Log online feature values with predictions; compare distributions with offline values for the same entities/time (population stability index, null rates).
- Alert when online values are older than TTL (stale materialization).

## Verify
- [ ] Training set built with a point-in-time join, no future feature rows.
- [ ] Online and offline values match for a sample of entities at the same timestamp.
- [ ] Materialization freshness is monitored.

## Checked
2026-11-08: Read in full: Feast overview and point-in-time joins, Databricks and Vertex AI pages. Searched for the relevant sections only: Feast data ingestion, feature view, CLI reference and online stores index. Together they confirm `feast apply`, `feast materialize-incremental`, `get_historical_features`, `get_online_features`, `ttl`, `FileSource(timestamp_field=...)`, TTL semantics and `filter_by_created_timestamp`. Databricks Feature Store page and Vertex AI Feature Store overview confirm the managed-equivalent notes. Removed: the unsourced "single-digit ms" latency figure, SageMaker Feature Store mention, Snowflake as an offline store example, the old Databricks "online tables" wording. The generic SQL and the streaming/skew-check advice are method, not vendor claims. The Feast online-store list comes from the Feast online stores index (names only).
Method: documentation only; no commands were run.
