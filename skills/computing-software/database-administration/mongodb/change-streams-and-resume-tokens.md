---
id: computing-software.database-administration.mongodb.change-streams-and-resume-tokens
name: change-streams-and-resume-tokens
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-transactions, change-streams, resume-token, resumeafter, startafter, fulldocument, pre-and-post-images, oplog-window]
level: practitioner
status: docs-checked
description: "Consume MongoDB change streams reliably: watch filters, persisting resume tokens, resumeAfter vs startAfter, pre/post images, and oplog-window failures."
sources:
  - https://www.mongodb.com/docs/manual/changeStreams/
  - https://www.mongodb.com/docs/manual/changeStreams/#resume-a-change-stream
  - https://www.mongodb.com/docs/manual/changeStreams/#change-streams-with-document-pre--and-post-images
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Opening and resuming change streams

**Goal:** a consumer that processes every change exactly once (at-least-once + idempotency) across restarts.

## Open
```javascript
const pipeline = [ { $match: { operationType: { $in: ["insert", "update", "replace", "delete"] }, "fullDocument.tenant": 7 } } ];
const cs = db.collection("orders").watch(pipeline, {
  fullDocument: "updateLookup",                  // current doc for updates (may be newer than the event)
  // fullDocument: "whenAvailable" + fullDocumentBeforeChange: "whenAvailable"   // 6.0+ with pre/post images enabled
  resumeAfter: savedToken                        // or startAfter / startAtOperationTime
});
for await (const ev of cs) {
  await handle(ev);                               // idempotent: keyed by ev._id or documentKey + clusterTime
  await saveToken(ev._id);                        // persist AFTER processing
}
```
Watch levels: collection, database (`db.watch()`), deployment (`client.watch()`). Requires replica set or sharded cluster, read concern majority.

## Resume
- `resumeAfter: token`: continue after that event; fails if the stream was invalidated (collection dropped/renamed).
- `startAfter: token`: unlike `resumeAfter`, can also resume after an invalidate event (by creating a new change stream).
- `startAtOperationTime: Timestamp`: from a cluster time, e.g. a snapshot time for initial load + stream.
- Use `cs.resumeToken` (post-batch resume token) to save progress even when no matching events arrive, so filtered streams do not fall behind.

## Oplog window
Resume works only while the oplog still has enough history to locate the operation for the token or timestamp. If the consumer is down longer, resuming fails; then resnapshot. Size the oplog for consumer downtime.

## Pre- and post-images (6.0+)
```javascript
db.runCommand({ collMod: "orders", changeStreamPreAndPostImages: { enabled: true } })
db.adminCommand({ setClusterParameter: { changeStreamOptions: { preAndPostImages: { expireAfterSeconds: 86400 } } } })
```
Stored in `config.system.preimages`; cost extra writes and storage.

## Gotchas
- Events larger than 16 MB fail (`BSONObjectTooLarge`); use `$changeStreamSplitLargeEvent` (7.0 and 6.0.9+) as the last pipeline stage.
- `updateLookup` does an extra read per event and returns the latest version, not the one at event time.
- Change streams cannot use indexes (the oplog cannot be indexed); avoid opening a high number of specifically targeted streams, which can impact server performance.

## Verify
Kill the consumer, write 100 docs, restart: exactly those 100 events are processed once, starting from the saved token.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: resumeAfter vs startAfter (startAfter can resume after invalidate), oplog must hold history for the token, postBatchResumeToken on aggregate and getMore, pre/post images from 6.0 via collMod changeStreamPreAndPostImages, fullDocument and fullDocumentBeforeChange whenAvailable, changeStreamOptions.preAndPostImages.expireAfterSeconds cluster parameter (6.0, default off), config.system.preimages, 16 MiB event limit with BSONObjectTooLarge, $changeStreamSplitLargeEvent (7.0 and 6.0.9), updateLookup returns the most current majority-committed document, change streams cannot use indexes. Removed unconfirmed error code and version tags.

Method: documentation only; no commands were run.
