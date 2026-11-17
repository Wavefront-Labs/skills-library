---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-processors-versus-aggregators
name: telegraf-processors-versus-aggregators
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [processors, aggregators, override-processor, rename, downsample]
level: intro
status: docs-checked
description: "Helps decide between processor and aggregator plugins in Telegraf and shows the override processor adding static tags."
sources: ["https://docs.influxdata.com/telegraf/v1/configure_plugins/aggregator_processor/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Processors versus aggregators

Both sit between inputs and outputs. Metrics from every input flow through the same stages, and results fan out to every output whose filters they pass.

## Processor

Acts on each metric as it passes and emits the result at once. Use when the change needs only the metric in hand: renaming, converting units, adding tags, running calculations.

```toml
[[processors.override]]
  [processors.override.tags]
    environment = "production"
    region = "us-west"
```

Before: `cpu,cpu=cpu0 usage_idle=92.4 1709572232000000000`. After: `cpu,cpu=cpu0,environment=production,region=us-west usage_idle=92.4 1709572232000000000`.

## Aggregator

Produces new aggregate metrics (running mean, min, max, quantiles, standard deviation) over a time window. Use when the result depends on many metrics over time. Every aggregator has a `period`.

Behaviours to remember: only metrics with timestamps inside the current period count; originals pass downstream unless `drop_original = true`; aggregates are per measurement, field and tag set.

Scope either type with metric filtering so only relevant metrics enter it, and see the ordering skill for the double pass.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Aggregator and processor plugins page and data pipeline page: override example, processor and aggregator behaviour. Removed: unconfirmed processor uses (converting types, mapping values).

Method: documentation only; no commands were run.
