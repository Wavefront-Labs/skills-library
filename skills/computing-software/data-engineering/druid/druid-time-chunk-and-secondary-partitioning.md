---
id: computing-software.data-engineering.druid.druid-time-chunk-and-secondary-partitioning
name: druid-time-chunk-and-secondary-partitioning
category: computing-software
field: data-engineering
product: druid
tags: [partitioning, time-chunk, segment-granularity, partitioned-by, hour, day]
level: practitioner
status: docs-checked
description: "Set time chunk partitioning and understand why it matters for pruning and locking."
sources:
  - https://github.com/apache/druid/blob/master/docs/ingestion/partitioning.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You can partition and sort segments within a datasource to shrink data and speed up queries. Splitting into separate datasources also works well while the number of datasources does not cause excessive per-datasource overhead.

Druid always partitions datasources by time into time chunks, each containing one or more segments, using `segmentGranularity` in the ingestion spec `dataSchema`. This matters because:
1. Queries filtering on `__time` (SQL) or `intervals` (native) use time partitioning to prune the set of segments.
2. Data management operations such as overwriting and compacting take exclusive write locks on time partitions.
3. Each segment file sits wholly inside one time chunk, so too fine a granularity can create many small segments and poor performance.

The most common choices are `hour` and `day`. For streaming ingestion `hour` is especially common because it lets compaction follow ingestion with less delay.

How you configure it depends on the method: SQL-based ingestion uses `PARTITIONED BY`, and Kafka, Kinesis and native batch use `segmentGranularity` inside the `granularitySpec`.

Secondary partitioning splits each time chunk into immutable segments by a dimension, so rows with the same value are stored together. Pick a natural dimension you often filter on. SQL uses `CLUSTERED BY`; native batch uses `partitionsSpec` inside `tuningConfig`; for Kafka or Kinesis, upstream partitioning decides, and you can change clustering later with `REPLACE` (with `CLUSTERED BY`) or compaction.

Sorting: each segment is sorted internally. Putting the partitioning dimension first in the sort order often helps compression more than partitioning alone. SQL uses the field order in `CLUSTERED BY` (or the `segmentSortOrder` context parameter); Kafka, Kinesis and native batch use the field order in `dimensionsSpec`. Rows are implicitly sorted by `__time` first unless `forceSegmentSortByTime` is `false`. That setting is experimental, segments built that way can only be read by Druid 31 or later, and some queries are unsupported on them, including native queries with `granularity` other than `all` and native `scan` queries with ascending or descending time order.

## Checked

2026-11-08. Read ingestion/partitioning.md in full. Added secondary partitioning, sorting and the forceSegmentSortByTime caveats.

Method: documentation only; no commands were run.
