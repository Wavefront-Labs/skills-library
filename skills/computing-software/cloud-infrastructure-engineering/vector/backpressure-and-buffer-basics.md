---
id: computing-software.cloud-infrastructure-engineering.vector.backpressure-and-buffer-basics
name: backpressure-and-buffer-basics
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [backpressure, buffers, sinks, when-full, in-memory, capacity, vector]
level: practitioner
status: docs-checked
description: "Know how backpressure propagates from sinks to sources and where default buffers sit."
sources:
  - https://vector.dev/docs/architecture/buffering-model/
  - https://vector.dev/docs/introduction/concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Backpressure is the signal that events cannot be processed as fast as they arrive. It travels from a sink, up through transforms, back to the source and potentially to the client. How a source reacts varies: HTTP sources may reject requests with 429 (Too Many Requests), while pull-based sources such as Kafka slow down fetching.

Buffering softens this. Every component has a small in-memory channel buffer, typically 100 events, so uneven workloads keep flowing when the receiver is briefly busy. Buffering is configured on sinks because sinks are the main source of backpressure: they talk over the network, where latency and outages occur. A sink's default in-memory buffer is larger, 500 events.

Two settings control a sink buffer: the buffer type and the `when_full` action.

```yaml
sinks:
  out:
    type: console
    inputs: [in]
    encoding: {codec: json}
    buffer:
      type: memory
      max_events: 1000
      when_full: block
```

Default `when_full` is `block`, which applies backpressure to earlier components. `drop_newest` drops new events and applies no backpressure.

Decision rule: block when losing data is worse than slowing the source; drop when data is low value or senders must not wait.

Verify by pausing the downstream service in a test and watching the source slow down or reject requests.

## Checked

2026-11-03. Read architecture/buffering-model, introduction/concepts and sinks/console. Confirmed: backpressure flows sink to transforms to sources, with HTTP 429 and Kafka as the examples; the roughly 100-event channel buffer between components; the 500-event default sink buffer; `block` as the default `when_full`; `drop_newest` semantics; `encoding.codec: json` on the console sink. Removed: the `vector top` buffer-pressure verification, which the pages do not describe.

Method: documentation only; no commands were run.
