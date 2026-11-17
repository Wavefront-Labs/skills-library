---
id: computing-software.database-administration.cloud-nosql-databases.firestore-query-operators-and-limits
name: firestore-query-operators-and-limits
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-query-operators-and-limits, firestore-queries-indexes, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Use query operators within their constraints."
sources:
  - https://firebase.google.com/docs/firestore/query-data/index-overview
  - https://firebase.google.com/docs/firestore/query-data/queries
  - https://firebase.google.com/docs/firestore/query-data/multiple-range-fields
  - https://firebase.google.com/docs/firestore/query-data/query-cursors
  - https://firebase.google.com/docs/firestore/query-data/aggregation-queries
  - https://firebase.google.com/docs/firestore/pricing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query operators and limits

**Goal:** Use query operators within their constraints.

## Steps
- Operators: ==, !=, <, <=, >, >=, in, not-in, array-contains, array-contains-any; or and and compound filters are supported. in and array-contains-any take up to 30 values, not-in up to 10, and a query is limited to 30 disjunctions in disjunctive normal form (fixed). You cannot combine not-in and != in one query.
- Range and inequality filters on multiple fields in one query are supported; they are billed on documents read and index entries read. Combining equality with inequality filters needs a composite index.
- Paginate with orderBy, startAfter(cursor) and limit; avoid offsets, which bill a read for each skipped document.
- Aggregation queries count(), sum() and average() are billed by index entries read (one read per batch of 1000, minimum one read) rather than per document.

## Gotcha
A query reads one collection; to search every collection with the same ID, including subcollections, use a collection group query.

## Verify
- [ ] Paged queries return stable ordered results and read counts equal the documents returned.

## Checked

2026-11-03. Confirmed on the Perform simple and compound queries, Query cursors, Aggregation queries, Multiple range fields and Pricing pages (operator list, 30 and 10 value limits, 30 disjunctions, offset billing, startAfter, aggregation billing, collection group queries). Removed: the shallow-query wording and the unsourced composite-index rule for multiple range fields.

Method: documentation only; no commands were run.
