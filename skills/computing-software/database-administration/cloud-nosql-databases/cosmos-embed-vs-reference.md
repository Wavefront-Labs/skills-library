---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-embed-vs-reference
name: cosmos-embed-vs-reference
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-embed-vs-reference, cosmos-data-modelling, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Decide when to embed related data and when to reference."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/modeling-data
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding versus referencing

**Goal:** Decide when to embed related data and when to reference.

## Steps
- Embed for contained, one-to-few relationships where the data is queried together, changes infrequently and does not grow without bound (items are limited to 2 MB).
- Reference for one-to-many and many-to-many relationships, or when related data changes frequently or could be unbounded.
- Denormalised models typically read faster; normalised models typically write faster.

## Gotcha
An unbounded array inside an item (for example comments on a post) keeps growing toward the 2 MB item limit, and operations on large items cost more RU.

## Checked

2026-11-03. Confirmed against "Data modeling in Azure Cosmos DB" (when to embed, when to reference, unbounded comments example), service quotas (2 MB item) and the request units page (item size raises RU).
Removed: the change-feed sync advice and the multiple-entity-types-per-container advice (not on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Common queries are satisfied by one read or a single-partition query.
