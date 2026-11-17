---
id: computing-software.cloud-infrastructure-engineering.fluentd.buffer-flush-parameters
name: buffer-flush-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, buffer, flush-mode, flush-interval, flush-thread-count, flush-at-shutdown]
level: practitioner
status: docs-checked
description: "Tune when and how Fluentd flushes chunks: flush_mode, flush_interval, flush_thread_count, thread intervals, flush_at_shutdown, delayed_commit_timeout."
sources:
  - https://docs.fluentd.org/configuration/buffer-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd flush parameters
- `flush_mode`: `default` (becomes `lazy` if `time` is a chunk key, else `interval`), `lazy` (once per timekey), `interval` (every `flush_interval`), `immediate` (right after append).
- `flush_interval`: default 60s; how often to check for flushing, and not a guarantee of a flush if the mode's condition is unmet.
- `flush_thread_count`: default 1; threads writing chunks in parallel.
- `flush_thread_interval`: default 1.0s sleep when no chunks wait.
- `flush_thread_burst_interval`: default 1.0s sleep between consecutive chunk flushes.
- `flush_at_shutdown`: default false for persistent buffers such as `buf_file`, true for `buf_memory`.
- `delayed_commit_timeout`: default 60s until an async write is deemed failed.

```
<buffer>
  flush_mode interval
  flush_interval 5s
  flush_thread_count 2
</buffer>
```
Related: `buffer-size-limits-and-compression` for overflow behaviour and `buffer-retry-and-backoff` for failures.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/buffer-section and confirmed: flush_mode semantics and the flush and thread parameter defaults. Removed or reworded: nothing.

Method: documentation only; no commands were run.
