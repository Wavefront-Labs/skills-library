---
id: computing-software.cloud-infrastructure-engineering.fluentd.buffer-size-limits-and-compression
name: buffer-size-limits-and-compression
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, buffer, chunk-limit-size, total-limit-size, compress, overflow-action]
level: practitioner
status: docs-checked
description: "Size a Fluentd buffer: chunk_limit_size, total_limit_size, chunk_full_threshold, queued_chunks_limit_size, compress, and overflow_action."
sources:
  - https://docs.fluentd.org/configuration/buffer-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd buffer sizing
- `chunk_limit_size`: default 8MB (memory) / 256MB (file).
- `chunk_limit_records`: optional cap on events per chunk.
- `total_limit_size`: default 512MB (memory) / 64GB (file). When reached, append operations fail and data is lost.
- `chunk_full_threshold` (default 0.95): a chunk flushes at `chunk_limit_size * threshold`.
- `queued_chunks_limit_size` (since v1.1.3, default 1, same as `flush_thread_count`): limits queued chunks; helps limit file descriptors with small `flush_interval` when the destination is down.
- `queue_limit_length`: v0.12 compatibility only; use `total_limit_size`.
- `compress`: `text` (default), `gzip`, or `zstd` (since v1.19.0). Chunks are decompressed automatically when sent, unless the output can pass compressed data as is.
- `decompression_size_limit` (since v1.19.3, default 256MB): aborts decompression with `Fluent::Plugin::Extractor::SizeLimitError`, an unrecoverable error, so the chunk goes to `secondary` or backup. Applies to `buf_file`, `buf_file_single`, `buf_memory`.

`overflow_action` when the queue is full:
- `throw_exception` (default): raise and log.
- `block`: wait and retry; suited to batch jobs, not throughput.
- `drop_oldest_chunk`: purge the oldest chunk.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/buffer-section and confirmed: size defaults, chunk_full_threshold formula, compress values, decompression_size_limit, overflow_action. Removed or reworded: nothing.

Method: documentation only; no commands were run.
