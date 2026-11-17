---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.resilience-sending-queue-and-retry
name: resilience-sending-queue-and-retry
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, resiliency, sending-queue, retry-on-failure, exporter]
level: practitioner
status: docs-checked
description: "Tune exporter retry_on_failure and sending_queue to survive backend outages without losing data."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md
  - https://opentelemetry.io/docs/collector/resiliency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Exporters usually include a sending queue that buffers data in memory before sending, with a retry mechanism using exponential backoff and jitter. If the endpoint is unavailable, data is queued instead of dropped.

```yaml
exporters:
  otlp:
    endpoint: otlp.example.com:4317
    sending_queue:
      queue_size: 5000
    retry_on_failure:
      initial_interval: 5s
      max_interval: 30s
      max_elapsed_time: 10m
```

Details from the resiliency page and exporter helper README:

- Retry defaults: `initial_interval` 5s, `max_interval` 30s, `max_elapsed_time` 300s (0 never stops), `multiplier` 1.5.
- Queue defaults: `enabled` true, `queue_size` 1000, `num_consumers` 10, and `sizer` `requests`; alternatives are `items` and `bytes`.
- If the endpoint stays down longer than `max_elapsed_time`, the oldest data is dropped. If the queue fills, new data is dropped.
- `block_on_overflow` (default false) makes the caller wait instead of rejecting.
- Data rejected before entering the queue skips retry and is counted by `otelcol_exporter_enqueue_failed_*`.
- `timeout` (default 5s) bounds each send attempt.
- Monitor `otelcol_exporter_queue_size`, `otelcol_exporter_queue_capacity` and `otelcol_exporter_send_failed_spans`.
- Enable queues for every exporter that sends over a network.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md
- https://opentelemetry.io/docs/collector/resiliency/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
