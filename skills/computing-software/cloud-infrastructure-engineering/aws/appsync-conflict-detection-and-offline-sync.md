---
id: computing-software.cloud-infrastructure-engineering.aws.appsync-conflict-detection-and-offline-sync
name: appsync-conflict-detection-and-offline-sync
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, appsync, conflict-detection, datastore, offline-sync, delta-sync, optimistic-concurrency, automerge]
level: practitioner
status: docs-checked
description: "Set up AppSync conflict detection for offline-capable clients: versioned DynamoDB data sources, optimistic concurrency, automerge or Lambda handlers, and delta sync tables."
sources: ["https://docs.aws.amazon.com/appsync/latest/devguide/conflict-detection-and-sync.html", "https://docs.aws.amazon.com/appsync/latest/devguide/conflict-detection-and-resolution.html", "https://docs.aws.amazon.com/appsync/latest/devguide/tutorial-delta-sync.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppSync conflict detection and offline sync

**Goal:** let mobile/web clients write while offline and reconcile concurrent edits safely when
they reconnect.

## Building blocks
- **Versioned data source:** DynamoDB data source with versioning on; AppSync maintains
  `_version`, `_lastChangedAt`, `_deleted` (soft delete) on each item.
- **Delta Sync table:** a second DynamoDB table acting as a journal of recent changes, groomed by
  DynamoDB TTL (`DeltaSyncTableTTL` on the data source, for example one hour or one day), so clients that
  were offline briefly fetch only changes; longer absences fall back to the base-table query.
- **Sync queries:** `syncOrders(lastSync: AWSTimestamp)` resolvers use the DynamoDB Sync operation. Without
  `lastSync` the query runs on the base table; with it, on the delta table.

## Conflict handlers (per resolver, `syncConfig`)
| Strategy | Behaviour |
|---|---|
| `OPTIMISTIC_CONCURRENCY` | reject the write if the client's `_version` is stale; client must refetch and retry |
| `AUTOMERGE` | scalar conflicts: the server value is kept; lists: incoming values are appended to the server list; sets: set union; omitted fields are preserved |
| `LAMBDA` | your function decides: `RESOLVE` (replace with the item you return), `REJECT` (error with the existing item), or `REMOVE` (DynamoDB only) |
```json
"syncConfig": {"conflictDetection":"VERSION","conflictHandler":"LAMBDA",
  "lambdaConflictHandlerConfig":{"lambdaConflictHandlerArn":"arn:aws:lambda:...:function:resolve"}}
```

## Clients
- Amplify **DataStore** (Gen 1 libraries) implements the local store, outbox, sync and conflict
  flow on top of these resolvers. Check Amplify's current documentation before choosing it for a new app.
- Custom clients must send `_version` in mutations and handle `ConflictUnhandled` errors
  (raised, for example, when a Lambda conflict handler returns `REJECT`).

## Gotchas
- `_deleted` items stay in the base table; set `baseTableTTL` or a cleanup job.
- Delta Sync TTL too short forces full syncs; too long grows the table.
- Lambda handler errors make the mutation fail; keep it deterministic and fast.
- Subscriptions plus sync queries both deliver changes; dedupe on id + `_version`.

## Verify
- [ ] Two clients edit the same record offline; after reconnect the chosen strategy applies (one rejected or merged).
- [ ] Delta Sync table receives records and expires them per TTL.
- [ ] Deleted records sync as `_deleted: true` and disappear from client UIs.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS AppSync Developer Guide conflict detection and resolution, versioning and Delta Sync tutorial pages; botocore appsync 2017-07-25 model (SyncConfig, DeltaSyncConfig). Fixed: AUTOMERGE keeps the server value for scalars, appends incoming list values to the server list (it does not union lists) and unions sets; Lambda handler actions are RESOLVE, REJECT and REMOVE (REMOVE for DynamoDB). Confirmed: three strategies, conflictDetection VERSION, deltaSyncTableTTL and baseTableTTL, _version and _deleted, base versus delta query by lastSync, ConflictUnhandled. Removed the 30-minute TTL example, the Amplify Gen 2 DataStore claim and the backfill claim, and replaced the prose-title Amplify source with the AppSync pages.
Method: documentation only; no commands were run.
