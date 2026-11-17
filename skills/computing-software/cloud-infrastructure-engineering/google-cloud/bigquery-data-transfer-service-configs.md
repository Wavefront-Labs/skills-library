---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigquery-data-transfer-service-configs
name: bigquery-data-transfer-service-configs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigquery, bigquery-data-transfer-service, dts, ingestion, dataset-copy]
level: practitioner
status: docs-checked
description: "Set up BigQuery Data Transfer Service configs for Cloud Storage, SaaS sources, S3 and dataset copies: schedules, service accounts, backfills, notifications and failure triage."
sources: ["https://cloud.google.com/bigquery/docs/dts-introduction", "https://cloud.google.com/bigquery/docs/working-with-transfers", "https://cloud.google.com/bigquery/docs/cloud-storage-transfer", "https://cloud.google.com/bigquery/docs/copying-datasets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigQuery Data Transfer Service

## 1. Create a transfer config
Cloud Storage → table, daily:
```bash
bq mk --transfer_config --project_id=<P> --target_dataset=raw --display_name=gcs-orders \
  --data_source=google_cloud_storage --schedule="every 24 hours" \
  --service_account_name=dts-loader@<P>.iam.gserviceaccount.com \
  --params='{"data_path_template":"gs://<B>/orders/{run_time|\"%Y%m%d\"}/*.csv","destination_table_name_template":"orders_{run_time|\"%Y%m%d\"}","file_format":"CSV","skip_leading_rows":"1","write_disposition":"APPEND"}'
```
Other `data_source` ids listed in the `bq mk --transfer_config` reference include `amazon_s3`, `azure_blob_storage`, `google_ads`, `youtube_channel`, `scheduled_query` and `cross_region_copy` (dataset copy). `write_disposition` accepts `APPEND` or `MIRROR`.

## 2. Dataset copy (move a dataset across regions/projects)
BigQuery uses the Data Transfer Service to copy datasets within or across regions (`data_source=cross_region_copy`). Create copies in the console or follow "Copy datasets" for the exact parameters. Only one transfer run is active per copy configuration at a time; further runs are queued.

## 3. Operate
```bash
bq ls --transfer_config --transfer_location=EU
bq ls --transfer_run --run_attempt=LATEST projects/<P>/locations/eu/transferConfigs/<ID>
bq mk --transfer_run --start_time=2026-10-01T00:00:00Z --end_time=2026-10-08T00:00:00Z projects/<P>/locations/eu/transferConfigs/<ID>   # backfill
bq ls --transfer_log projects/<P>/locations/eu/transferConfigs/<ID>/runs/<RUN>
```
Configure Pub/Sub or email run notifications so failures reach someone (`notification_pubsub_topic` on the transfer config, format `projects/<P>/topics/<TOPIC>`; the Data Transfer Service agent must keep the `pubsub.publisher` role).

## Gotchas
- Without a service account (`--service_account_name`), a config uses its owner's credentials; use a service account so transfers do not depend on one person.
- Cloud Storage transfers pick files up immediately (no minimum file age); in `APPEND` mode an unmodified file is loaded only once, and a changed modification time causes a reload.
- Files matching the URI must share the destination table's schema or the transfer fails.

## Verify
- [ ] The latest run succeeded; row counts in the destination match the source files for that run date.

## Checked

2026-10-27. Confirmed in the bq command-line reference (`bq mk --transfer_config`, `--transfer_run`, `bq ls --transfer_config/--transfer_run/--transfer_log/--run_attempt/--transfer_location`, data source ids), the Cloud Storage transfer page (parameter names, APPEND/MIRROR, no minimum file age, reload rule, same-schema rule), the copy datasets page (Data Transfer Service backend, one active run per copy configuration), the run notifications page (Pub/Sub, Data Transfer Service agent keeps `pubsub.publisher`) and the bigquerydatatransfer v1 TransferConfig schema (`notificationPubsubTopic`, `ownerInfo`). Removed: the "files younger than one hour are skipped" claim (the docs say there is no minimum file age), `bq show --transfer_log` (the documented command is `bq ls --transfer_log`), `--notification_pubsub_topic` (not a bq flag), the cross_region_copy parameter JSON, the TokenCreator claim and the location-match claim. Read end to end.

Method: documentation only; no commands were run.
