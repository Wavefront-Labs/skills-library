---
id: computing-software.cloud-infrastructure-engineering.observability.log-pipeline-buffering-and-backpressure
name: log-pipeline-buffering-and-backpressure
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [log-pipeline-backpressure, log-buffering, log-pipeline, fluent-bit, otel-collector, persistent-queue]
level: advanced
status: docs-checked
description: "Size buffers and choose backpressure behaviour (block, drop, spill to disk) in Fluent Bit, OTel Collector and Vector so backend outages do not lose or stall logs."
sources: ["https://docs.fluentbit.io/manual/data-pipeline/buffering", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/memorylimiterprocessor/README.md", "https://vector.dev/docs/architecture/buffering-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log pipeline buffering and backpressure

When the backend slows or fails, something must give: memory, disk, the application, or the data. Decide explicitly.

## Fluent Bit
```ini
[SERVICE]
    storage.path              /var/fluent-bit/state
    storage.sync              normal
    storage.backlog.mem_limit 50M
[INPUT]
    Name          tail
    Path          /var/log/containers/*.log
    storage.type  filesystem      # chunks also kept on disk
[OUTPUT]
    Name                     loki
    storage.total_limit_size 5G   # oldest queued chunks discarded beyond this
```
- `storage.type` is per input: `memory` (default), `filesystem` (hybrid: every chunk is also
  written to disk, less prone to loss) or `memrb`. Filesystem buffering needs a global `storage.path`.
- With `memory`, hitting `mem_buf_limit` pauses the input plugin until memory frees up, so a
  tailed file can rotate away meanwhile (data loss). `mem_buf_limit` has no limit by default.
- `memrb` is a fixed-size memory ring buffer: when full it drops the oldest chunks instead of
  pausing the input, and counts them in `memrb_dropped_chunks` and `memrb_dropped_bytes`.
- Chunks average about 2 MB.

## OTel Collector
```yaml
extensions:
  file_storage: {directory: /var/lib/otelcol/queue}
exporters:
  otlphttp/loki:
    sending_queue: {enabled: true, storage: file_storage, queue_size: 10000, num_consumers: 10}
    retry_on_failure: {enabled: true, max_elapsed_time: 0}  # 0 = retry forever
```
- `sending_queue` defaults: `enabled` true, `queue_size` 1000 (units set by `sizer`, default
  `requests`), `num_consumers` 10, `block_on_overflow` false. Setting `storage` makes the queue
  persistent and there is then no in-memory queue.
- If data cannot be added to the queue (full, or the storage cannot take it) it is typically
  dropped; `block_on_overflow: true` makes the caller wait for space instead. Enqueue failures
  are counted by the `otelcol_exporter_enqueue_failed_*` metrics.
- `retry_on_failure` defaults: `initial_interval` 5s, `max_interval` 30s, `max_elapsed_time`
  300s, `multiplier` 1.5.
- The `memory_limiter` processor starts refusing data when memory passes its limit
  (`limit_mib`, `spike_limit_mib`, `check_interval`).
- Auth extension context is not kept when items go through a persistent queue.

## Vector
`buffer: {type: disk, max_size: 5368709120, when_full: block}` or `drop_newest`. `block` is the
default `when_full` and waits indefinitely, which pushes backpressure upstream; `drop_newest`
sheds load. Buffers can be stacked with `when_full: overflow`; the last buffer must block or drop.

## Sizing
Buffer size = ingest rate x outage you must survive. 2 MB/s x 30 min = 3.6 GB per node.

## Gotchas
- Disk buffers on the node's root filesystem can fill the node; use a dedicated volume or cap size.
- `block` propagates backpressure to apps that log synchronously to stdout pipes; most runtimes buffer, but a full pipe stalls writes.
- Retries without backoff amplify backend outages; keep exponential backoff.

## Verify
- [ ] Block the backend for 10 minutes in staging; after recovery all lines arrive (count compare).
- [ ] Alerts exist on buffer usage and drops (`memrb_dropped_chunks`, `otelcol_exporter_enqueue_failed_*`).

## Checked
2026-10-31. Confirmed against the Fluent Bit buffering page (`storage.type` values, `mem_buf_limit` behaviour, `memrb` and its metrics, `storage.total_limit_size`, `storage.backlog.mem_limit`, 2 MB chunks), the Collector exporterhelper README (queue and retry defaults, persistent queue, `block_on_overflow`, enqueue-failure metrics), the memory limiter README (refuses data above its limit) and the Vector buffering-model page (`block` default, `drop_newest`, `overflow`, disk `max_size`/`when_full`). Removed as unconfirmed: `Retry_Limit False`, `fluentbit_storage_*` and `otelcol_exporter_queue_size` metric names, the `Mem_Buf_Limit 50MB` input line, and the claim about receivers returning retryable errors.
Method: documentation only; no commands were run.
