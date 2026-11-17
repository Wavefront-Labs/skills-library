---
id: computing-software.data-engineering.apache-pinot.apache-pinot-realtime-to-offline-task
name: apache-pinot-realtime-to-offline-task
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, realtime-to-offline, realtimetoofflinesegmentstask, buckettimeperiod, buffertimeperiod, mergetype, dedup, numsegmentsbatchperserverrequest, hybrid-table]
level: advanced
status: docs-checked
description: "Pinot RealtimeToOfflineSegmentsTask: bucket and buffer periods, mergeType (concat, rollup, dedup), defaults and the upsert snapshot rule."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/pinot-managed-offline-flows.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/components/cluster/minion.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Realtime-to-offline segments task

RealtimeToOfflineSegmentsTask moves data from a REALTIME table to the matching OFFLINE table one time window at a time, so you need no hand-written offline jobs. Reasons: backfill a day, replace segments, roll up granular data, better compression, dedup.
```
"task": { "taskTypeConfigsMap": { "RealtimeToOfflineSegmentsTask": {
  "bucketTimePeriod": "6h",
  "bufferTimePeriod": "5d",
  "roundBucketTimePeriod": "1h",
  "mergeType": "rollup",
  "score.aggregationType": "max",
  "maxNumRecordsPerSegment": "100000"
}}}
```
Properties and defaults:
- `bucketTimePeriod` (default `1d`): window converted per run.
- `bufferTimePeriod` (default `2d`): a window is not scheduled until it is older than this. A processed window is never processed again, so size it to your late-data tolerance.
- `roundBucketTimePeriod` (default none): rounds the time value before merging.
- `mergeType` (default `concat`): `concat` (no aggregation), `rollup` (aggregate metrics across common dimensions and time) or `dedup`.
- `{metric}.aggregationType` (rollup only, default `sum`): e.g. `sum`, `max`, `min`, `avg`, sketch types, `firstWithTime`, `lastWithTime`. `avg` needs a BYTES metric holding AvgPair values.
- `maxNumRecordsPerSegment` (default 5,000,000).
- `numSegmentsBatchPerServerRequest` (upsert tables only, default 500): batch size when fetching valid doc IDs from servers.

Setup: start a minion, add the task to the REALTIME table config, create the OFFLINE table, enable the `PinotTaskManager` periodic task (frequency or cron, see the minion scheduling skill) and restart the controller.

Constraints:
- Only completed (`ONLINE`) segments are moved; if the window's data is still in a `CONSUMING` segment that run is skipped. At least one completed segment must exist.
- For upsert tables the task fetches valid doc IDs from servers to drop stale versions, so the upsert `snapshot` must not be `DISABLE` (use `ENABLE`).

## Checked

2026-11-09. Read the Pinot docs page `pinot-managed-offline-flows.md` in full (how it works, configuration steps and property table) and the scheduling sections of `minion.md`. Confirmed all keys, defaults and constraints above. Removed: the claim that the task enables offline-only features such as star-tree or tiering, and the statement about the hybrid time boundary advancing, neither of which appears on the pages read.
Method: documentation only; no commands were run.
