---
id: computing-software.cloud-infrastructure-engineering.fluentd.performance-tuning-single-process
name: performance-tuning-single-process
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, performance-tuning, flush-thread-count, gzip-command, gc, ruby-gc-heap-oldobject-limit-factor]
level: advanced
status: docs-checked
description: "Tune a single Fluentd process: flush_thread_count, external gzip for S3/TD, keeping config simple, Ruby GC factor for memory, and when to go multi-worker."
sources:
  - https://docs.fluentd.org/deployment/performance-tuning-single-process
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd performance tuning (single process)
The page says these techniques suffice up to 5,000 messages/sec; beyond that Fluentd becomes CPU bound, so use workers (`multi-process-workers`).

- Configure the OS first (see `before-install-os-tuning`) and check `top` for the bottleneck (CPU, memory, disk I/O).
- Avoid extra computation inside Fluentd; keep the config simple.
- `flush_thread_count` (default 1) parallelises remote outputs and hides I/O or network latency, but does not speed up CPU work such as record mutation.
- Ruby's GIL means compression blocks other work. `out_s3` can compress outside the process with `store_as gzip_command`; Treasure Data uses `use_gzip_command`.
- Memory: set `RUBY_GC_HEAP_OLDOBJECT_LIMIT_FACTOR` lower than the default 2.0 for small containers, for example `1.2`. Avoid values below `1.0` without a special reason; they can degrade performance, such as delayed startup.
- Many workers for CPU-heavy loads:
```
<system>
  workers 8
</system>
```

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/deployment/performance-tuning-single-process and confirmed: 5,000 messages/sec guidance, flush_thread_count, gzip_command, RUBY_GC_HEAP_OLDOBJECT_LIMIT_FACTOR values, workers example. Removed or reworded: nothing.

Method: documentation only; no commands were run.
