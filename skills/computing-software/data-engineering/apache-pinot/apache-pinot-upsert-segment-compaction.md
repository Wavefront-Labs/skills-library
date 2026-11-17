---
id: computing-software.data-engineering.apache-pinot.apache-pinot-upsert-segment-compaction
name: apache-pinot-upsert-segment-compaction
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, upsert-compaction, upsertcompactiontask, invalidrecordsthresholdpercent, invalidrecordsthresholdcount, buffertimeperiod, validdoctype, validdocidstype, minion]
level: advanced
status: docs-checked
description: "Reclaiming space in upsert tables with UpsertCompactionTask: threshold keys, validDocIdsType choices, and the skipUpsert count query to estimate dead rows."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/upsert-and-dedup/segment-compaction-on-upserts.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upsert segment compaction

Upsert tables keep every version of a record in immutable segments; older versions are not queried but still use storage. A minion task, `UpsertCompactionTask`, replaces a completed segment with a compacted one holding only the latest records. Prerequisites: task scheduling enabled and a minion available.
```
"task": { "taskTypeConfigsMap": { "UpsertCompactionTask": {
  "schedule": "0 */5 * ? * *",
  "bufferTimePeriod": "7d",
  "invalidRecordsThresholdPercent": "30",
  "invalidRecordsThresholdCount": "100000",
  "tableMaxNumTasks": "100",
  "validDocIdsType": "SNAPSHOT"
}}}
```

- `bufferTimePeriod`: set to `0d` to compact segments as soon as they complete; otherwise how long to wait after a segment completes.
- `invalidRecordsThresholdPercent` / `invalidRecordsThresholdCount` (optional): a completed segment may be selected when the share or the count of old records exceeds the value. By default all thresholds are 0, meaning none applied. Do not set them very low (close to 1): compaction is expensive.
- `tableMaxNumTasks` (optional): limits the number of tasks scheduled.
- `validDocIdsType` (optional): `SNAPSHOT` (default), `SNAPSHOT_WITH_DELETE`, `IN_MEMORY`, `IN_MEMORY_WITH_DELETE`. The default stays SNAPSHOT even when `upsertConfig.deleteRecordColumn` is set. The snapshot types need `upsertConfig.snapshot` not to be DISABLE; the `_WITH_DELETE` types need `upsertConfig.deleteRecordColumn` set. In-memory types read the bitmap from the real-time server's memory, which is updated while consuming; snapshots are taken only after a segment commits.
- A completed segment containing only old records is deleted outright rather than compacted.

Estimate the benefit first:
```
SET skipUpsert=true; SELECT COUNT(*) FROM t
```
Compare with the normal count. The gap is the number of old rows.

## Checked

Confirmed against the Pinot docs page "Segment compaction on upserts": config keys, example values, validDocIdsType values and prerequisites, threshold defaults and the skipUpsert query. Changed the example cron schedule to the page's value and corrected the snapshot requirement ("not DISABLE", not "ENABLE").

Method: docs-only read of cited pages, 2026-11-08
