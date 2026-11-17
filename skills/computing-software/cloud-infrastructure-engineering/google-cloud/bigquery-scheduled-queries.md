---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigquery-scheduled-queries
name: bigquery-scheduled-queries
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigquery, bigquery-scheduled-queries, dts, run-time-parameters, etl]
level: practitioner
status: docs-checked
description: "Schedule BigQuery SQL with run_time/run_date parameters, destination partitions, service accounts and notifications, backfill past runs, and know when to graduate to Dataform."
sources: ["https://cloud.google.com/bigquery/docs/scheduling-queries", "https://cloud.google.com/bigquery/docs/transfer-run-notifications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigQuery scheduled queries

Scheduled queries are Data Transfer Service configs with `data_source=scheduled_query`.

## 1. Create
`bq query --schedule=... --display_name=... --destination_table=...` works for SELECT-to-table queries
(with `{run_date}` templating in the table name, e.g. `daily_rollup_{run_date}`). Prefer DDL/DML in the SQL
itself so the destination is explicit and idempotent:
```bash
bq mk --transfer_config --data_source=scheduled_query --target_dataset='' \
  --display_name=daily_rollup --schedule="every day 03:00" \
  --service_account_name=sq-runner@<P>.iam.gserviceaccount.com --location=EU \
  --params='{"query":"DELETE FROM mart.daily_rollup WHERE dt = DATE_SUB(@run_date, INTERVAL 1 DAY); INSERT INTO mart.daily_rollup SELECT DATE_SUB(@run_date, INTERVAL 1 DAY) AS dt, store_id, SUM(amount) FROM raw.sales WHERE DATE(ts) = DATE_SUB(@run_date, INTERVAL 1 DAY) GROUP BY store_id"}'
```
- `@run_time` (TIMESTAMP, UTC) is the intended execution time, not the actual start, and `@run_date` (DATE) is the logical calendar date.
- Schedules are interpreted in UTC. Examples of valid formats from the API reference: `every 24 hours`, `1st,3rd monday of month 15:30`, `every wed,fri of jan,jun 13:15`, `first sunday of quarter 00:00`.

## 2. Backfill and notify
```bash
bq mk --transfer_run --start_time=2026-10-01T03:00:00Z --end_time=2026-10-10T03:00:00Z \
  projects/<P>/locations/eu/transferConfigs/<ID>
# notifications: set notification_pubsub_topic (projects/<P>/topics/sq-failures) on the transfer config through the API or console
```

## Gotchas
- Without a service account, a scheduled query runs with the credentials of the user who owns it; that user needs `bigquery.jobs.create` on the project.
- Delete+insert (or `MERGE`) keeps reruns idempotent; plain `INSERT` duplicates on retry.

## Verify
- [ ] `bq ls --transfer_run --run_attempt=LATEST <CONFIG>` shows SUCCEEDED; a rerun for the same date leaves row counts unchanged.

## Checked

2026-10-27. Confirmed in the scheduling queries page (`@run_time`, `@run_date`, DDL/DML support, user credentials need `bigquery.jobs.create`), the bq reference (`bq mk --transfer_config` flags including `--data_source`, `--target_dataset`, `--service_account_name`, `--params`, `--schedule`, `bq mk --transfer_run` with `--start_time`/`--end_time`, `bq ls --transfer_run --run_attempt`), the run notifications page and the bigquerydatatransfer v1 TransferConfig schema (schedule in UTC with example formats, `notificationPubsubTopic`). Removed: `bq update --notification_pubsub_topic` (not a documented bq flag), the Dataform/Workflows and dependency-chain advice, the claim that a backfill needs no care. Read end to end.

Method: documentation only; no commands were run.
