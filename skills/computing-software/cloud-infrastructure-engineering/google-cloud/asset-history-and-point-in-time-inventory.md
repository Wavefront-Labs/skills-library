---
id: computing-software.cloud-infrastructure-engineering.google-cloud.asset-history-and-point-in-time-inventory
name: asset-history-and-point-in-time-inventory
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-asset-inventory, asset-history, point-in-time-assets, forensics, change-tracking, bigquery]
level: practitioner
status: docs-checked
description: "Answer what a resource or IAM policy looked like at a past time: Cloud Asset get-history and snapshot-time exports within 35 days, and daily BigQuery snapshots for longer."
sources: ["https://cloud.google.com/asset-inventory/docs/get-asset-history", "https://cloud.google.com/asset-inventory/docs/export-asset-metadata", "https://cloud.google.com/sdk/gcloud/reference/asset/get-history"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asset history and point-in-time inventory

## 1. One resource: what changed and when (last 35 days)
```bash
gcloud asset get-history --project=<P> --content-type=resource \
  --asset-names=//compute.googleapis.com/projects/<P>/zones/<Z>/instances/web-1 \
  --start-time=2026-09-20T00:00:00Z --end-time=2026-10-16T00:00:00Z --format=json
# IAM policy history of a bucket
gcloud asset get-history --project=<P> --content-type=iam-policy \
  --asset-names=//storage.googleapis.com/<BUCKET> --start-time=2026-10-01T00:00:00Z
```
Each entry has a `window` (`startTime`, `endTime`) during which that version was current, and
`deleted: true` for deletions. `--start-time` is inclusive and must be within the last 35 days; `--end-time` is exclusive and defaults to now. Correlate a window start with
Admin Activity logs to find the actor.

## 2. Whole scope at a past instant
```bash
gcloud asset export --organization=<ORG_ID> --content-type=iam-policy \
  --snapshot-time=2026-10-10T12:00:00Z \
  --bigquery-table=projects/<P>/datasets/cai/tables/iam_20261010 --output-bigquery-force
```
`--snapshot-time` must be within the last 35 days. Check progress with
`gcloud asset operations describe <OPERATION>`.

## 3. Longer than 35 days: keep your own history
Schedule a daily export (Cloud Scheduler → Workflows or a Cloud Run job) per content type:
```bash
gcloud asset export --organization=<ORG_ID> --content-type=resource \
  --bigquery-table=projects/<P>/datasets/cai/tables/resource --per-asset-type \
  --partition-key=read-time --output-bigquery-force
```
`--partition-key=read-time` partitions the BigQuery table by read time (the API's `PartitionSpec` key `READ_TIME`), so each daily export can be selected by date. For change-level granularity add a real-time feed
(`gcloud asset feeds create`) to Pub/Sub → BigQuery.

## Gotchas
- History covers asset *metadata*, not data inside resources (object contents, table rows).
- `--per-asset-type` creates one table per asset type, with columns mapped from the nested fields of `Resource.data`.

## Verify
- [ ] `get-history` for a known-modified VM shows two windows with the change at the expected time.
- [ ] A SQL query on the daily partitions reproduces an IAM binding older than 35 days.

## Checked

2026-10-28. Confirmed against: gcloud `asset get-history` reference (start time within 35 days, inclusive; end time exclusive, defaults to now), the BigQuery export page (`--snapshot-time` no more than 35 days in the past; `--per-asset-type`; READ_TIME partition key), and the Cloud Asset API v1 discovery document (TemporalAsset `window` and `deleted`, PartitionSpec, BigQueryDestination).

Removed: the 100 asset-name limit, the history-enabled asset types claim, the export permission names, and the date-function SQL.

Method: documentation only; no commands were run.
