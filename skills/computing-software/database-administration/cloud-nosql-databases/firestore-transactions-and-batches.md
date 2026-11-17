---
id: computing-software.database-administration.cloud-nosql-databases.firestore-transactions-and-batches
name: firestore-transactions-and-batches
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-transactions-and-batches, firestore-transactions, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Use transactions for read-modify-write and batches for atomic multi-writes."
sources:
  - https://firebase.google.com/docs/firestore/manage-data/transactions
  - https://firebase.google.com/docs/firestore/quotas
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactions and batched writes

**Goal:** Use transactions for read-modify-write and batches for atomic multi-writes.

## Steps
- runTransaction(async tx => { const s = await tx.get(ref); tx.update(ref, {count: s.data().count + 1}); }) reads before writes and retries on contention.
- Batched writes (writeBatch in the web SDK, then batch.commit()) apply any mix of set, update and delete atomically when you need no reads; each operation counts separately toward usage.
- A transaction retries if a document it read is changed by a concurrent edit, and fails if it reads after writing, exceeds the 10 MiB request size, or passes the 270-second limit (60-second idle expiry). Transactions fail when the client is offline.
- Keep transactions short and side-effect free, because the function may run several times.

## Gotcha
Do not modify application state inside the transaction callback; it can be retried and rerun.

## Verify
- [ ] Concurrent increments reach the exact total in a test with parallel clients.

## Checked

2026-11-03. Confirmed on the Transactions and batched writes page (reads before writes, automatic retry, no application-state changes, offline failure, writeBatch and commit, error causes) and the Usage and limits page (10 MiB, 270 s, 60 s idle). Removed: the 500-operation batch figure and the server-versus-client locking claim, which the pages do not state.

Method: documentation only; no commands were run.
