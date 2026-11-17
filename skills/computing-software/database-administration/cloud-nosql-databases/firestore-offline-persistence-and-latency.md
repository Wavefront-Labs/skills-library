---
id: computing-software.database-administration.cloud-nosql-databases.firestore-offline-persistence-and-latency
name: firestore-offline-persistence-and-latency
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-offline-persistence-and-latency, firestore-realtime, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Use the local cache for offline apps."
sources:
  - https://firebase.google.com/docs/firestore/query-data/listen
  - https://firebase.google.com/docs/firestore/manage-data/enable-offline
  - https://firebase.google.com/docs/firestore/manage-data/transactions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline persistence and latency compensation

**Goal:** Use the local cache for offline apps.

## Steps
- Web: persistence is off by default (memory cache); enable it with initializeFirestore(app, {localCache: persistentLocalCache()}). Android and Apple SDKs enable persistence by default. Web persistence is supported only in Chrome, Safari and Firefox, and the cache is not cleared between sessions.
- metadata.hasPendingWrites is true for a document with local changes that have not yet been written to the backend.
- The default cache size threshold is 100 MB; past it Firestore periodically cleans up older unused documents, and you can configure the threshold or disable cleanup.
- You can write, read, listen to and query cached data offline, but transactions fail when the client is offline.

## Gotcha
A listener's first snapshot can be populated from the local cache while the server data is fetched concurrently; do not treat cached data as confirmed server state. On shared devices ask before enabling web persistence.

## Verify
- [ ] The app works in airplane mode and sync completes with no lost writes after reconnect.

## Checked

2026-11-03. Confirmed on the Access data offline, Get realtime updates (hasPendingWrites, cache-first snapshots) and Transactions pages. Removed: the latency compensation wording, the fromCache property and the mobile-only qualifier on the 100 MB default.

Method: documentation only; no commands were run.
