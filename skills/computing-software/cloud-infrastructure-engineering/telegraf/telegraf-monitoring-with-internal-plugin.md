---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-monitoring-with-internal-plugin
name: telegraf-monitoring-with-internal-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [monitoring, internal-plugin, self-metrics, buffer-size, metrics-dropped]
level: practitioner
status: docs-checked
description: "Shows how to monitor Telegraf itself with the internal input: measurements to watch, buffer saturation and per-instance stats via alias."
sources: ["https://docs.influxdata.com/telegraf/v1/administer/monitor/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Monitoring Telegraf with the internal input

The internal input emits metrics about the running process and its plugins through the normal pipeline.

```toml
[[inputs.internal]]
  collect_memstats = true
  # collect_gostats = false
  # per_instance = false
```

## Measurements

- `internal_agent`: totals such as `metrics_gathered`, `metrics_written`, `metrics_dropped`, `gather_errors`, `gather_timeouts`.
- `internal_gather`: per-input stats such as `gather_time_ns` and `gather_timeouts`.
- `internal_write`: per-output stats such as `buffer_size`, `buffer_limit`, `metrics_dropped`.
- `internal_memstats`: Go memory stats.

Watch `internal_write`: a `buffer_size` climbing toward `buffer_limit` means the output cannot keep up and metrics will be dropped when the buffer fills.

## Instances

Plugins that set `alias` report per-instance statistics with the alias as a tag. `per_instance` collects stats per instance rather than per plugin type.

## Fleet monitoring

Agents running the heartbeat output report to Telegraf Controller on an interval with agent metrics, error counts, plugin statistics and a status computed from CEL expressions in the plugin config. Controller marks agents that stop reporting.

## Checked

Method: docs-checked 2026-11-09 against the Monitor Telegraf page (raw markdown in github.com/influxdata/docs-v2, read in full). All claims confirmed.
