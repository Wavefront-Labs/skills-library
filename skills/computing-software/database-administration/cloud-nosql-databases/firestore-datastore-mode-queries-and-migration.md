---
id: computing-software.database-administration.cloud-nosql-databases.firestore-datastore-mode-queries-and-migration
name: firestore-datastore-mode-queries-and-migration
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-datastore-mode-queries-and-migration, firestore-datastore-mode, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Know what Datastore compatibility blocks and how import and TTL interact with it."
sources:
  - https://cloud.google.com/datastore/docs/firestore-or-datastore
  - https://firebase.google.com/docs/firestore/quotas
  - https://firebase.google.com/docs/firestore/ttl
  - https://firebase.google.com/docs/firestore/manage-data/export-import
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Datastore mode queries and migration

**Goal:** Operate Datastore mode and plan migration.

## Steps
- A Datastore-compatible database accepts Datastore API requests only and denies Firestore API requests.
- It uses Datastore indexes instead of Firestore indexes, which offer more index types and configurability.
- Managed bulk copy uses gcloud firestore export gs://BUCKET_NAME and gcloud firestore import gs://BUCKET_NAME/EXPORT_PREFIX/. When Datastore entities are imported into a Firestore database, numeric entity IDs appear as __id<number>__ document IDs.
- TTL cannot be used on a Datastore-mode database whose concurrency mode is Optimistic With Entity Groups; switch it to Optimistic concurrency first.

## Gotcha
Datastore compatibility blocks rich queries, Firestore index types and real-time capabilities. Use it only for apps that depend on the Datastore APIs.

## Verify
- [ ] The application uses only Datastore API calls against this database, and any TTL policy is accepted.

## Checked

2026-11-03. Confirmed on the Choose between Firestore APIs page, the Usage and limits page (imported Datastore numeric IDs), the TTL page (Optimistic With Entity Groups restriction) and the managed export and import page (command forms). Removed: entity group and ancestor details, index.yaml, projections, legacy-upgrade history and eventual-consistency claims, none of which the fetched pages state.

Method: documentation only; no commands were run.
