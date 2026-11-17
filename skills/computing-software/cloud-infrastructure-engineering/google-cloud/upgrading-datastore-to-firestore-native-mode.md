---
id: computing-software.cloud-infrastructure-engineering.google-cloud.upgrading-datastore-to-firestore-native-mode
name: upgrading-datastore-to-firestore-native-mode
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, firestore, datastore-to-firestore-upgrade, firestore-migration, datastore-mode, app-engine]
level: advanced
status: docs-checked
description: "Move legacy Cloud Datastore workloads onto Firestore: what the automatic upgrade did, Datastore compatibility vs Native mode, concurrency modes, and when the type can change."
sources: ["https://docs.cloud.google.com/datastore/docs/firestore-or-datastore", "https://docs.cloud.google.com/datastore/docs/concepts/transactions", "https://docs.cloud.google.com/firestore/native/docs/manage-databases"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Datastore to Firestore

Legacy Cloud Datastore databases were upgraded to **Firestore in Datastore mode**: Datastore
compatibility is an API layer on top of Firestore with the same availability, performance,
consistency and scalability. Native mode is the full Firestore API (collection/document model,
real-time updates, mobile and web client libraries). A Datastore-mode database blocks Firestore
API requests, uses Datastore indexes instead of Firestore indexes and has no real-time updates.

## 1. Decide the target mode
| Keep Datastore mode | Move to Native mode |
|---|---|
| Legacy App Engine app built on the Datastore API | Need real-time listeners, mobile/web client libraries, richer queries and index types |

Mode is chosen per database, and you do not need it for every database in a project. The type can
be changed (`gcloud firestore databases update --type=...`) **only while the database is empty**,
so use a new named database for the new mode:
```bash
gcloud firestore databases create --database=app-native --location=<LOCATION> --type=firestore-native
```

## 2. Concurrency mode of upgraded databases
Upgraded databases that depended on entity-group semantics were initially set to
`OPTIMISTIC_WITH_ENTITY_GROUPS`, which limits transactions to 25 entity groups and writes to an
entity group to 1 per second. Changing the project's concurrency mode to `OPTIMISTIC` removes
those limits, but the Remote API library needs entity groups and will not work in
`OPTIMISTIC`. Test on a test project first (see the transactions page).

## 3. Migrate the data
Migration between modes is a new-database move: export from the source database, import into the
target, compare per-collection counts, and plan a write freeze or dual-write cutover. Check the
Firestore export/import page for which export formats each mode accepts before relying on a
cross-mode import; this skill does not assert it.
```bash
gcloud datastore export gs://<BUCKET>/ds-export --project=<P>
```

## 4. Rewrite access code
- Datastore client calls become Firestore client calls on the new data model.
- Rebuild indexes in the Firestore format; `gcloud datastore indexes` and `gcloud firestore indexes` manage different index definitions.
- Add security rules if clients read directly.

## Verify
- [ ] `gcloud firestore databases describe --database=app-native` shows the intended database type; document counts per collection match the source kinds.

## Checked
2026-10-31. Confirmed against "Choose between Firestore APIs" (Datastore compatibility is a database-level API layer, uses Datastore indexes, no real-time), the Datastore transactions page (concurrency modes, 25 entity groups, 1 write per second per entity group, Remote API note, upgrade history) and "Manage databases" (`--type` values, type changeable only if the database is empty). Removed: the claim that a Datastore export imports into a Native database, the `nam5` location, the Key-to-document-path mapping, the per-document write rate and the export-consistency statements (not confirmed in fetched pages).
Method: documentation only; no commands were run.
