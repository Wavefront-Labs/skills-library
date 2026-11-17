---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.batch-processor-placement
name: batch-processor-placement
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, processors, batch, throughput, ordering]
level: practitioner
status: docs-checked
description: "Place the batch processor after sampling and enrichment and tune timeout and batch size."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The batch processor groups spans, metric data points or log records into batches, which compresses better and reduces the outgoing connections needed. It supports size-based and time-based batching.

```yaml
processors:
  batch:
  batch/2:
    send_batch_size: 10000
    timeout: 10s
```

A second form enforces a maximum without delay:

```yaml
processors:
  batch:
    send_batch_max_size: 10000
    timeout: 0s
```

Details from the README:

- Place it after `memory_limiter` and after any sampling processors, because batching should happen after data is dropped.
- `send_batch_size` (default 8192) is a trigger and does not limit batch size. `timeout` (default 200ms) sends regardless of size; zero ignores `send_batch_size`.
- `send_batch_max_size` (default 0, no limit) splits larger batches and must be at least `send_batch_size`.
- `metadata_keys` creates one batcher per distinct combination of `client.Metadata` values, for multi-tenant pipelines, capped by `metadata_cardinality_limit` (default 1000). Receivers need `include_metadata: true`.
- A processor referenced in several pipelines gets a separate instance in each.
- Exporters can also batch inside `sending_queue` with `batch`, which is off by default.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md
- https://opentelemetry.io/docs/collector/configuration/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
