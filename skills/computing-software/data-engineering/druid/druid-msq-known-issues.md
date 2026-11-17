---
id: computing-software.data-engineering.druid.druid-msq-known-issues
name: druid-msq-known-issues
category: computing-software
field: data-engineering
product: druid
tags: [msq, known-issues, grouping-sets, insert-column-list, disk-space, fault-tolerance]
level: advanced
status: docs-checked
description: "List the documented MSQ limitations to check before relying on SQL ingestion."
sources:
  - https://github.com/apache/druid/blob/master/docs/multi-stage-query/known-issues.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Runtime:
- Fault tolerance is partial. Workers are relaunched if killed unexpectedly, but the controller is not.
- Worker stage outputs are stored in the directory given by `druid.indexer.task.baseDir`. Stages producing a lot of output can fill the disk and the query fails with an UnknownError containing "No space left on device".

SELECT:
- `GROUPING SETS` are not implemented and return a QueryNotSupported error.

INSERT and REPLACE:
- Column lists such as `INSERT INTO tbl (a, b, c) SELECT ...` are not implemented.
- Columns are inserted by name from the SELECT, not by position as in standard SQL.
- Not all ingestion spec options are supported, including the `createBitmapIndex` and `multiValueHandling` dimension properties and the `indexSpec` tuning property.

EXTERN:
- Schemaless dimensions are not available. Every column and type must be listed in the `signature` parameter.
- Input sources matching very many files can exhaust memory on the controller task.
- EXTERN refers to external files; use `FROM` to read `druid` input sources.

WINDOW:
- A window cannot exceed 100,000 elements.
- Where the native engine has a non-empty `leafOperator`, MSQ adds an extra scan stage after the window stage.

Automatic compaction with the MSQ engine:
- `metricSpec` is supported only for certain aggregators.
- Only dynamic and range partitioning are supported.
- Set `rollup` to true if and only if `metricSpec` is non-empty.
- Partition only on string dimensions, and not multi-valued ones.
- `maxTotalRows` is not supported in `DynamicPartitionsSpec`; use `maxRowsPerSegment`.
- Segments can only be sorted with `__time` as the first column.

Check this list when a statement that works in native batch fails under MSQ.

## Checked

2026-11-08. Read multi-stage-query/known-issues.md in full. Added the missing EXTERN, WINDOW and automatic-compaction limits and removed a claim that the page was only partly covered.

Method: documentation only; no commands were run.
