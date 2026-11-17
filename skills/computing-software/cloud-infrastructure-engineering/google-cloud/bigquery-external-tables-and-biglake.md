---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigquery-external-tables-and-biglake
name: bigquery-external-tables-and-biglake
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigquery, bigquery-external-tables, biglake, connections, iceberg]
level: advanced
status: docs-checked
description: "Query files in Cloud Storage from BigQuery: plain external tables vs BigLake tables, Cloud resource connections, hive partitioning, metadata caching, and Iceberg tables."
sources: ["https://cloud.google.com/bigquery/docs/external-data-cloud-storage", "https://cloud.google.com/bigquery/docs/biglake-intro", "https://cloud.google.com/bigquery/docs/create-cloud-resource-connection", "https://cloud.google.com/bigquery/docs/metadata-caching"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigQuery external tables and BigLake

BigLake tables use a **connection's** service account (access delegation), so you grant users access only to the table, not the bucket, and can enforce row-level and column-level security; the BigLake docs recommend them for external object stores.

## 1. Connection
```bash
bq mk --connection --location=EU --project_id=<P> --connection_type=CLOUD_RESOURCE lake-conn
bq show --connection <P>.eu.lake-conn          # note the connection's service account
gcloud storage buckets add-iam-policy-binding gs://<LAKE> \
  --member=serviceAccount:<CONN_SA> --role=roles/storage.objectViewer
```

## 2. BigLake table with hive partitions and metadata cache
```sql
CREATE EXTERNAL TABLE `<P>.lake.events`
WITH PARTITION COLUMNS (dt DATE)
WITH CONNECTION `<P>.eu.lake-conn`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://<LAKE>/events/*'],
  hive_partition_uri_prefix = 'gs://<LAKE>/events',
  require_hive_partition_filter = TRUE,
  max_staleness = INTERVAL 4 HOUR,
  metadata_cache_mode = 'AUTOMATIC');
```
- Partition pruning needs `dt=2026-10-16/` style paths and a filter on `dt`.
- Metadata caching has a staleness interval between 30 minutes and 7 days; the cache refreshes automatically (usually every 30 to 60 minutes) or manually with `CALL BQ.REFRESH_EXTERNAL_METADATA_CACHE(...)`. If the Cloud Storage bucket is regional, run the call in that location.
- To move an existing external table onto a connection, recreate it with `CREATE OR REPLACE EXTERNAL TABLE ... WITH CONNECTION`.

## 3. Iceberg
Cached metadata cannot be used with Apache Iceberg external tables: BigQuery already uses the metadata Iceberg records in its manifest files. See the BigLake documentation for the current Iceberg table options.

## Gotchas
- The Cloud Storage bucket must be in the same location as the dataset that contains the table.
- BigLake tables enforce row-level and column-level security (and dynamic data masking for Cloud Storage tables) because users never touch the bucket.

## Verify
- [ ] A user with only dataset `dataViewer` (no bucket access) can query the BigLake table; bytes processed reflect partition pruning.

## Checked

2026-10-27. Confirmed in the Cloud Storage external tables, BigLake intro, metadata caching and create cloud resource connection pages and the bq reference: `bq mk --connection --connection_type=CLOUD_RESOURCE`, `roles/storage.objectViewer` on the bucket, `WITH PARTITION COLUMNS`, `hive_partition_uri_prefix`, `require_hive_partition_filter`, `metadata_cache_mode` option, staleness interval 30 minutes to 7 days, automatic refresh every 30 to 60 minutes, `BQ.REFRESH_EXTERNAL_METADATA_CACHE`, `CREATE OR REPLACE EXTERNAL TABLE`, bucket in the same location as the dataset, access delegation with row and column security, no cached metadata for Iceberg. Removed: `serviceAccountId` field name, the `ALTER` claim, the Iceberg `format`/metadata path/managed-table details, the "plain external tables cannot be cached" and billing claims, the "only BigLake" masking claim, the "better performance" claim. Read end to end.

Method: documentation only; no commands were run.
