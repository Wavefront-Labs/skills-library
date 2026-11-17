---
id: computing-software.database-administration.cloud-nosql-databases.firestore-ttl-with-indexes-and-cleanup
name: firestore-ttl-with-indexes-and-cleanup
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-ttl-with-indexes-and-cleanup, firestore-ttl, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Combine TTL with query filters and cleanup."
sources:
  - https://firebase.google.com/docs/firestore/ttl
  - https://firebase.google.com/docs/firestore/best-practices
  - https://firebase.google.com/docs/firestore/manage-data/delete-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TTL, indexes and cleanup jobs

**Goal:** Combine TTL with query filters and cleanup.

## Steps
- Expired documents keep appearing in queries until TTL deletes them; add an expireAt > now filter to hide them.
- A TTL field can be indexed or unindexed. Standard edition indexes every field by default, and indexing a timestamp field can create hotspots at higher traffic; a single-field index exemption disables the index on a TTL field.
- TTL does not delete subcollections; because TTL deletes fire Cloud Firestore triggers, a Cloud Function on delete can remove children.
- For complex retention use a scheduled function plus recursiveDelete.

## Gotcha
Expect lag (typically within 24 hours of expiry, not transactional, not ordered); do not rely on TTL for hard compliance deadlines.

## Verify
- [ ] Queries ignore expired documents and orphaned subcollections are cleaned.

## Checked

2026-11-03. Confirmed on the TTL page (not instantaneous, still queryable until deleted, subcollections kept, triggers fire, indexed or unindexed field, hotspot warning), the Best practices page (exempt TTL fields from indexing) and the Delete data page (recursiveDelete).

Method: documentation only; no commands were run.
