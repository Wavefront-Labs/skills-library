---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigquery-administration-and-cost-control
name: bigquery-administration-and-cost-control
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigquery, bigquery-admin, slots, bigquery-reservations, bigquery-editions, on-demand-pricing, capacity-pricing, autoscaling-slots, custom-quotas, maximum-bytes-billed, partitioning, clustering, table-expiration, storage-billing-model, physical-storage, information-schema, bigquery-iam, authorized-views, row-level-security, column-level-security, bi-engine]
level: practitioner
status: gated
description: "Administer BigQuery: on-demand vs editions and slot reservations, byte quotas, partition filters, storage billing model, INFORMATION_SCHEMA cost reports, authorized views."
sources: ["https://cloud.google.com/bigquery/docs/editions-intro", "https://cloud.google.com/bigquery/docs/reservations-intro", "https://cloud.google.com/bigquery/docs/custom-quotas", "https://cloud.google.com/bigquery/docs/best-practices-costs", "https://cloud.google.com/bigquery/docs/information-schema-jobs", "https://cloud.google.com/bigquery/docs/authorized-views", "https://cloud.google.com/bigquery/docs/row-level-security-intro"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BigQuery administration and cost control

**Goal:** analysts can query freely, nobody can spend $5k on one `SELECT *`, the heavy
pipelines run on reserved capacity, and every byte scanned is attributable.

## 1. Pricing model decision
- **On-demand**: $/TiB scanned, 2000-slot soft cap per project. Right for bursty, low-volume, or
  while you measure.
- **Editions** (Standard/Enterprise/Enterprise Plus) with **slot reservations**: pay per slot-hour,
  `--autoscale-max-slots` adds capacity on demand, optional 1-/3-year **commitments** for a baseline discount.
  Switch when monthly on-demand cost > equivalent slots, or when you need predictable throughput.
```bash
bq mk --reservation --project_id=<ADMIN_PROJECT> --location=EU --edition=ENTERPRISE \
   --slots=100 --autoscale_max_slots=400 pipelines
bq mk --reservation_assignment --project_id=<ADMIN_PROJECT> --location=EU \
   --reservation_id=<ADMIN_PROJECT>:EU.pipelines --assignee_type=FOLDER --assignee_id=<FOLDER_ID> --job_type=QUERY
```
- Assign at folder/org level; `--job_type=PIPELINE` for load/extract, `ML_EXTERNAL`, `BACKGROUND` for CDC.
- A reservation with 0 baseline + autoscale max = pure pay-per-use slots, often cheaper than on-demand for scan-heavy queries.
- Mixed: keep ad-hoc projects on-demand; assign ETL projects to the reservation. `assignee` with `--reservation_id=none` opts a project *out* of an inherited reservation.

## 2. Hard cost caps (do these first)
- **Custom quotas** (Console → IAM → Quotas → BigQuery API → *Query usage per day* / *per user per day*). Exceeding fails the query — the only true cap for on-demand.
- `maximum_bytes_billed` per job (`bq query --maximum_bytes_billed=1000000000`), enforced in Looker/connectors via job config defaults; a session/org default is not available, so bake it into tooling.
- Org policy / dataset default **table expiration** (`--default_table_expiration`) for scratch datasets; `--default_partition_expiration` on event tables.
- Storage: switch datasets with high compression to **physical storage billing** (`ALTER SCHEMA ds SET OPTIONS (storage_billing_model='PHYSICAL')`) after checking `INFORMATION_SCHEMA.TABLE_STORAGE` (`total_logical_bytes` vs `total_physical_bytes` (gated: unconfirmed, source is paywalled or blocked)); long-term storage pricing applies automatically to tables unmodified for 90 consecutive days.

## 3. Make tables cheap to scan
- **Partition** by ingestion time or a `DATE/TIMESTAMP/INT` column; `require_partition_filter=true` so a query without a `WHERE` on the partition column is rejected.
- **Cluster** by the high-cardinality filter/join columns (up to 4); clustering + partition pruning is where 90 % of savings live.
- Materialized views for repeated aggregates; **BI Engine** reservation (GiB) for dashboard latency.
- Query dry-run shows bytes: `bq query --dry_run` — teach it, and surface it in the console's validator.

## 4. Who spent what
```sql
SELECT user_email, project_id, SUM(total_bytes_billed)/POW(1024,4) AS tib_billed,
       SUM(total_slot_ms)/3600000 AS slot_hours, COUNT(*) AS jobs
FROM `region-eu`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) AND job_type='QUERY'
GROUP BY 1,2 ORDER BY tib_billed DESC LIMIT 50;
```
`JOBS_BY_ORGANIZATION` (gated: unconfirmed, source is paywalled or blocked) needs `roles/bigquery.resourceViewer` at org; `JOBS_TIMELINE` for slot contention; labels on jobs (`--label team:x`) for chargeback. Billing export (see `billing-accounts-and-budgets`) ties it to money.

## 5. Access model
- Dataset-level IAM (`roles/bigquery.dataViewer`), table/view-level IAM, and **authorized views/datasets** so consumers query a view without access to the source dataset: add the view (or whole dataset) as an `authorized view`/`authorized dataset` entry on the *source* dataset (console → Sharing → Authorize views, or `bq update --source` with an `access` entry of type `view`).
- **Row-level security**: `CREATE ROW ACCESS POLICY region_eu ON ds.t GRANT TO ('group:eu-analysts@example.com') FILTER USING (region = 'EU')`.
- **Column-level security**: Data Catalog policy tags on columns + `roles/datacatalog.categoryFineGrainedReader`; dynamic data masking rules on the same tags.
- `roles/bigquery.jobUser` in the *query* project + `dataViewer` on data projects is the standard analyst pair; `bigquery.user` adds dataset creation.
- Keep data and compute in the same **location** (EU vs europe-west1 are different); cross-region queries fail.

## Gotchas
- A reservation's slots are shared by every assignee; one runaway pipeline starves the dashboards — separate reservations per workload class, or set `--max_slots`/priorities (Enterprise+).
- `SELECT *` on a clustered table still scans every column; column pruning is the user's job (or a view).
- Daily custom quota resets at midnight Pacific, not local.
- Deleting a dataset deletes tables but 7-day time travel (`FOR SYSTEM_TIME AS OF`) and `bq cp` from snapshot can recover tables; **undelete dataset** exists for a window — act fast.
- Flat-rate (legacy) commitments cannot be mixed with editions in the same admin project without migration; migrate before renewal.

## Verify
- [ ] A query over the per-user quota fails with `Custom quota exceeded`; a `--maximum_bytes_billed` under the scan size fails before running.
- [ ] ETL project jobs show `reservation_id` set in `INFORMATION_SCHEMA.JOBS`; ad-hoc projects show null (on-demand) as intended.
- [ ] Top-10 cost query above is on a weekly dashboard; the biggest table has `require_partition_filter=true`.
- [ ] An EU analyst via the row access policy sees only EU rows; a policy-tagged column returns an error without the fine-grained reader role.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: example quota figures and the 'halves automatically' storage saving. Gated: the TABLE_STORAGE column names total_logical_bytes and total_physical_bytes, and the JOBS_BY_ORGANIZATION view name, were not found in the fetched pages.

Method: documentation only; no commands were run.
