---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-consistency-level-selection
name: cosmos-consistency-level-selection
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-consistency-level-selection, cosmos-consistency, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Pick one of five levels: strong, bounded staleness, session, consistent prefix, eventual."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-consistency
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consistency level selection

**Goal:** Pick one of five levels: strong, bounded staleness, session, consistent prefix, eventual.

## Steps
- Session is the most widely used level: read-your-writes using the session token.
- Strong increases write latency because data must replicate and commit across large distances, and it reduces availability during failures.
- Bounded staleness keeps lag below K versions of an item or T time, whichever is reached first.
- Set the account default with az cosmosdb update --default-consistency-level Session; a request can override the default.

## Gotcha
Session tokens are partition-bound and tracked per SDK client; to read your writes from another instance, pass the token generated for the relevant items.

## Checked

2026-11-03. Confirmed against "Consistency levels" and "Manage consistency levels" pages and the az cosmosdb update reference (--default-consistency-level accepts BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong): five levels, session most widely used, strong latency and availability trade-off, K or T bounded staleness, default override, partition-bound session tokens.
Removed: the 2x read RU claim, the consistent-prefix "no gaps" wording, and "clients can relax, not strengthen" (not on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] A write-then-read test across instances honours the chosen level and the RU cost is as expected.
