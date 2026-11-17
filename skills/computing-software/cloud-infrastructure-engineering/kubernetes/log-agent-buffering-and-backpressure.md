---
id: computing-software.cloud-infrastructure-engineering.kubernetes.log-agent-buffering-and-backpressure
name: log-agent-buffering-and-backpressure
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, logging-architecture, log-backpressure, fluent-bit, vector, buffering]
level: practitioner
status: docs-checked
description: "Configure buffering and backpressure in Fluent Bit, Vector and the OTel Collector so log bursts and sink outages neither OOM the agent nor silently drop logs."
sources: ["https://docs.fluentbit.io/manual/data-pipeline/buffering", "https://docs.fluentbit.io/manual/administration/backpressure", "https://vector.dev/docs/architecture/buffering-model/", "https://opentelemetry.io/docs/collector/resiliency/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log agent buffering and backpressure

When the sink slows or fails, the agent must either buffer, slow down reading, or drop. Pick
deliberately; the kubelet keeps rotating container logs (`containerLogMaxSize` 10Mi,
`containerLogMaxFiles` 5 by default), so an agent that pauses too long loses unread files anyway.

## Fluent Bit
```ini
[SERVICE]
    storage.path              /var/fluent-bit/state/flb-storage/
    storage.sync              normal
    storage.backlog.mem_limit 50M
    storage.max_chunks_up     128

[INPUT]
    Name          tail
    Path          /var/log/containers/*.log
    storage.type  filesystem          # hybrid memory + filesystem buffering

[OUTPUT]
    Name                      loki
    Match                     kube.*
    storage.total_limit_size  5G      # oldest chunks dropped beyond this
    Retry_Limit               False   # no retry limit (or a number; default 1)
```
`Mem_Buf_Limit` applies to memory-only buffering: the input pauses when it is reached, and some
inputs lose data while paused, which is why filesystem buffering is used here. With filesystem
buffering, `storage.max_chunks_up` caps chunks held in memory. Mount `/var/fluent-bit/state` from
a hostPath so buffers survive pod restarts. Watch `fluentbit_output_retries_failed_total` (chunks
discarded after `Retry_Limit`), `fluentbit_output_dropped_records_total` and
`fluentbit_input_storage_overlimit`.

## Vector
```yaml
sinks:
  loki:
    type: loki
    buffer: {type: disk, max_size: 5368709120, when_full: block}   # or drop_newest
```
`block` is the default `when_full` behaviour. Disk buffers have a minimum size of about 256 MiB.

## OpenTelemetry Collector
`memory_limiter` as the first processor in the pipeline (the documented best practice);
exporter `sending_queue` with `storage: file_storage` (the `file_storage` extension) for
persistence across restarts; `retry_on_failure` with `max_elapsed_time` (default 300s).

## Choosing
- Audit and security logs: block plus disk buffer; alert on buffer growth.
- Debug logs: drop_newest under pressure is acceptable.
Set agent memory limits above the in-memory buffer sizes, or the agent OOMs during a burst.

## Verify
Block the sink (scale Loki to 0) for 10 minutes; the agent's disk buffer grows, memory stays
below limit, and all logs arrive after the sink returns.

## Checked
2026-10-27 against the kubelet configuration reference (kubernetes/website main, v1.38
development tree; v1.37 is the latest release), Fluent Bit docs (fluent/fluent-bit-docs master:
buffering, backpressure, scheduling and retries, monitoring), Vector's buffering model page,
the OpenTelemetry Collector resiliency page and the memory_limiter processor README. Confirmed:
`containerLogMaxSize` 10Mi and `containerLogMaxFiles` 5 defaults; the Fluent Bit storage keys,
`storage.total_limit_size` dropping the oldest chunks, `Retry_Limit False`, and the metric names;
Vector `when_full` values and default; the Collector settings and defaults. Fixed: `Mem_Buf_Limit`
was paired with filesystem buffering as if it caused spilling to disk.
Method: documentation only; no commands were run.
