---
id: computing-software.ai-ml-engineering.feature-engineering.vertex-ai-feature-store
name: vertex-ai-feature-store
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, vertex-feature-store, bigquery, feature-online-store, feature-view, gcp]
level: practitioner
status: draft
description: "Serve features with Vertex AI Feature Store (BigQuery-backed): feature groups over BigQuery, online stores with Bigtable or optimized serving, feature view sync and online fetch."
sources:
  - https://cloud.google.com/vertex-ai/docs/featurestore/latest/overview
  - https://cloud.google.com/vertex-ai/docs/featurestore/latest/create-featureview
  - https://cloud.google.com/vertex-ai/docs/featurestore/latest/serve-feature-values
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vertex AI Feature Store

The current Vertex AI Feature Store keeps feature data **in BigQuery** (your tables/views are the offline store) and syncs selected features into an online store for low-latency serving. The older "Feature Store (Legacy)" with featurestores/entity types/ingestion jobs is a different API being retired: check which one a project uses.

## Prepare BigQuery source
A table or view with an entity ID column (`entity_id` or a named key), a `feature_timestamp` column, and feature columns. For time-series history, keep multiple rows per entity with timestamps; for latest-only serving, a view that selects the latest row.

## Online store and feature view
```python
from google.cloud.aiplatform_v1 import FeatureOnlineStoreAdminServiceClient
from google.cloud.aiplatform_v1.types import feature_online_store as fos, feature_view as fv
admin = FeatureOnlineStoreAdminServiceClient(client_options={"api_endpoint": f"{REGION}-aiplatform.googleapis.com"})
admin.create_feature_online_store(parent=f"projects/{P}/locations/{REGION}", feature_online_store_id="serving",
    feature_online_store=fos.FeatureOnlineStore(optimized=fos.FeatureOnlineStore.Optimized()))   # or bigtable=...
admin.create_feature_view(parent=f"projects/{P}/locations/{REGION}/featureOnlineStores/serving",
    feature_view_id="customer_v1",
    feature_view=fv.FeatureView(
        big_query_source=fv.FeatureView.BigQuerySource(uri=f"bq://{P}.features.customer_latest", entity_id_columns=["customer_id"]),
        sync_config=fv.FeatureView.SyncConfig(cron="0 */4 * * *")))
```
- **Optimized** online serving: lowest latency, supports embeddings and vector search (approximate nearest neighbour) on a feature view.
- **Bigtable** online serving: large data volumes, cost-efficient at scale, autoscaling nodes.
- Feature views can also reference registered **feature groups/features** (registry over BigQuery) instead of a raw source.
- Sync: scheduled cron, manual `sync_feature_view`, or continuous sync (for supported setups) for freshness.

## Fetch online
```python
from google.cloud.aiplatform_v1 import FeatureOnlineStoreServiceClient
from google.cloud.aiplatform_v1.types import feature_online_store_service as svc
data = FeatureOnlineStoreServiceClient(client_options={"api_endpoint": PUBLIC_ENDPOINT})
resp = data.fetch_feature_values(feature_view=FV_NAME, data_key=svc.FeatureViewDataKey(key="C123"))
```
Optimized stores expose a dedicated public endpoint (or Private Service Connect); use it, not the regional one.

## Training data
Because features live in BigQuery, build point-in-time training sets with SQL: join labels to feature history on key with `feature_timestamp <= label_time`, pick the latest per key/label (`QUALIFY ROW_NUMBER() OVER (PARTITION BY key, label_time ORDER BY feature_timestamp DESC) = 1`). The Vertex AI SDK/BigFrames offer helpers for point-in-time lookup.

## Gotchas
- Latest-value semantics: online returns the latest synced row per entity; stale if sync lags. Monitor sync job status.
- Region: online store, feature views and BigQuery dataset should be co-located.
- IAM: service accounts need BigQuery read on sources and Vertex AI user for serving.
- Costs: Bigtable nodes and optimized store nodes bill continuously; size and autoscale accordingly.

## Verify
After a sync, fetch a few keys and compare with `SELECT ... WHERE customer_id = 'C123'` on the source view; alert on sync failures and on fetch latency SLOs.
