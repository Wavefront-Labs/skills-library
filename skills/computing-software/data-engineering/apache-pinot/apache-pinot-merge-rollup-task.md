---
id: computing-software.data-engineering.apache-pinot.apache-pinot-merge-rollup-task
name: apache-pinot-merge-rollup-task
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, merge-rollup, mergerolluptask, mergetype, rollup, concat, buckettimeperiod, buffertimeperiod, roundbuckettimeperiod, maxnumrecordspersegment, erasedimensionvalues, retentionexpirybufferperiod]
level: advanced
status: docs-checked
description: "Pinot MergeRollupTask: scope, per-level keys (mergeType, bucketTimePeriod, bufferTimePeriod), aggregation types and the ZooKeeper watermark."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/minion-merge-rollup-task.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minion merge-rollup task

MergeRollupTask merges small segments into larger, time-aligned ones, optionally rolling up rows to a coarser granularity. It applies to **OFFLINE append-only tables** and **REALTIME tables without upsert or dedup**.
```
"MergeRollupTask": {
  "1day.mergeType": "rollup",
  "1day.bucketTimePeriod": "1d",
  "1day.bufferTimePeriod": "1d",
  "1day.roundBucketTimePeriod": "1d",
  "1day.maxNumRecordsPerSegment": "1000000",
  "1day.maxNumRecordsPerTask": "5000000",
  "1day.eraseDimensionValues": "a,b",
  "metricColA.aggregationType": "sum"
}
```
Keys are prefixed by a merge level name (`1hour`, `1day`); several levels chain to apply different granularity to different age ranges. Defaults: `mergeType` `concat` (or `rollup`), `maxNumRecordsPerSegment` 5,000,000, `maxNumRecordsPerTask` 50,000,000, `maxNumParallelBuckets` 1; `bucketTimePeriod` and `bufferTimePeriod` have none. `bufferTimePeriod` delays a bucket until it is older than the buffer, and a processed window is never reprocessed. `eraseDimensionValues` replaces listed dimensions with their `defaultValue` before rollup. `{metric}.aggregationType` (default `sum`) includes `max`, `min`, `avg`, sketch types, `percentileTDigest`, `firstWithTime`, `lastWithTime`; `avg` requires a BYTES column of serialized AvgPair values.

Prerequisites: start a minion, then in the controller config set `controller.task.scheduler.enabled=true` and a `controller.task.frequencyPeriod` (for example `1h`), and restart the controller.

State: a watermark per merge level is kept in ZooKeeper at `MINION_TASK_METADATA/MergeRollupTask/<tableNameWithType>`; everything before it is merged and time aligned. Output segments swap in with the segment replacement protocol, a broker-level atomic swap using segment lineage.

`retentionExpiryBufferPeriod` (for example `"1h"`) keeps segments near retention expiry out of task generation, but the watermark advances past a bucket whose segments are all filtered and that bucket is never reprocessed, so keep the buffer conservative. Watch the metric `mergeRollupTaskDelayInNumBuckets` to see whether the task is stuck.

## Checked

2026-11-09. Read the whole Pinot docs page `minion-merge-rollup-task.md`. Confirmed the scope, key names, defaults, prerequisites, ZooKeeper path, atomic swap, aggregation types, AvgPair requirement, retention-buffer caveat and metric. Changed: the example now mirrors the page's examples; a defaults list and the watermark caveat were added.
Method: documentation only; no commands were run.
