---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-metric-filtering
name: telegraf-metric-filtering
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [filtering, namepass, tagpass, fieldinclude, metricpass, cel]
level: practitioner
status: docs-checked
description: "Telegraf selectors (namepass, namedrop, tagpass, tagdrop, metricpass) and modifiers (fieldinclude, taginclude and excludes) to scope what each plugin handles."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/filtering/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Metric filtering

Filters attach to any input, output, processor or aggregator. None are set by default.

## Selectors: include or exclude whole metrics

- `namepass` / `namedrop`: glob lists on the measurement name. `namedrop` is tested after `namepass`. `namepass_separator` and `namedrop_separator` exclude separator characters from wildcards, useful for dot-delimited names.
- `tagpass` / `tagdrop`: tables of tag key to glob list. Conditions across keys combine with OR.
- `metricpass`: a CEL expression returning true to pass. Variables: `name`, `tags`, `fields`, `time`. A runtime failure, such as reading a missing field, logs an error and passes the metric. CEL is interpreted and much slower than the other selectors, so avoid it on high-throughput paths.

A rejected metric is dropped by inputs and outputs; processors and aggregators let it continue downstream unchanged.

## Modifiers: trim tags and fields

`fieldinclude`, `fieldexclude`, `taginclude`, `tagexclude`. If a modifier removes all fields, the metric is dropped. `taginclude` removes tags, unlike `tagpass`, which passes or rejects the whole metric.

## TOML trap

Explicit-table `tagpass` or `tagdrop` (`[inputs.cpu.tagpass]`) must be at the end of the plugin definition. Inline tables (`tagpass = {...}`) must be in the main plugin definition.

`always_include_local_tags` and `always_include_global_tags` in `[agent]` keep tags through `taginclude`/`tagexclude`.

## Checked

Method: docs-checked 2026-11-09 against the Filter Telegraf metrics page (raw markdown in github.com/influxdata/docs-v2, read in full). All claims confirmed; the data-pipeline page was not needed for these claims.
