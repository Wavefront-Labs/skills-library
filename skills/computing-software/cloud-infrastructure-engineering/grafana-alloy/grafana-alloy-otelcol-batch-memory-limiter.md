---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-otelcol-batch-memory-limiter
name: grafana-alloy-otelcol-batch-memory-limiter
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [otelcolprocessorbatch, otelcolprocessormemory-limiter, send-batch-size, spike-limit, soft-hard-limit, limit-percentage]
level: practitioner
status: docs-checked
description: "Configure otelcol.processor.batch and memory_limiter: send_batch_size versus send_batch_max_size, timeout, hard and soft limit arithmetic, and where each sits in the pipeline."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/components/otelcol/otelcol.processor.batch.md", "https://github.com/grafana/alloy/blob/main/docs/sources/reference/components/otelcol/otelcol.processor.memory_limiter.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Batch and memory_limiter processors

## otelcol.processor.batch
Defaults: `send_batch_size` 2000, `send_batch_max_size` 3000, `timeout` "200ms", `metadata_keys` [], `metadata_cardinality_limit` 1000.

A batch flushes when `timeout` elapses since the last send or when the item count (spans, log records or metric data points) reaches `send_batch_size`. That value is a trigger, not a cap: large incoming chunks can exceed it unless `send_batch_max_size` is set. `send_batch_max_size = 0` means unlimited; otherwise it must be at least `send_batch_size`. Logs, traces and metrics are batched independently. Place batching after anything that drops data, such as sampling.

```alloy
otelcol.processor.batch "default" {
  send_batch_size     = 2000
  send_batch_max_size = 3000
  timeout             = "200ms"
  output {
    traces = [otelcol.exporter.otlp.default.input]
  }
}
```

## otelcol.processor.memory_limiter
`check_interval` is required. Set either `limit` (for example "1GiB") or the pair `limit_percentage` plus `spike_limit_percentage`, never both. `limit` and `limit_percentage` are the hard limits; the soft limit is the hard limit minus `spike_limit` (default 20% of `limit`). Below the soft limit nothing is dropped and no GC is forced.

GC pacing defaults: `min_gc_interval_when_soft_limited` 10s, `max_gc_interval_when_soft_limited` 30s, `min_gc_interval_when_hard_limited` 0s, `max_gc_interval_when_hard_limited` 30s.

Connect the limiter directly to the receivers, before every other processor, so receivers can retry refused data and apply backpressure to senders.

## Checked
2026-11-04: confirmed against the otelcol.processor.batch and otelcol.processor.memory_limiter reference pages. Removed: nothing.
Method: documentation only; no commands were run.
