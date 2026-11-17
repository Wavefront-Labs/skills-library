---
id: computing-software.cloud-infrastructure-engineering.vector.runtime-and-concurrency-model
name: runtime-and-concurrency-model
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [runtime, tokio, concurrency, stateless-transforms, task-transforms, channels, vector]
level: advanced
status: docs-checked
description: "Understand how Vector maps components to async tasks and why task transforms can become bottlenecks."
sources:
  - https://vector.dev/docs/architecture/runtime-model/
  - https://vector.dev/docs/architecture/concurrency-model/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vector's runtime is futures-based and asynchronous. Nodes in the topology roughly map to async tasks that talk over channels, all scheduled by the Tokio runtime.

- **Source tasks** have an output channel.
- **Sink tasks** have an input channel and share infrastructure for streaming, batching, partitioning, networking, retries and buffers.
- **Transforms** come in two kinds. Stateless function transforms do a single operation per event without keeping state (the `remap` transform is the example) and are inlined into the source for concurrency. Task transforms may keep state across events, run as separate tasks and cannot be inlined (`dedupe` is the example).

Edges between nodes are customised channels with dynamic output control. Backpressure is the default and can be changed per sink to shed load or persist to disk.

Concurrency model: each source defines its own unit of concurrency, so scaling follows incoming volume without manual tuning. The `file` source parallelises across the files it tails; the `socket` source across open connections. Stateless transforms parallelise with it. Task transforms cannot currently be parallelised and can introduce processing bottlenecks.

## Checked

Method: docs-checked 2026-11-09 against the full Vector runtime model and concurrency model pages (raw markdown from the vectordotdev/vector repo). Dropped an unsourced design-consequence paragraph and a verification line.
