---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.buffering-modes
name: buffering-modes
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, buffering, chunks, memrb, filesystem-buffering, storage-type, up-down-chunks]
level: practitioner
status: docs-checked
description: "Choose memory, filesystem or memory ring buffer buffering per input and understand chunks, up and down states."
sources: ["https://docs.fluentbit.io/manual/pipeline/buffering"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Buffering modes

Ingested data is buffered in memory before processing and routing. Records are grouped into **chunks** of about 2 MB on average. Buffered data uses Fluent Bit's internal binary representation and is immutable. Chunks held in both memory and the filesystem are `up`; those only on the filesystem are `down`. A `down` chunk becomes `up` when a copy is written to memory. After an `up` chunk is routed, both copies are flushed. Chunks with a bad layout or invalid header size are marked irrecoverable, logged and discarded.

Set the mode per input with `storage.type`:

- **memory** (memory-only): fastest and lowest overhead, but most prone to data loss.
- **filesystem** (hybrid): each chunk is stored via mmap, plus an identical memory copy when space allows. Less efficient, less prone to loss. Needs `storage.path` in the service section.
- **memrb** (memory ring buffer): when full, the oldest chunks are dropped instead of pausing the input. Dropped totals appear in the `memrb_dropped_chunks` and `memrb_dropped_bytes` metrics. Use when recent data matters more than completeness.

Set a default with service `storage.type` plus `storage.inherit: on`; inputs that set their own `storage.type` override it.

```yaml
service:
  storage.path: /var/log/flb-storage/
  storage.type: filesystem
  storage.inherit: on
pipeline:
  inputs:
    - name: cpu
    - name: mem
      storage.type: memory
```

Limits for each mode are in `computing-software.cloud-infrastructure-engineering.fluent-bit.backpressure-memory-buffering` and `computing-software.cloud-infrastructure-engineering.fluent-bit.backpressure-filesystem-buffering`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Buffering page: chunk size, up and down chunks, irrecoverable chunks, the three modes, memrb metrics, global default with storage.inherit, and the example.

Method: documentation only; no commands were run.
