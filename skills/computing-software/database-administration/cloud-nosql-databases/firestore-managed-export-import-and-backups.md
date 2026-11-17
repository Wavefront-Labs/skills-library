---
id: computing-software.database-administration.cloud-nosql-databases.firestore-managed-export-import-and-backups
name: firestore-managed-export-import-and-backups
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-managed-export-import-and-backups, firestore-bundles-export, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Back up and restore Firestore data."
sources:
  - https://firebase.google.com/docs/firestore/manage-data/export-import
  - https://firebase.google.com/docs/firestore/backups
  - https://firebase.google.com/docs/firestore/use-pitr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed export, import and backups

**Goal:** Back up and restore Firestore data.

## Steps
- Managed export: gcloud firestore export gs://BUCKET_NAME (optionally --collection-ids=COLLECTION_GROUP_ID, comma-separated).
- Import: gcloud firestore import gs://BUCKET_NAME/EXPORT_PREFIX/ --database=DATABASE; imports keep the exported document IDs and overwrite existing documents with the same ID.
- Scheduled backups (Blaze plan): firebase firestore:backups:schedules:create --database '(default)' --recurrence 'DAILY' --retention 14w; retention can be up to 14 weeks, and each database can have one daily and one weekly schedule. A restore creates a new database, and a backup does not contain TTL policies.
- Point-in-time recovery (PITR) retains versions for seven days when enabled (one hour when disabled); export a PITR state with gcloud firestore export ... --snapshot-time=TIMESTAMP, a whole-minute timestamp in that window.

## Gotcha
An export is not an exact snapshot at the start time and may include changes made while it runs; for a consistent export enable PITR and use --snapshot-time.

## Verify
- [ ] A restore test into a new database matches document counts.

## Checked

2026-11-03. Confirmed on the managed export and import, Back up and restore data (scheduled backups) and Point-in-time recovery pages (command forms, overwrite behaviour, 14 week retention, one daily and one weekly schedule, restore to new database, 7 day / 1 hour PITR window, --snapshot-time, export not an exact snapshot). Removed: the gcloud backups schedules create command and 7d example, which the pages do not show (they use the Firebase CLI).

Method: documentation only; no commands were run.
