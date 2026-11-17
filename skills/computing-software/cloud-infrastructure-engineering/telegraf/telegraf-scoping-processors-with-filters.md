---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-scoping-processors-with-filters
name: telegraf-scoping-processors-with-filters
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [processors, metric-filtering, namepass, scoping, tagpass]
level: advanced
status: docs-checked
description: "Shows how to limit a processor or aggregator to selected metrics with namepass, tagpass and related filters so other metrics bypass it unchanged."
sources: ["https://docs.influxdata.com/telegraf/v1/configure_plugins/aggregator_processor/", "https://docs.influxdata.com/telegraf/v1/configuration/filtering/", "https://docs.influxdata.com/telegraf/v1/concepts/data-pipeline/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scoping processors and aggregators with filters

Processor and aggregator filters apply before the plugin runs. A metric the filters reject is not dropped; it skips that plugin and continues downstream unchanged. That makes filters the way to apply a transform to some metrics only.

```toml
[[processors.override]]
  namepass = ["cpu*"]
  [processors.override.tags]
    environment = "production"
```

Only measurements matching `cpu*` receive the tag.

## Typical uses

- Keep aggregate metrics out of a processor to avoid the second-pass problem (see the ordering skill).
- Limit an aggregator to the measurements you want summarised. Use `taginclude` on the aggregator to group by chosen tags only.
- Split pipelines by destination using output filters, so each output receives a different subset.

## Choose cheap selectors

`namepass`, `tagpass` and the other glob selectors are fast. `metricpass` (CEL) is interpreted and much slower; avoid it in high-throughput paths when a simpler selector works.

Remember that explicit-table `tagpass` must be last in the plugin definition because later keys would otherwise be read as part of the table.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Data pipeline page (where filtering happens) and Metric filtering page (tagpass table placement, metricpass CEL speed). Removed: nothing.

Method: documentation only; no commands were run.
