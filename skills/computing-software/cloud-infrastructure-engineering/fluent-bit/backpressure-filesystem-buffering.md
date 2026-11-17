---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.backpressure-filesystem-buffering
name: backpressure-filesystem-buffering
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, backpressure, pause-on-chunks-overlimit, total-limit-size, filesystem-buffering, max-chunks-up]
level: advanced
status: docs-checked
description: "Bound filesystem buffering with storage.max_chunks_up, storage.pause_on_chunks_overlimit and per-output storage.total_limit_size."
sources: ["https://docs.fluentbit.io/manual/administration/backpressure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Backpressure with filesystem buffering

Three settings govern filesystem-buffered inputs.

**`storage.max_chunks_up`** (service section) is a global cap on how many filesystem-backed chunks can be `up`, mapped into memory, across all filesystem inputs. It does not limit memory-only inputs. When it is reached, filesystem inputs stop bringing new chunks up; whether they keep writing to disk depends on the next setting.

**`storage.pause_on_chunks_overlimit`** (per input):
- `off`: the input stops buffering to memory but continues buffering to the filesystem.
- `on`: the input stops both memory and filesystem buffering until memory frees up.

**`storage.total_limit_size`** (per output) limits the queued chunks for that destination. Fluent Bit keeps logical queues: a chunk, chosen by tag, may go to several destinations, and a slow destination creates backpressure. When an output reaches its limit, the oldest chunk in its queue is discarded to make room for new data.

**`storage.backlog.mem_limit`** applies only to the built-in `storage_backlog` input that promotes leftover chunks from a previous run back into memory. Hitting it does not pause regular inputs and it does not cap other inputs' memory.

**Flush requests in flight.** From v5.1.3, Fluent Bit caps concurrent flush requests: 4096 on Linux (possibly lowered at startup if the engine channel capacity is small) and 1024 elsewhere. Extra tasks wait for the next flush cycle and are not dropped; a debug line reports it. The cap is not configurable.

See `computing-software.cloud-infrastructure-engineering.fluent-bit.buffering-modes` for the modes themselves.

## Checked

2026-11-03. Confirmed on the Fluent Bit Backpressure and Buffering pages: storage.max_chunks_up, storage.pause_on_chunks_overlimit, storage.total_limit_size, storage.backlog.mem_limit, and the flush-in-flight limits (4096 Linux, 1024 elsewhere, v5.1.3, not configurable).

Method: documentation only; no commands were run.
