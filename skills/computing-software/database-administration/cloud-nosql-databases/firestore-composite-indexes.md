---
id: computing-software.database-administration.cloud-nosql-databases.firestore-composite-indexes
name: firestore-composite-indexes
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-composite-indexes, firestore-queries-indexes, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Create indexes so queries run, and manage them as code."
sources:
  - https://firebase.google.com/docs/firestore/query-data/index-overview
  - https://firebase.google.com/docs/reference/firestore/indexes
  - https://firebase.google.com/docs/firestore/query-data/indexing
  - https://firebase.google.com/docs/firestore/best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composite and single-field indexes

**Goal:** Create indexes so queries run, and manage them as code.

## Steps
- Automatic (single-field) indexes are built per field: ascending and descending for non-array, non-map fields, array-contains for arrays. A compound query with a range clause that has no matching composite index fails with an error.
- Define in firestore.indexes.json: {"indexes":[{"collectionGroup":"orders","queryScope":"COLLECTION","fields":[{"fieldPath":"status","order":"ASCENDING"},{"fieldPath":"createdAt","order":"DESCENDING"}]}]} and deploy with firebase deploy --only firestore (indexes and rules); list deployed indexes with firebase firestore:indexes.
- The error message of a failing compound query includes a link that opens the Firebase console to create the missing index; indexes can take a few minutes to build.
- Exempt fields you never query with a fieldOverrides entry that has an empty indexes array (collectionGroup, fieldPath, indexes: []).

## Gotcha
Index fanout is the main contributor to write latency and adds storage; exemptions reduce this for fields never queried. Limits: 40,000 index entries per document, and 200 composite indexes per database (1000 with billing enabled).

## Verify
- [ ] The firestore.indexes.json in source control matches the console, and each production query runs without an index error.

## Checked

2026-11-03. Confirmed on the Firestore index overview, Managing indexes, Firestore indexes reference (JSON fields collectionGroup, queryScope, fields, fieldPath, order, fieldOverrides; deploy with --only firestore; firebase firestore:indexes), Best practices (index fanout, exemptions) and Usage and limits (40,000 entries, 200/1000 composite indexes) pages. Removed: the claim that the deploy target is firestore:indexes (the docs show --only firestore). The createdAt/status/orders names in the JSON example are illustrative.

Method: documentation only; no commands were run.
