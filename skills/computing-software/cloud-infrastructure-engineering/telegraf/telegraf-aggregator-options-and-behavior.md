---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-aggregator-options-and-behavior
name: telegraf-aggregator-options-and-behavior
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [aggregators, period, delay, grace, drop-original]
level: practitioner
status: docs-checked
description: "Covers aggregator period, delay, grace and drop_original and how aggregates are grouped. Use when configuring windowed aggregates like mean, min and max."
sources: ["https://docs.influxdata.com/telegraf/v1/configure_plugins/aggregator_processor/", "https://docs.influxdata.com/telegraf/v1/configuration/plugin-options/", "https://docs.influxdata.com/telegraf/v1/concepts/data-pipeline/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Aggregator options and behaviour

Aggregators produce new aggregate metrics (mean, min, max, quantiles, standard deviation) from many metrics over time. Use a processor when the change needs only the metric in hand.

## Options

- `period`: window size, default `"30s"`. Metrics with timestamps outside the current period are ignored; metrics older than `now() - period` are not included.
- `delay`: how long to wait before flushing so inputs on the same interval can deliver. Default `"100ms"`.
- `grace`: how long late metrics are still accepted into the next period. Default `"0s"`.
- `drop_original`: default false. By default aggregators emit aggregates and also pass the originals downstream; set true to emit only aggregates.

## Grouping

Aggregates are created per unique combination of measurement, field and tag set. Use `taginclude` to group by specific tags only.

## Interaction with processors

Aggregates take a second trip through processors by default; see the processor ordering skill. Aggregator filters apply before aggregation, and non-matching metrics pass on without being aggregated.

## Downsampling

The aggregator docs include a downsample-before-writing pattern: aggregate over a period with `drop_original = true` so only summarised metrics reach the output.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Plugin options (period, delay, grace, drop_original defaults), data pipeline and aggregator pages (grouping, now() - period, downsample section). Removed: nothing.

Method: documentation only; no commands were run.
