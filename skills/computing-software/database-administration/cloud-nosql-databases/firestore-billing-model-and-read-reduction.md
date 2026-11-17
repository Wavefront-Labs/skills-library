---
id: computing-software.database-administration.cloud-nosql-databases.firestore-billing-model-and-read-reduction
name: firestore-billing-model-and-read-reduction
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-billing-model-and-read-reduction, firestore-cost-capacity, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Understand what is billed and reduce reads."
sources:
  - https://firebase.google.com/docs/firestore/pricing
  - https://firebase.google.com/docs/firestore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Billing model and read reduction

**Goal:** Understand what is billed and reduce reads.

## Steps
- Billed per document read, write and delete, plus database storage (including index overhead) and outbound data transfer. Every query has a minimum charge of one document read; queries with more than one range field also bill index entries read, one read per batch of up to 1000 entries.
- Reduce: limit() and cursors (no extra cost; an offset bills every skipped document), data bundles, the local cache, and narrowly scoped listeners.
- Aggregation queries (count(), sum(), average()) bill by index entries read (one read per batch of 1000, minimum one read), not one read per document.
- Cost control: create a monthly budget with alerts in the Billing section of the Google Cloud console (budgets alert, they do not cap usage).
- For current rates see the Firestore pricing page.

## Gotcha
A listener bills a read each time a document in its result set is added or updated, so a large, frequently updated result set multiplies reads; narrow the query. A reconnecting listener can be billed as a new query (after 30 minutes offline with persistence enabled, on every reconnect without it).

## Verify
- [ ] The usage dashboard's reads per active user fall and budget alerts are configured.

## Checked

2026-11-03. Confirmed on the Firestore pricing page (index entry reads per 1000, minimum one read per query, aggregation billing, offset billing, listener billing and the 30-minute reconnect rule, storage and outbound transfer) and the quotas page (budgets alert but do not limit usage). Removed: region price claim and the unverified list of what counts as network egress.

Method: documentation only; no commands were run.
