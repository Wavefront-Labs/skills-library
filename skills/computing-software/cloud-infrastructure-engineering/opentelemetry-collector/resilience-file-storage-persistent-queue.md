---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.resilience-file-storage-persistent-queue
name: resilience-file-storage-persistent-queue
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, resiliency, file-storage, persistent-queue, wal]
level: advanced
status: docs-checked
description: "Persist the exporter queue to disk with the file_storage extension so queued data survives Collector restarts."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/extension/storage/filestorage/README.md
  - https://opentelemetry.io/docs/collector/resiliency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An in-memory sending queue is lost if the Collector crashes. To protect against that, the resiliency page has the queue write to a write-ahead log on disk through the `file_storage` extension, so on restart the Collector reads the data back and resumes sending.

```yaml
extensions:
  file_storage:
    directory: /var/lib/otelcol/storage
exporters:
  otlp:
    endpoint: otlp.example.com:4317
    sending_queue:
      storage: file_storage
service:
  extensions: [file_storage]
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [otlp]
```

Details from the pages and READMEs:

- Setting `sending_queue::storage` enables persistence and there is then no in-memory queue. `queue_size` still caps stored batches and defaults to 1000.
- The extension needs read and write access to its directory, which must already exist unless `create_directory` is set. The default directory is `/var/lib/otelcol/file_storage` outside Windows.
- `max_size` limits each database file, with `0` meaning unlimited; a write beyond it is rejected.
- `fsync` forces a sync after each write, trading performance for integrity.
- `compaction.on_start` and `compaction.on_rebound` shrink the file, both off by default.
- Loss is still possible if the disk fails or fills, and auth-extension context is not kept in a persistent queue.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/README.md
- https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/extension/storage/filestorage/README.md
- https://opentelemetry.io/docs/collector/resiliency/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
