---
id: computing-software.data-engineering.druid.druid-rollup-at-ingestion
name: druid-rollup-at-ingestion
category: computing-software
field: data-engineering
product: druid
tags: [rollup, pre-aggregation, query-granularity, granularity-spec, rollup-ratio]
level: practitioner
status: docs-checked
description: "Decide whether to use rollup and measure the rollup ratio."
sources:
  - https://github.com/apache/druid/blob/master/docs/ingestion/rollup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rollup is a form of summarisation or pre-aggregation at ingestion time. It can shrink stored data and row counts by orders of magnitude, at the cost of losing the ability to query individual events. It is controlled by the `rollup` setting in the `granularitySpec` and is enabled by default: rows with identical dimension values and identical timestamps after `queryGranularity` truncation are combined into one row. With rollup off, Druid loads each row as it is.

Use rollup when you want optimal performance or have strict space limits, and you do not need raw values from high-cardinality dimensions. Disable it if you need results for individual rows, or need GROUP BY or WHERE on any column. If use cases conflict, create multiple tables with different rollup settings.

To measure the rollup ratio compare the row count in Druid with the number of ingested events. If `num_rows` is a count-type metric made at ingestion:

```sql
SELECT SUM("num_rows") / (COUNT(*) * 1.0) FROM datasource
```

The higher the result, the greater the benefit from rollup.

To maximize rollup:
- Use fewer dimensions and lower-cardinality dimensions.
- Use sketches instead of storing high-cardinality dimensions.
- Coarsen `queryGranularity`, for example `PT5M` instead of `PT1M`, so more rows share timestamps.
- Optionally load the same data into a "full" datasource with rollup off (or minimal ratio) and an "abbreviated" one with fewer dimensions and a higher ratio, and use the second when queries only need its dimensions.
- If your ingestion method is best-effort, switch to a perfect rollup method or reindex or compact in the background afterwards.

Perfect versus best-effort: perfect rollup aggregates input fully at ingestion, using an extra preprocessing step that scans the whole input to determine intervals and partitioning, which adds ingestion time. Best-effort methods may leave rows with the same timestamp and dimensions in different segments, because they parallelize without a shuffle or publish segments incrementally before a time chunk is complete. SQL-based batch is always perfect; Kafka and Kinesis indexing are always best-effort; native batch (`index_parallel` and `index`) can be either depending on configuration.

## Checked

2026-11-08. Read ingestion/rollup.md in full. Added rollup maximization tips and perfect versus best-effort rollup per ingestion method.

Method: documentation only; no commands were run.
