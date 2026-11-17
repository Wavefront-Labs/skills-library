---
id: computing-software.database-administration.cloud-nosql-databases.firestore-datastore-mode-differences
name: firestore-datastore-mode-differences
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-datastore-mode-differences, firestore-datastore-mode, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Choose between native mode and Datastore mode."
sources:
  - https://cloud.google.com/datastore/docs/firestore-or-datastore
  - https://firebase.google.com/docs/firestore/locations
  - https://firebase.google.com/docs/firestore/use-pitr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Datastore mode differences

**Goal:** Choose between native mode and Datastore mode.

## Steps
- Firestore API (native): collection and document data model, real-time updates, mobile and web client libraries, a strongly consistent storage layer, Firestore indexes and rich queries.
- Datastore mode (Datastore compatibility): a database-level setting for backwards compatibility. The database accepts Datastore API requests and denies Firestore API requests, uses Datastore indexes, and has no real-time capabilities. Recommended only for apps that depend on the Datastore APIs, such as legacy App Engine apps.
- Datastore compatibility is an option you choose when you create the database.
- You do not have to enable Datastore compatibility for every database in a project; extra databases need the Blaze plan.

## Gotcha
A Datastore-compatible database denies Firestore API requests, so its Firestore-only features (rich queries, Firestore index types, real-time updates) are unavailable.

## Verify
- [ ] gcloud firestore databases describe --database=DATABASE_ID shows the type field expected by the application (FIRESTORE_NATIVE in the documented example output).

## Checked

2026-11-03. Confirmed on the Choose between Firestore APIs page (compatibility is a database-level setting, denies Firestore API requests, Datastore indexes, no real-time, recommended for legacy App Engine), the Firestore locations page (multiple databases on Blaze) and the PITR page (describe output with type: FIRESTORE_NATIVE). Removed: the 1 write/sec and strong-consistency-by-default claims, the immutable-mode claim, the DATASTORE_MODE enum value, and the security-rules statement.

Method: documentation only; no commands were run.
