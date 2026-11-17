---
id: computing-software.database-administration.mongodb.filtering-and-scaling-change-streams
name: filtering-and-scaling-change-streams
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, change-stream-filter, change-streams, mongodb-transactions, fulldocument, pre-images]
level: practitioner
status: docs-checked
description: "Filter MongoDB change streams server-side with $match, project only needed fields, use pre/post images, and scale consumers by partitioning the stream."
sources:
  - https://www.mongodb.com/docs/manual/changeStreams/
  - https://www.mongodb.com/docs/manual/administration/change-streams-production-recommendations/
  - https://www.mongodb.com/docs/manual/reference/change-events/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtering and scaling change streams

**Goal:** consume only the events you need, keep the stream fast, and parallelise consumers without losing ordering guarantees you depend on.

## Server-side filter
```javascript
const cs = db.orders.watch([
  { $match: { operationType: { $in: ["insert", "update"] }, "fullDocument.status": "paid" } },
  { $project: { "fullDocument.items": 0 } }
], { fullDocument: "updateLookup" })
```
- The `$match` and `$project` stages run on the server, so unmatched events are not returned to the client.
- `fullDocument: "updateLookup"` fetches the current document at read time (may be newer than the event). 6.0+ `fullDocument: "whenAvailable"`/`"required"` uses post-images stored at write time.
- Pre-images (6.0+): `db.runCommand({collMod: "orders", changeStreamPreAndPostImages: {enabled: true}})` then `fullDocumentBeforeChange: "whenAvailable"`.
- Do not modify or remove the `_id` field (the resume token) in the pipeline; MongoDB raises an error.

## Scaling consumers
- One stream per collection is ordered. To parallelise, run N consumers each with a filter partition:
```javascript
{ $match: { $expr: { $eq: [ { $mod: [ { $abs: { $toHashedIndexKey: "$documentKey._id" } }, 4 ] }, 2 ] } } }
```
(consumer 2 of 4). `$mod` keeps the sign of a negative dividend and hashes can be negative, hence `$abs`. Per-document ordering is preserved because each `_id` always maps to the same consumer; cross-document order is not.
- Change streams cannot use indexes, and the manual advises avoiding a high number of specifically targeted streams, so prefer fewer streams with filters over one stream per tenant.

## Resumability
Store `cs.resumeToken` after processing each event (or batch); restart with `resumeAfter`/`startAfter`. The token is valid while the event is still in the oplog: size the oplog window larger than the longest consumer outage.

## Large events
Events > 16 MB fail with `BSONObjectTooLarge`; `$changeStreamSplitLargeEvent` (7.0 and 6.0.9+) as the last stage splits them into fragments.

## Verify
Lag = now - `clusterTime` of the last processed event; alert when it approaches the oplog window.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: server-side filtering with $match/$project, fullDocument whenAvailable and fullDocumentBeforeChange (6.0), collMod changeStreamPreAndPostImages, the pipeline must not modify or remove the _id resume token, $changeStreamSplitLargeEvent (7.0 and 6.0.9), $toHashedIndexKey, $mod keeps the sign of a negative dividend (fixed the partition example with $abs), oplog history requirement for resume. Removed unconfirmed sharded no-op claim.

Method: documentation only; no commands were run.
