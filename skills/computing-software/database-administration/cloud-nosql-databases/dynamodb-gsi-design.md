---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-gsi-design
name: dynamodb-gsi-design
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-gsi-design, dynamodb-indexes, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Add a GSI to serve an alternate access pattern with its own key schema."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global secondary index design

**Goal:** Add a GSI to serve an alternate access pattern with its own key schema.

## Steps
- A GSI has its own partition and optional sort key, its own provisioned or on-demand throughput, and is eventually consistent only.
- Project only needed attributes (KEYS_ONLY, INCLUDE, ALL) to limit storage and write cost.
- Sparse index: only items having the GSI key attribute(s) appear; index "open" orders by writing the attribute only while open and deleting it on shipment.
- Default limit is 20 GSIs per table.

## Gotcha
A throttled GSI back-pressures writes to the base table; provision GSI write capacity to match base writes.

## Verify
- [ ] describe-table shows IndexStatus ACTIVE, backfill complete, and queries on the index return the expected items.

## Checked
Checked 2026-11-03 against the secondary index, sparse index best-practice and GSI online operations pages: own throughput, eventually consistent reads only, projection types, sparse behaviour (the isOpen example), the 20 GSI default and base-table throttling from an under-provisioned GSI match. Resolved the "(confirm)" on the GSI limit.
Method: documentation only; no commands were run.
