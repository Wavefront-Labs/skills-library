---
id: computing-software.database-administration.cloud-nosql-databases.firestore-documents-collections-subcollections
name: firestore-documents-collections-subcollections
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-documents-collections-subcollections, firestore-data-model, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Structure data as documents in collections, with subcollections for nested sets."
sources:
  - https://firebase.google.com/docs/firestore/data-model
  - https://firebase.google.com/docs/firestore/manage-data/delete-data
  - https://firebase.google.com/docs/firestore/best-practices
  - https://firebase.google.com/docs/firestore/quotas
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Documents, collections and subcollections

**Goal:** Structure data as documents in collections, with subcollections for nested sets.

## Steps
- A document is limited to 1 MiB (1,048,576 bytes) and lives in a collection; paths alternate collection and document, e.g. users/alice/orders/o1.
- Use subcollections for unbounded children (messages, orders) so the parent document stays small.
- Document IDs: auto-ID from add() are well distributed; avoid monotonically increasing IDs at high write rates.
- Subcollections nest up to 100 levels deep.

## Gotcha
Deleting a document does not delete its subcollections; they remain orphaned until deleted explicitly (use recursiveDelete() in the server libraries or the Firebase CLI firebase firestore:delete command).

## Verify
- [ ] Each access pattern reads one document or one collection query, and deleting a parent also removes children via recursiveDelete.

## Checked

2026-11-03. Confirmed on the data model, Usage and limits, Best practices and Delete data pages (1 MiB, 100-level nesting, scattered automatic IDs and monotonic-ID hotspots, orphaned subcollections, recursiveDelete, firebase firestore:delete). Removed: the claim about reads not including subcollections and the -r flag.

Method: documentation only; no commands were run.
