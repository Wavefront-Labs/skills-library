---
id: computing-software.database-administration.cloud-nosql-databases.firestore-snapshot-listeners
name: firestore-snapshot-listeners
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-snapshot-listeners, firestore-realtime, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Subscribe to document and query changes."
sources:
  - https://firebase.google.com/docs/firestore/query-data/listen
  - https://firebase.google.com/docs/firestore/pricing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot listeners

**Goal:** Subscribe to document and query changes.

## Steps
- onSnapshot(query, snap => snap.docChanges().forEach(c => ...)) delivers initial results then added, modified, removed changes.
- A listener is billed a read each time a document in its result set is added or updated, and when a document leaves the result set because it changed; a deleted document is not billed. Cost scales with result size and update rate.
- Call the returned unsubscribe function on teardown.
- The initial snapshot can come from the local cache while the server data is fetched; includeMetadataChanges: true also fires on metadata changes, and metadata.hasPendingWrites marks local changes not yet on the backend.

## Gotcha
A listener you do not detach keeps receiving updates, which are billed and use bandwidth; unsubscribe when screens close.

## Verify
- [ ] Listener counts in the usage dashboard match active screens and reads per session are within budget.

## Checked

2026-11-03. Confirmed on the Get realtime updates page (onSnapshot, docChanges types added, modified and removed, detaching with the returned function, includeMetadataChanges, hasPendingWrites, cache-first initial snapshot) and the Pricing page (listener billing). Removed: the fromCache property and the claim that each initial listen reads every matching document as a separate rule.

Method: documentation only; no commands were run.
