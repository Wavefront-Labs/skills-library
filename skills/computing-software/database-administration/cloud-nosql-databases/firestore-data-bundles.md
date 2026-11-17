---
id: computing-software.database-administration.cloud-nosql-databases.firestore-data-bundles
name: firestore-data-bundles
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-data-bundles, firestore-bundles-export, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Serve precomputed query results from a CDN to reduce reads."
sources:
  - https://firebase.google.com/docs/firestore/bundles
  - https://firebase.google.com/docs/firestore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data bundles

**Goal:** Serve precomputed query results from a CDN to reduce reads.

## Steps
- Build bundles on a server with the Admin SDK (Node.js, Java, Python): in Node, const bundle = firestore.bundle('latest-stories'); then bundle.add('latest-stories-query', querySnapshot).build() returns the bundle buffer to serve from a CDN or Cloud Storage.
- Clients call loadBundle(db, stream) from the web SDK, then namedQuery(db, 'latest-stories-query') and read it from the cache (for example getDocsFromCache).
- Bundles reduce read cost for popular, public, slowly changing data.
- A documented integrated option is to build bundles in Cloud Functions and serve them with Firebase Hosting.

## Gotcha
The Admin SDK does not evaluate Security Rules and bundles whatever you query, so bundle only publicly readable data. A bundle is a snapshot, stale until rebuilt.

## Verify
- [ ] Clients render from the bundle with no reads for the cached query in the usage dashboard.

## Checked

2026-11-03. Confirmed on the Firestore data bundles page (Admin SDK bundle building, bundle.add with a named query and build(), loadBundle and namedQuery, CDN or Cloud Storage serving, Cloud Functions plus Hosting option, Admin SDK ignores Security Rules, reduced query cost). Removed: scheduled rebuild advice and the wording that bundles are subject to rules.

Method: documentation only; no commands were run.
