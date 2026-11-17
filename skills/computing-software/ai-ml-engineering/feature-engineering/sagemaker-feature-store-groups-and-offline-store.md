---
id: computing-software.ai-ml-engineering.feature-engineering.sagemaker-feature-store-groups-and-offline-store
name: sagemaker-feature-store-groups-and-offline-store
category: computing-software
field: ai-ml-engineering
product: feature-engineering
tags: [feature-engineering, sagemaker-feature-store, feature-groups, offline-store, athena, aws]
level: practitioner
status: draft
description: "Use SageMaker Feature Store: feature groups with record identifier and event time, ingestion, online reads, and point-in-time training sets from the offline store."
sources:
  - https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store.html
  - https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-create-feature-group.html
  - https://sagemaker.readthedocs.io/en/stable/api/prep_data/feature_store.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SageMaker Feature Store groups and offline store

## Concepts
- **Feature group**: schema plus `record_identifier_name` (entity key) and `event_time_feature_name` (when the value became true).
- **Online store**: low-latency latest record per key (standard or in-memory tier).
- **Offline store**: append-only history in S3 (Parquet or Iceberg table format) registered in Glue for Athena/Spark queries.

## Create and ingest
```python
import sagemaker, time
from sagemaker.feature_store.feature_group import FeatureGroup
sess = sagemaker.Session()
df["event_time"] = pd.Timestamp.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")    # string or fractional epoch
df["customer_id"] = df["customer_id"].astype("string")
fg = FeatureGroup(name="customer-features-v1", sagemaker_session=sess)
fg.load_feature_definitions(data_frame=df)           # infers String/Integral/Fractional
fg.create(s3_uri="s3://ml-feature-store/offline", record_identifier_name="customer_id",
          event_time_feature_name="event_time", role_arn=role, enable_online_store=True,
          table_format="Iceberg")
while fg.describe()["FeatureGroupStatus"] == "Creating": time.sleep(5)
fg.ingest(data_frame=df, max_workers=4, wait=True)   # PutRecord calls, writes online then offline
```
- pandas `object` columns break inference; cast to `string` dtype first.
- Offline writes land in S3 within minutes (asynchronous replication).
- For big backfills, write directly to the offline store via Spark (feature store Spark connector) or batch ingestion, not row-by-row PutRecord.

## Online read
```python
rt = boto3.client("sagemaker-featurestore-runtime")
rt.get_record(FeatureGroupName="customer-features-v1", RecordIdentifierValueAsString="C123",
              FeatureNames=["spend_30d", "orders_30d"])
rt.batch_get_record(Identifiers=[{"FeatureGroupName": "customer-features-v1",
                                  "RecordIdentifiersValueAsString": ["C1", "C2"]}])
```

## Point-in-time training sets
```python
from sagemaker.feature_store.feature_store import FeatureStore
from sagemaker.feature_store.dataset_builder import DatasetBuilder
fs = FeatureStore(sagemaker_session=sess)
builder = fs.create_dataset(base=labels_df, record_identifier_feature_name="customer_id",
                            event_time_identifier_feature_name="label_time",
                            output_path="s3://ml-datasets/churn/")
builder.with_feature_group(fg, target_feature_name_in_base="customer_id", included_feature_names=["spend_30d", "orders_30d"])
builder.point_in_time_accurate_join()
df_train, query = builder.to_dataframe()
```
Or write the Athena query yourself: join on key with `fg.event_time <= label.label_time`, take the latest row per (key, label_time), and exclude soft-deleted records (`is_deleted`).

## Gotchas
- Event time must be the time the value was valid, not ingestion time, or point-in-time joins are wrong.
- Records with older event time than the current online value don't overwrite online, but do append offline.
- Schema changes: add features with `fg.update(feature_additions=[...])`; removing/renaming requires a new group (version in the name).
- TTL on online records (`TtlDuration`) to expire stale features.

## Verify
For a few keys, compare the online record with the latest offline row (Athena) after replication; run the training-set query for a label date and confirm no feature event_time exceeds it.
