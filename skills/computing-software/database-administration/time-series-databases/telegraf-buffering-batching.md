---
id: computing-software.database-administration.time-series-databases.telegraf-buffering-batching
name: telegraf-buffering-batching
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-telegraf, telegraf-buffering-batching, influxdb, telegraf]
level: practitioner
status: draft
description: "Prevent metric loss during outages and tune write size for Telegraf outputs."
sources:
  - https://docs.influxdata.com/influxdb/v2/
  - https://docs.influxdata.com/telegraf/v1/
  - https://docs.influxdata.com/influxdb3/core/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Telegraf buffering and batching

**Goal:** Prevent metric loss during outages and tune write size for Telegraf outputs.

## Steps
- `metric_batch_size` (default 1000, confirm) points per write; `metric_buffer_limit` (default 10000, confirm) points held in memory when the output fails.
- Raise the buffer for longer outages: `metric_buffer_limit = 100000`; memory grows with it.
- `flush_jitter = "5s"` staggers many agents so they do not hit the server together.
- `collection_jitter` spreads input collection.
- Newer versions can spill the buffer to disk (`buffer_strategy = "disk"`, confirm availability); otherwise memory is the only buffer.
- Watch the `internal` input for `buffer_size`, `metrics_dropped`, `write_errors`.

**Gotcha:** When the buffer fills, the oldest metrics are dropped while collection continues; the only sign is the `metrics_dropped` counter.

## Verify
- `inputs.internal` shows `metrics_dropped` of 0 during a simulated outage shorter than the buffer.
- After restoring the output, buffered points arrive with original timestamps.
