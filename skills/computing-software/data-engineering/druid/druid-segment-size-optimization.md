---
id: computing-software.data-engineering.druid.druid-segment-size-optimization
name: druid-segment-size-optimization
category: computing-software
field: data-engineering
product: druid
tags: [segment-optimization, rows-per-segment, parallelism, compaction, processing-threads]
level: practitioner
status: docs-checked
description: "Tune segment size for parallelism using the 5 million row guideline."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/segment-optimization.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Segment size matters for two reasons. With best-effort rollup, larger segments can allow more aggregation and so a smaller datasource. And each query goes to all Historicals and real-time tasks holding the input segments, with one thread of each process's processing pool handling one segment. If segments are too large, data is poorly spread over data servers and parallelism drops. If they are too small, scheduling overhead rises and the per-segment threads compete for the fixed slots in the pool.

Best is to get size right at ingestion, but that is hard for streaming because volume varies. In that case create sub-optimal segments first and fix them later with compaction.

Consider:
- Rows per segment: generally around 5 million. This usually matters more than byte size, because one thread processes each segment, so row count directly sets how much each thread does and how well execution parallelises.
- Segment byte size: recommended 300 to 700 MB. If it disagrees with the row-count guidance, tune rows per segment instead. Some deep storage has an upper limit on segment size; S3 deep storage caps at 5 GB.

These are general recommendations. If most queries are heavy and slow per row, smaller segments give more parallelism, so find the optimum for your workload.

To check whether compaction is needed, query the `sys.segments` system table for the datasource with `is_published = 1`, grouped by `"start"`, `"end"` and `version`, and compare `AVG("num_rows")` and `AVG("size")` with the targets. The result can include overshadowed segments, so look only at the max version per interval.

To fix small segments either turn on automatic compaction (the Coordinator or compaction supervisor submits compaction tasks to re-index small segments, configured per datasource), or run periodic batch ingestion jobs that read the Kafka-generated segments with a `druid` input source, which helps when compacting many segments in parallel.

## Checked

2026-11-08. Read operations/segment-optimization.md in full. Added the byte size recommendation (300 to 700 MB), the S3 5 GB cap, the sys.segments check and the compaction options.

Method: documentation only; no commands were run.
