---
id: computing-software.database-administration.cloud-nosql-databases.firestore-data-types-and-modelling
name: firestore-data-types-and-modelling
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [firestore-data-types-and-modelling, firestore-data-model, firestore, google-firestore, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Choose types and denormalisation to match your queries."
sources:
  - https://firebase.google.com/docs/firestore/data-model
  - https://firebase.google.com/docs/firestore/manage-data/data-types
  - https://firebase.google.com/docs/firestore/quotas
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data types and modelling choices

**Goal:** Choose types and denormalisation to match your queries.

## Steps
- Types: text string, 64-bit integer, floating-point number, boolean, date and time (timestamp), geographical point, reference, array, map, bytes, null and vector (Enterprise edition adds more, such as 32-bit integer and Decimal128).
- Denormalise: copy fields needed for list views into the parent or a summary document; update copies with a batched write or Cloud Function.
- Collection group queries search all collections with the same ID.
- Standard-edition limits: document 1 MiB; 40,000 index entries per document; map and array nesting depth 20; text and bytes values up to 1,048,487 bytes, of which queries consider only the first 1,500 bytes; vector dimension up to 2048.

## Gotcha
Arrays suit small bounded sets because a document is capped at 1 MiB. arrayUnion() and arrayRemove() add or remove elements without rewriting the array, and in Standard edition an array cannot contain another array.

## Verify
- [ ] Typical screens load with one query and no client-side joins.

## Checked

2026-11-03. Confirmed on the Supported data types, Cloud Firestore data model and Usage and limits pages, and the add-data page (arrayUnion, arrayRemove). Removed: the 20,000 field limit (not in the docs) and the claim that arrays cannot be updated per element.

Method: documentation only; no commands were run.
