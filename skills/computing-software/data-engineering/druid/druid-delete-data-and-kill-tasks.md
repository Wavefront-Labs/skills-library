---
id: computing-software.data-engineering.druid.druid-delete-data-and-kill-tasks
name: druid-delete-data-and-kill-tasks
category: computing-software
field: data-engineering
product: druid
tags: [delete, kill-task, unused-segments, drop-rules, soft-delete]
level: practitioner
status: docs-checked
description: "Delete Druid data by marking segments unused then running a kill task; delete records via reindexing; auto-kill options."
sources:
  - https://github.com/apache/druid/blob/master/docs/data-management/delete.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid stores data partitioned by time chunk and deletes by dropping segments, a fast metadata-only operation.

## Time-range delete (two steps)

1. Mark segments unused (soft delete): a drop rule does it, or you mark them unused via the Coordinator API or web console. Data stops being queryable but files stay in deep storage and records stay in the metadata store.
2. Run a `kill` task (hard delete): permanently removes the segment files from deep storage and the records from the metadata store. Unrecoverable without a backup.

Drop rules (alongside load rules) define intervals to keep and to discard; dropped data is marked unused the same way and still needs a kill task to be permanently removed. An entire table is deleted the same way: mark all segments unused, then optionally kill.

## Deleting specific records

Reindex with a filter that is the inverse of what you want gone, then kill the old unused segments. This rewrites segments, so it can be slow.
- Native batch: use the `druid` input source with a `transformSpec` filter, for example a `not` filter wrapping a `selector` on `userName` equal to `bob`.
- SQL: `REPLACE <table> OVERWRITE ... SELECT ... FROM <table> WHERE userName <> 'bob'`. Druid has no `UPDATE` or `ALTER TABLE`.

## Kill task

Payload fields: `type` `kill`, `id`, `dataSource`, `interval` (all unused segments in it are destroyed), optional `versions`, `context`, `batchSize`, `limit`, `maxUsedStatusLastUpdatedTime`.
- `versions`: default null, all unused versions in the interval.
- `batchSize`: default 100, segments deleted per batch; batching yields Overlord resources, since some Overlord operations can stall during a kill.
- `limit`: default null, no limit.
- `maxUsedStatusLastUpdatedTime`: default null; only segments marked unused no later than this time are considered.

Warnings: a kill permanently removes all information about the segments. With concurrent locks, keep a large buffer between marking segments unused and killing them, or a concurrent append upgrading a segment being killed can lose data.

## Auto-kill

- Coordinator duty: periodically finds intervals with eligible unused segments and launches a kill task per interval (configured under the Coordinator data management settings).
- Overlord embedded kill (experimental): requires segment metadata caching on the Overlord and must not be enabled together with Coordinator auto-kill. Advantages listed: no task slots used, kills as soon as segments are eligible, few segments per task so locks are not held long, a dedicated `KILL` lock type that coexists with ingestion on the same interval, little configuration.

## Checked

2026-11-08. Read the cited data-deletion page in full. Extended the draft with record-level deletion, the kill-task parameter defaults, the concurrent-lock warning and both auto-kill options.

Method: documentation only; no commands were run.
