---
id: computing-software.ai-ml-engineering.feature-engineering.feast-feature-views-materialization-and-online-serving
name: feast-feature-views-materialization-and-online-serving
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, feast-materialize, feature-views, feast, online-store, feature-store]
level: practitioner
status: docs-checked
description: "Define Feast entities and feature views, apply the registry, materialize to the online store, and fetch online features and point-in-time training data."
sources:
  - https://raw.githubusercontent.com/feast-dev/feast/master/docs/getting-started/quickstart.md
  - https://raw.githubusercontent.com/feast-dev/feast/master/docs/getting-started/concepts/feature-view.md
  - https://raw.githubusercontent.com/feast-dev/feast/master/docs/getting-started/concepts/point-in-time-joins.md
  - https://raw.githubusercontent.com/feast-dev/feast/master/docs/getting-started/concepts/feature-retrieval.md
  - https://raw.githubusercontent.com/feast-dev/feast/master/docs/how-to-guides/running-feast-in-production.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feast feature views, materialization and online serving

## Definitions
`feature_store.yaml` configures the architecture of the feature store (provider, stores, registry); Python files hold the definitions. `feast apply` scans the Python files in the repo directory, registers the entity and feature view definitions, and commits them to the registry.
```python
from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64
driver = Entity(name="driver", join_keys=["driver_id"])
source = FileSource(path="data/driver_stats.parquet",
                    timestamp_field="event_timestamp", created_timestamp_column="created")
driver_stats_fv = FeatureView(
    name="driver_stats", entities=[driver], ttl=timedelta(days=1),
    schema=[Field(name="trips_today", dtype=Int64), Field(name="rating", dtype=Float32)],
    online=True, source=source, tags={"team": "driver_performance"})
```
- A feature view can carry an optional TTL, which limits how far back Feast looks when generating historical datasets, and free-form metadata via `tags`.
- Production guidance: keep definitions in a Git repository; run `feast plan` and `feast apply` from CI/CD when pull requests are opened or merged; use separate staging and production environments.

## Training data (point-in-time correct)
```python
training_df = store.get_historical_features(
    entity_df=entity_df,    # must include an event_timestamp column
    features=["driver_stats:trips_today", "driver_stats:rating"]).to_df()
```
`event_timestamp` is the inclusive upper bound for each entity row: Feast joins the latest feature values at or before it, which prevents leakage of future values. It scans backward from that timestamp up to the TTL; TTL is relative to each entity-row timestamp, not to the time you run the query.

## Materialize and serve online
```bash
feast materialize-incremental $CURRENT_TIME
```
`materialize-incremental` starts from each feature view's most recent materialization end date; on the first run it starts from now minus the view's `ttl`. Online reads:
```python
store = FeatureStore(repo_path=".")
vec = store.get_online_features(features=["driver_stats:trips_today"], entity_rows=[{"driver_id": 1001}]).to_dict()
```
- You orchestrate materialization yourself. Cron can be enough for a few infrequent jobs; Kubernetes Jobs or Airflow suit parallel work. The default in-process engine loads all the data being materialized into memory from the offline store. Feast keeps materialization history in the registry, so an Airflow worker needs read and write permission to the registry file.
- Event timestamps also ensure old feature values are not served online.
- `FeatureService` groups features for a model and can be passed to both `get_online_features` and `get_historical_features`, so training and serving use the same set.
- Fresh values can be pushed into Feast through the push API (data ingestion), to online or offline stores. Feast does not orchestrate batch transformation DAGs; the production guide points to Airflow plus dbt for that.

## Verify
- [ ] For a sample of entities, online values match historical retrieval at the current time (within materialization lag).
- [ ] Materialization jobs are scheduled and their success monitored.
- [ ] Training and serving reference the same FeatureService.

## Checked
Date: 2026-11-09.
- Confirmed in the Feast quickstart, feature view, point-in-time joins, feature retrieval and production guide pages (master branch docs): items above.
- Removed as unconfirmed: the example feature_store.yaml (S3 registry, aws provider, Snowflake and Redis stores, entity_key_serialization_version), `feast materialize` backfill example dates, `feast serve` feature server, StreamFeatureView, on-demand feature views, "values older than ttl return null online", the timezone-naive-as-UTC claim, the concurrent-apply registry advice, and the docs.feast.dev source URLs.
Method: documentation only; no commands were run.
