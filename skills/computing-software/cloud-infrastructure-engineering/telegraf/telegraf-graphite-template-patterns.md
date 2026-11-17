---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-graphite-template-patterns
name: telegraf-graphite-template-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [graphite, templates, template-patterns, measurement, dot-delimited]
level: advanced
status: docs-checked
description: "Explains Telegraf template patterns that map dot-delimited strings such as Graphite buckets to measurement, tags and fields, with filters and extra tags."
sources: ["https://docs.influxdata.com/telegraf/v1/data_formats/template-patterns/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Template patterns

A template maps a dot-delimited string to and from a Telegraf metric, for example `host.mytag.mytag.measurement.measurement.field*`.

## Keywords

- `measurement`: this segment is part of the measurement name; may repeat.
- `field`: segment is part of the field name; may repeat.
- `measurement*` / `field*`: all remaining segments.
- Any other word is a tag key.

`measurement` must be present, and `field*` cannot be combined with `measurement*`.

## Examples

```toml
templates = ["region.region.measurement*"]
```
maps `us.west.cpu.load 100` to `cpu.load,region=us.west value=100`.

```toml
separator = "_"
templates = ["measurement.measurement.field.field.region"]
```
maps `cpu.usage.idle.percent.eu-east 100` to `cpu_usage,region=eu-east idle_percent=100`.

## Filters

A glob before the template selects by bucket name:

```toml
templates = [
  "cpu.* measurement.measurement.region",
  "mem.* measurement.measurement.host"
]
```

Several unfiltered templates can also be told apart by shape, for example `*.*.*` for 3-part names and `*.*.*.*` for 4-part names.

## Extra tags

Append line-protocol style tags after the template: `"measurement.measurement.field.region datacenter=1a"`.

## Checked

Method: docs-checked 2026-11-09 against the influxdata docs-v2 source for Telegraf template patterns, read in full.
