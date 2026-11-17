---
id: computing-software.cloud-infrastructure-engineering.google-cloud.centralised-logging-project-and-audit-log-retention
name: centralised-logging-project-and-audit-log-retention
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, landing-zone, logging-project, centralized-logging-project, audit-log-export, audit-log-bigquery, aggregated-sinks, log-buckets, bucket-lock]
level: practitioner
status: docs-checked
description: "Build the central logging project: org aggregated audit-log sinks into a log bucket with Observability Analytics, BigQuery, and a locked GCS bucket for multi-year retention."
sources: ["https://docs.cloud.google.com/logging/docs/central-log-storage", "https://docs.cloud.google.com/logging/docs/export/aggregated_sinks", "https://docs.cloud.google.com/logging/docs/buckets", "https://docs.cloud.google.com/storage/docs/bucket-lock"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Centralised logging project and long-term audit retention

One project (`prj-c-logging`) owns all org-wide log storage; only security/audit groups read it.

## 1. Log bucket for day-to-day search (Observability Analytics)
```bash
LP=<LOGGING_PROJECT>
gcloud logging buckets create org-audit --project=$LP --location=europe-west2 \
  --retention-days=400 --enable-analytics
gcloud logging sinks create org-audit-to-bucket \
  logging.googleapis.com/projects/$LP/locations/europe-west2/buckets/org-audit \
  --organization=<ORG_ID> --include-children \
  --log-filter='logName:"cloudaudit.googleapis.com"'
WI=$(gcloud logging sinks describe org-audit-to-bucket --organization=<ORG_ID> --format='value(writerIdentity)')
gcloud projects add-iam-policy-binding $LP --member=$WI --role=roles/logging.bucketWriter
gcloud logging links create org_audit_bq --bucket=org-audit --location=europe-west2 --project=$LP  # read-only BigQuery view
```

## 2. BigQuery export (if you need joins, scheduled reports, longer SQL retention)
```bash
bq --location=EU mk -d $LP:audit_logs
gcloud logging sinks create org-audit-to-bq bigquery.googleapis.com/projects/$LP/datasets/audit_logs \
  --organization=<ORG_ID> --include-children --use-partitioned-tables \
  --log-filter='logName:"cloudaudit.googleapis.com"'
# grant the new writerIdentity roles/bigquery.dataEditor on the dataset
```
The sink destination must be a write-enabled dataset, never the read-only linked dataset from step 1.

## 3. Immutable archive for compliance (years)
```bash
gcloud storage buckets create gs://<org>-audit-archive --project=$LP --location=EU \
  --default-storage-class=ARCHIVE --uniform-bucket-level-access --public-access-prevention
gcloud storage buckets update gs://<org>-audit-archive --retention-period=<DURATION>   # e.g. years; see the gcloud reference for the format
gcloud logging sinks create org-audit-to-gcs storage.googleapis.com/<org>-audit-archive \
  --organization=<ORG_ID> --include-children --log-filter='logName:"cloudaudit.googleapis.com"'
# grant writerIdentity roles/storage.objectCreator; after verification:
gcloud storage buckets update gs://<org>-audit-archive --lock-retention-period   # irreversible
```
Cloud Storage sinks are processed hourly, and a new one can take several hours to start routing.

## Gotchas
- The `_Required` bucket's retention cannot be changed, and retention of a bucket in a folder or organization cannot be extended; route to a bucket in a project (as above) to set your own retention. The org sink adds central copies, it does not move the originals.
- Data Access logs can be large; exclude noisy services with sink filters before routing them to BigQuery.
- Set the org default log storage region (`gcloud logging settings update --organization=<ORG_ID> --storage-location=<REGION>`) for residency.
- Locking a log bucket (`gcloud logging buckets update ... --locked`) is irreversible, and the bucket cannot be deleted until every entry has met its retention period; add a project lien to guard against accidental project deletion. Upgrading a bucket to analytics (`--enable-analytics`) also cannot be undone.

## Verify
- [ ] A fresh admin action in any project appears in the log bucket, and in the Cloud Storage archive after the hourly sink run.
- [ ] `gcloud storage buckets describe gs://<org>-audit-archive --format='value(retentionPolicy)'` shows `isLocked: true`.
- [ ] Only audit groups hold read roles on the logging project.

## Checked
2026-10-31. Confirmed on the Cloud Logging routing overview, buckets, aggregated sinks and sink export pages: _Required retention fixed and folder/org bucket retention cannot be extended (route to a project bucket), bucket lock is irreversible and blocks deletion until entries age out (use a project lien), Observability Analytics upgrade cannot be changed or removed, Cloud Storage sinks processed hourly and may take several hours to start, writer roles (bucketWriter, objectCreator, dataEditor), linked BigQuery datasets are read-only, partitioned tables option. Removed: the VPC flow-log filter term, the `--default_partition_expiration` flag, the sharded-table sentence, the `7y` value and `bigquery.dataViewer` (unconfirmed). Commands checked with check_commands.py.
Method: documentation only; no commands were run.
