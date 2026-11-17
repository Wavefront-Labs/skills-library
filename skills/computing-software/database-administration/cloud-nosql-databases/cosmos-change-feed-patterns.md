---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-change-feed-patterns
name: cosmos-change-feed-patterns
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-change-feed-patterns, cosmos-change-feed, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Use the change feed for materialised views, event sourcing and migrations."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-pull-model
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-modes
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change feed patterns

**Goal:** Use the change feed for materialised views, event sourcing and migrations.

## Steps
- Update a denormalised view container from changes to the source container.
- Pull model gives control with FeedIterator (created with a required ChangeFeedStartFrom and ChangeFeedMode), scoped by FeedRange (a range of partition key values) and resumable from a continuation token.
- Start from the beginning, from now, or from a continuation token via ChangeFeedStartFrom.
- Handlers must be idempotent: the change feed processor guarantees at-least-once delivery.

## Gotcha
Latest version mode does not capture deletes or intermediate versions; all versions and deletes mode (needs continuous backup) records them.

## Checked

2026-11-03. Confirmed against the change feed overview, pull model and change feed modes pages: materialised-view use, FeedIterator, ChangeFeedStartFrom.Beginning/Now/ContinuationToken, FeedRange, at-least-once delivery, latest-version versus all-versions-and-deletes behaviour.
Removed: the point-in-time start option (not shown on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] A view container converges to the source after a replay from the beginning.
