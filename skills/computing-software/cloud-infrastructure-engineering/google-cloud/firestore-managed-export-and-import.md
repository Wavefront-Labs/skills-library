---
id: computing-software.cloud-infrastructure-engineering.google-cloud.firestore-managed-export-and-import
name: firestore-managed-export-and-import
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, firestore, firestore-export-import, gcloud-firestore-export, datastore-export, bigquery-load]
level: practitioner
status: docs-checked
description: "Export and import Firestore data with gcloud: full and per-collection exports to Cloud Storage, IAM, scheduling, loading exports into BigQuery, and import caveats."
sources: ["https://docs.cloud.google.com/firestore/docs/manage-data/export-import", "https://docs.cloud.google.com/sdk/gcloud/reference/firestore/export", "https://docs.cloud.google.com/sdk/gcloud/reference/firestore/backups/schedules/create", "https://docs.cloud.google.com/bigquery/docs/loading-data-cloud-firestore"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firestore managed export and import

## Export
```bash
gcloud firestore export gs://fs-exports-<P>/$(date +%F) --database='(default)'
gcloud firestore export gs://fs-exports-<P>/orders-$(date +%F) --collection-ids=orders,customers
gcloud firestore operations list
gcloud firestore operations describe <OP>
```
- Use a bucket in a location near the database location; Requester Pays and Rapid buckets cannot be used.
- The Firestore service agent needs Storage Admin on the bucket (it has access by default if the bucket is in the same project); the caller needs a role such as Cloud Datastore Import Export Admin plus a Cloud Storage role such as Storage Admin.
- Without `--snapshot-time` an export may include changes made while it ran. With PITR enabled, `--snapshot-time` takes a whole-minute timestamp within the past seven days (for example `2026-10-20T10:20:00Z`) for a consistent view; the export fails if data no longer exists at that time.
- `--collection-ids` exports only the named collection groups (subcollections are not included automatically).

## Import
```bash
gcloud firestore import gs://fs-exports-<P>/2026-10-17 --database=restore-test
gcloud firestore import gs://fs-exports-<P>/2026-10-17 --collection-ids=orders
```
Import **overwrites** documents with the same IDs and leaves other documents in place. Data exported from one database can be imported into another (`--database`), which avoids clobbering production. Import operations do not trigger Cloud Functions; snapshot listeners do receive updates. Imports update indexes using the target database's current index definitions.

## Into BigQuery
Only exports made with a `--collection-ids` filter can be loaded. Point the load at the single `KIND_COLLECTION_ID.export_metadata` file (no wildcards; not `overall_export_metadata`); you cannot append to an existing table:
```bash
bq load --source_format=DATASTORE_BACKUP analytics.orders \
  gs://fs-exports-<P>/orders-2026-10-17/all_namespaces/kind_orders/all_namespaces_kind_orders.export_metadata
```

## Scheduling
For recovery, consider **scheduled backups** (`gcloud firestore backups schedules create --database=... --recurrence=daily|weekly --retention=7d`; weekly also needs `--day-of-week`) and PITR; managed export and import suits recovering from accidental deletion and exporting data for offline processing.

## Gotchas
- Exports incur one read per document exported (not shown in the console usage section); imports incur one write per document.
- Export files stay in the bucket until you delete them; use lifecycle rules on the bucket to expire old exports.
- Index definitions are not included in an export; recreate them from your index configuration.

## Verify
- [ ] Import into a scratch database and compare document counts per collection.

## Checked
Checked 2026-10-24 against the Firestore export and import documentation, the gcloud `firestore export` and `firestore backups schedules create` references and the BigQuery guide for loading Firestore exports (docs.cloud.google.com). Confirmed `--collection-ids`, `--snapshot-time` rules, `--database`, overwrite-on-import behaviour, no function triggers on import, billing, index handling, the `bq load --source_format=DATASTORE_BACKUP` metadata-file rule and the scheduled-backup flags. Removed the service-agent email address, the exact role ID, the Cloud Scheduler recipe and the claim about same-location buckets, which the pages do not state in that form.
Method: documentation only; no commands were run.
