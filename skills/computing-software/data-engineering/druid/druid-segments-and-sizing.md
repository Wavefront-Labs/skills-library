---
id: computing-software.data-engineering.druid.druid-segments-and-sizing
name: druid-segments-and-sizing
category: computing-software
field: data-engineering
product: druid
tags: [segments, segment-granularity, columnar, target-rows-per-segment, partitioning]
level: practitioner
status: docs-checked
description: "Explain segment structure and the 300-700 MB, five-million-row sizing guidance."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/segments.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid stores data and indexes in segment files partitioned by time. A segment is created for each segment interval that contains data; empty intervals have no segment. Multiple segments can exist for the same interval if data was ingested by different jobs, and compaction can later merge them. The interval length is set by `segmentGranularity` in the `granularitySpec`.

For good performance under heavy query load, keep segment files in the recommended range of 300 to 700 MB. If files are larger, change the granularity of the segment interval, or partition the data and adjust `targetRowsPerSegment` in your `partitionsSpec`. A good starting point for that parameter is 5 million rows.

Segment files are columnar: each column is laid out in its own data structure, so a query only scans the columns it needs. There are three basic column types: timestamp, dimensions and metrics. Timestamp and metric columns are arrays of integer or floating point values compressed with LZ4; after a query selects rows Druid decompresses them, pulls out the relevant rows and applies the aggregator. Dimension columns support filter and group-by, so each dimension needs additional data structures beyond the raw values: a dictionary, a list of dictionary-encoded values and one bitmap per distinct value.

## Checked

2026-11-09: confirmed against the Druid Segments page (docs/design/segments.md): time-partitioned segment files, no segment for an empty interval, compaction, `segmentGranularity` in the `granularitySpec`, the 300-700 MB range, `targetRowsPerSegment` in the `partitionsSpec` with 5 million rows as a starting point, columnar layout, the three column types, LZ4 compression of timestamp and metric columns, and the three per-dimension structures.

Method: documentation only; no commands were run.
