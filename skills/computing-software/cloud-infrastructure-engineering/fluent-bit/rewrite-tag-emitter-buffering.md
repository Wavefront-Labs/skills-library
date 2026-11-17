---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.rewrite-tag-emitter-buffering
name: rewrite-tag-emitter-buffering
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, rewrite-tag, emitter, emitter-mem-buf-limit, emitter-storage-type, backpressure]
level: advanced
status: docs-checked
description: "Name the rewrite_tag emitter and bound its memory or move it to filesystem buffering under backpressure."
sources: ["https://docs.fluentbit.io/manual/pipeline/filters/rewrite-tag"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rewrite tag emitter buffering

`rewrite_tag` emits new records through an internal emitter plugin. Three keys configure it:

| Key | Default | Meaning |
| --- | --- | --- |
| `emitter_name` | `emitter_for_rewrite_tag.0` in metrics | optional name of the emitter; it exposes metrics like any other component |
| `emitter_mem_buf_limit` | `10M` | memory cap when outputs apply backpressure |
| `emitter_storage.type` | `memory` | buffering for the emitted records: `memory` or `filesystem` |

When the emitter buffer exceeds `emitter_mem_buf_limit` the pipeline pauses, and stays paused until the output drains the buffer back under the limit.

If the destination for re-tagged records may face backpressure through latency or a slow network, the docs strongly recommend `emitter_storage.type: filesystem`. That needs `storage.path` in the service section.

```yaml
service:
  storage.path: /var/lib/fluent-bit/storage
pipeline:
  filters:
    - name: rewrite_tag
      match: app.*
      rule: $level ^(error)$ errors.$TAG false
      emitter_name: errors_emitter
      emitter_storage.type: filesystem
      emitter_mem_buf_limit: 20M
```

Set `emitter_name` to change the emitter's name in the metrics.

Buffering modes are explained in `computing-software.cloud-infrastructure-engineering.fluent-bit.buffering-modes`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Rewrite tag page: emitter_name, emitter_mem_buf_limit default 10M and pause behaviour, emitter_storage.type values and the strong filesystem recommendation, and the emitter_for_rewrite_tag.0 metric name. The storage.path requirement comes from the Buffering page. Removed: an unsourced verification step.

Method: documentation only; no commands were run.
