---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-processor-ordering-and-double-pass
name: telegraf-processor-ordering-and-double-pass
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [processors, aggregators, processor-order, skip-processors, double-pass]
level: advanced
status: docs-checked
description: "Explains why processors run twice around aggregators and how to control it with agent skip settings, filters and the order option. Use when aggregate values are transformed twice."
sources: ["https://docs.influxdata.com/telegraf/v1/concepts/data-pipeline/", "https://docs.influxdata.com/telegraf/v1/configure_plugins/aggregator_processor/", "https://docs.influxdata.com/telegraf/v1/configuration/plugin-options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Processor ordering and the second pass

By default processors run twice: once before aggregators, and again on the metrics the aggregators emit. Only aggregates take the second pass; original metrics go to the output buffer without re-processing. The side effect is real: a processor that scales values scales the aggregate a second time.

## Controls in [agent]

- `skip_processors_before_aggregators = true`: processors run only after aggregators.
- `skip_processors_after_aggregators = true`: processors run only before aggregators. The default is scheduled to change to `true` in Telegraf 1.40, and Telegraf logs a warning at startup until you set it explicitly.

## Other options

- Use metric filtering on the processor so aggregate metrics bypass it.
- Make custom processor scripts idempotent so repeated processing has no side effects.

## Order among processors

Processors run in file order unless you set `order` (starting at 1). Processors without `order` run before those that define it, so set `order` on all of them when sequence matters:

```toml
[[processors.rename]]
  order = 1
[[processors.strings]]
  order = 2
```

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Data pipeline page (Processor ordering) and plugin options (order), agent reference (skip_processors_*). Removed: nothing.

Method: documentation only; no commands were run.
