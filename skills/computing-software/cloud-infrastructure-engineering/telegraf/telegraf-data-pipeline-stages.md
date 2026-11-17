---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-data-pipeline-stages
name: telegraf-data-pipeline-stages
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [data-pipeline, inputs, processors, aggregators, outputs]
level: intro
status: docs-checked
description: "Describes the Telegraf pipeline from input plugins through processors, aggregators and the output buffer to outputs. Use to reason about where a metric is changed or dropped."
sources: ["https://docs.influxdata.com/telegraf/v1/concepts/data-pipeline/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Telegraf data pipeline

Every metric follows one path: input plugins collect it, processors and aggregators transform it, and output plugins write it. Processors and aggregators are optional; with none configured, metrics go straight from inputs to the output buffer.

## Stages

- **Collect**: on each collection interval Telegraf calls every polling input. Service inputs emit metrics as data arrives instead. Inputs reading raw data (files, queues, HTTP) use a parser chosen by `data_format`. Input metric filters apply after gathering, so only passing metrics enter the pipeline.
- **Process**: processors act on each metric and emit the result. Metrics not matching a processor's filters bypass it unchanged.
- **Aggregate**: aggregators collect matching metrics into a window set by `period` and emit aggregates at its end.
- **Write**: outputs write in batches of up to `metric_batch_size`, on every `flush_interval`, or sooner when a full batch is ready. Output filters apply before writing, so each output can receive a different subset.

## Where filters apply

Input: after gathering. Processor and aggregator: before processing, non-matching metrics pass downstream. Output: before writing.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Data pipeline page: stages, batching and where filtering happens. Removed: nothing.

Method: documentation only; no commands were run.
