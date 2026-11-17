---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-indexing-policy-tuning
name: cosmos-indexing-policy-tuning
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-indexing-policy-tuning, cosmos-indexing, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Index only what queries need to cut write RU and storage."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/index-policy
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indexing policy tuning

**Goal:** Index only what queries need to cut write RU and storage.

## Steps
- The default policy indexes every property of every item and enforces range indexes for strings and numbers; exclude large or unqueried paths with excludedPaths such as {"path":"/payload/*"} to cut write RU.
- Policy JSON: {"indexingMode":"consistent","includedPaths":[{"path":"/status/?"}],"excludedPaths":[{"path":"/*"}]}
- Index changes run as asynchronous background transformations without affecting read or write availability or provisioned throughput; track progress with the SDK's index transformation progress (IndexTransformationProgress).
- New containers cannot select lazy indexing; use consistent or none.

## Gotcha
With the exclude-root strategy the partition key path is not indexed by default; include it if queries filter on it, or those queries force full scans and raise RU.

## Checked

2026-11-03. Confirmed against the "Indexing policies" page: default policy, range indexes, root path must be included or excluded, exclude-root strategy example shape, asynchronous index transformation, IndexTransformationProgress, lazy indexing unavailable for new containers, partition key not indexed with exclude strategy. The /payload/* and /status/? paths are illustrative.
Removed: the x-ms-documentdb index transformation header and the ORDER BY scan claim (not on the page).
Method: documentation only; no commands were run.

## Verify
- [ ] Write RU per item falls after excluding unused paths and key queries still run with acceptable RequestCharge.
