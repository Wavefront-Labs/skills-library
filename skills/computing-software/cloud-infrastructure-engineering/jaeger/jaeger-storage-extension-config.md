---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-storage-extension-config
name: jaeger-storage-extension-config
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, jaeger-storage, metric-backends, storage-backends-yaml, jaeger-storage-exporter]
level: practitioner
status: docs-checked
description: "Declare named trace and metrics backends once in the jaeger_storage extension and reference them from the exporter and query."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: share one storage definition between writers and readers.

The OpenTelemetry Collector normally has an exporter per destination, but Jaeger also reads data via the UI and query APIs. The `jaeger_storage` extension therefore holds all backends, which other components reference by name:
```
jaeger_storage:
  backends:
    some_trace_storage:
      memory:
        max_traces: 100000
  metric_backends:
    some_metrics_storage:
      prometheus:
        endpoint: http://prometheus:9090
        normalize_calls: true
        normalize_duration: true
```
- `backends` is a dictionary of trace backends; `metric_backends` a dictionary of metrics backends.
- The key names (some_trace_storage) are free names you reference elsewhere.
- The next key is the backend type (memory and prometheus in this example).

Writing: `jaeger_storage_exporter` sends data to any registered backend:
```
jaeger_storage_exporter:
  trace_storage: some_trace_storage
  queue:
    num_consumers: 10
    queue_size: 100
```
Failure mode: a queue configured like this acknowledges spans as soon as they are enqueued, before the storage wrote them. If the pipeline must not lose spans, set `wait_for_result: true` and do not use the batch processor.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 Configuration page, read in full (jaeger_storage extension, jaeger_storage_exporter, queue and wait_for_result note).

Method: documentation only; no commands were run.
