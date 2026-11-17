---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-output-buffering-and-delivery
name: telegraf-output-buffering-and-delivery
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [buffer, metric-buffer-limit, disk-buffer, flush-interval, delivery]
level: practitioner
status: docs-checked
description: "Covers per-output buffers, metric_buffer_limit, the memory and disk buffer strategies and buffer_directory. Use when sizing buffers or surviving destination outages."
sources: ["https://docs.influxdata.com/telegraf/v1/concepts/data-pipeline/", "https://docs.influxdata.com/telegraf/v1/configuration/agent/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Output buffering and delivery

Each output plugin has its own buffer holding metrics awaiting a successful write. If a destination is unreachable, metrics accumulate up to `metric_buffer_limit` (default 10000) and Telegraf retries on the next flush.

## Strategies (agent buffer_strategy)

- `memory` (default): buffered metrics live only in memory. When the buffer fills, the oldest metrics are dropped to make room, and everything buffered is lost if Telegraf stops.
- `disk`: each output persists its buffer to a write-ahead log in `buffer_directory` and removes entries as writes succeed. After a restart Telegraf flushes existing entries before new metrics. Telegraf does not limit the disk space used, so monitor the directory.

```toml
[agent]
  buffer_strategy = "disk"
  buffer_directory = "/var/lib/telegraf/buffer"
  buffer_disk_sync = true
```

Each output creates its own subdirectory. `buffer_directory` is required for `disk`. `buffer_disk_sync` defaults to true; disabling it speeds writes at the risk of losing the last flush interval of metrics in a power failure.

Raising `metric_buffer_limit` tolerates longer downtime at the cost of memory. Batch size, flush interval and the buffer limit can be overridden per output.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Data pipeline page (Buffering and delivery) and agent reference (buffer_strategy, buffer_directory, buffer_disk_sync, metric_buffer_limit). Removed: nothing.

Method: documentation only; no commands were run.
