---
id: computing-software.cloud-infrastructure-engineering.vector.memory-and-disk-buffers
name: memory-and-disk-buffers
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [buffers, disk-buffer, memory-buffer, max-size, durability, data-dir, vector]
level: advanced
status: docs-checked
description: "Choose between in-memory and disk buffers and plan disk space and failure behaviour."
sources:
  - https://vector.dev/docs/architecture/buffering-model/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Memory buffers** are fastest but sized in events, not bytes: a 100,000-event buffer may use a few MB for small events or hundreds of MB for kilobyte-sized ones, so memory use shifts when upstream data grows. For planning, estimate an event's size as its uncompressed JSON encoding. They are not durable: a crash or host loss drops whatever is buffered. Push-based sources may not be able to resend.

**Disk buffers** persist events across restarts and crashes. They work like a write-ahead log: events are written to data files before being read out. Data is synced on an interval (500 ms by default) to balance throughput against loss risk. The maximum size is enforced strictly, but the minimum is about 256 MiB. Files are append-only logs that grow to 128 MiB and are deleted once fully processed. Events are checksummed, and on corruption Vector recovers as many events as it can decode and emits metrics.

```yaml
buffer:
  type: disk
  max_size: 1073741824
  when_full: block
```

Operator duties: keep free space on the volume holding `data_dir` for the sum of all disk buffers, and keep other processes from consuming it. On an I/O error, such as no space, Vector stops itself on purpose because it cannot know what reached disk; restart after fixing the cause.

Verify free space with `df` on the `data_dir` volume.

## Checked

2026-11-03. Read architecture/buffering-model. Confirmed: event-count sizing and the 100,000-event example, JSON-size rule of thumb, memory buffers not durable, disk buffers as a write-ahead log, 500 ms sync interval, strict maximum, roughly 256 MiB minimum, 128 MiB append-only files, checksums and recovery, forced stop on I/O error, and the free-space duty for `data_dir`. Nothing removed.

Method: documentation only; no commands were run.
