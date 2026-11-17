---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigquery-datasets-and-dataset-access
name: bigquery-datasets-and-dataset-access
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigquery, bigquery-datasets, dataset-access, authorized-views, iam]
level: practitioner
status: docs-checked
description: "Create BigQuery datasets with the right location, expiration and storage billing, and grant access with dataset IAM, authorized views/datasets and conditional bindings."
sources: ["https://cloud.google.com/bigquery/docs/datasets", "https://cloud.google.com/bigquery/docs/control-access-to-resources-iam", "https://cloud.google.com/bigquery/docs/authorized-datasets", "https://cloud.google.com/bigquery/docs/authorized-views"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigQuery datasets and dataset access

## 1. Create with deliberate settings
```bash
bq --location=EU mk --dataset \
  --default_partition_expiration=7776000 \
  --storage_billing_model=PHYSICAL --max_time_travel_hours=48 \
  --description="Curated sales marts" --label=env:prod \
  <P>:sales_mart
```
- **Location is permanent**: copy the dataset (Data Transfer Service dataset copy) to move it.
- `--default_partition_expiration` is in seconds (7776000 is 90 days) and applies to partitions of newly created partitioned tables; `--storage_billing_model=PHYSICAL` opts the dataset into physical storage billing (not possible if legacy flat-rate slot commitments exist in the same region); `--max_time_travel_hours` sets the time travel window.

## 2. Dataset-level IAM
```bash
bq show --format=prettyjson <P>:sales_mart > ds.json   # edit "access" list
bq update --source ds.json <P>:sales_mart
# or GoogleSQL DCL:
GRANT `roles/bigquery.dataViewer` ON SCHEMA `<P>.sales_mart` TO "group:analysts@example.com";
```
Users also need `bigquery.jobs.create` (for example through `roles/bigquery.jobUser`) in a project to run queries.

## 3. Share without exposing sources
- **Authorized view**: view in dataset B, authorized on dataset A; readers of B see view results, not A's tables.
- **Authorized dataset**: authorize all views in dataset B at once on A (fewer per-view updates).
Both are entries in dataset A's `access` list; edit them with the same `bq show` / `bq update --source` round trip. The user sharing needs `bigquery.datasets.get` and `bigquery.datasets.update` on dataset A.
- Row access policies and column policy tags narrow access further.

## Gotchas
- Project basic roles appear in a dataset's access list as special groups (`projectOwners`, `projectWriters`, `projectReaders`): remove them for sensitive datasets.
- `bq update --source` takes the whole edited JSON; start from the current `bq show --format=prettyjson` output.
- Default table expiration applies only to new tables.

## Verify
- [ ] `bq show --format=prettyjson <P>:sales_mart | jq .access` lists only intended principals; a test analyst can query the authorized view but not the base table.

## Checked

2026-10-27. Confirmed in the datasets, control access (IAM), authorized views and authorized datasets pages and the bq reference: `bq mk --dataset` flags `--default_partition_expiration` (seconds), `--default_table_expiration` (seconds), `--storage_billing_model`, `--max_time_travel_hours`, physical billing restriction with legacy flat-rate commitments, default expiry applies to newly created tables, `bq show` / `bq update --source` round trip, `GRANT ... ON SCHEMA` DCL, special groups `projectOwners`/`projectWriters`/`projectReaders`, `bigquery.jobs.create` / `roles/bigquery.jobUser`, authorized view and authorized dataset concepts, sharing permissions. Removed: `--default_table_expiration=0` (the page documents a one-hour minimum), the physical-billing-usually-wins advice and `TABLE_STORAGE` pointer, the 48-168 h time travel range, the `targetTypes` JSON and console path, the "that project pays" remark. Read end to end.

Method: documentation only; no commands were run.
