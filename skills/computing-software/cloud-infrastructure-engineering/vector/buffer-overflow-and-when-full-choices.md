---
id: computing-software.cloud-infrastructure-engineering.vector.buffer-overflow-and-when-full-choices
name: buffer-overflow-and-when-full-choices
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [buffers, overflow, drop-newest, block, durability, performance, vector]
level: sme
status: docs-checked
description: "Select a when_full policy and understand why overflow topologies are not production ready."
sources:
  - https://vector.dev/docs/architecture/buffering-model/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`when_full` decides what happens when the buffer fills.

- `block` (default): wait indefinitely, giving ordered, reliable processing and backpressure upstream. May be unacceptable if clients cannot wait for Vector to accept data.
- `drop_newest`: drop the incoming event. Suits idempotent or low-value data such as debug logs, and sheds load without blocking. It is not recommended for in-memory buffers with bursty, periodic batch workloads: the buffer fills immediately and drops events even when capacity exists.
- `overflow`: chain buffers so one spills into the next. The docs warn that overflow buffers are not yet suitable for production and may lose data. There are no ordering guarantees, and the last buffer must block or drop.

```yaml
buffer:
  - type: memory
    max_events: 1000
    when_full: overflow
  - type: disk
    max_size: 1073741824
    when_full: drop_newest
```

Recommended setups from the docs:

- No storage available: use in-memory buffers (external storage buffering is not supported).
- Performance first: in-memory; raise `max_events` and keep blocking, which usually handles higher rates.
- Durability first: disk buffers; keep blocking, or drop when sources push from clients who must not wait.

Verify by pausing the downstream service in a test and watching whether the sink blocks or drops events, as `when_full` dictates.

## Checked

2026-11-03. Read architecture/buffering-model. Confirmed: `block`, `drop_newest` and `overflow` behaviour, the warning that overflow buffers are not yet suitable for production, no ordering guarantees, the last buffer must block or drop, the example topology with a 1 GiB disk buffer, and the three recommended setups including that external storage buffering is not supported. Reworded: the verification step no longer names buffer metrics.

Method: documentation only; no commands were run.
