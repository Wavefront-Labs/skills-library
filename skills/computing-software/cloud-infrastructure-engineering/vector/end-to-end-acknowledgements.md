---
id: computing-software.cloud-infrastructure-engineering.vector.end-to-end-acknowledgements
name: end-to-end-acknowledgements
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [acknowledgements, delivery, batch-notifier, fanout, sources, sinks, vector]
level: advanced
status: docs-checked
description: "Enable end-to-end acknowledgements so sources only confirm data after sinks have delivered it."
sources:
  - https://vector.dev/docs/architecture/end-to-end-acknowledgements/
  - https://vector.dev/docs/architecture/guarantees/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
End-to-end acknowledgements let clients verify that data reached the destination sinks. A participating source creates a batch notifier for events: one half stays with the source, the other travels with the events. When a sink processes them, the downstream response status updates the notifier. The notifier is always updated, even when events are dropped on purpose (for example by `filter`) or by mistake, and the source then propagates the status upstream: an HTTP status such as 200 vs 500, or native acknowledgement for sources like `kafka` and `aws_sqs`.

Corner cases handled by design:

- Fanout: the status is shared across copies of an event, and the worst status wins. If one of three sinks fails, the event is marked failed so it can be resent to all three.
- Merging: with `aggregate` or `reduce`, each event holds a list of source batches, and all are updated on delivery.
- Dropped by design, such as `dedupe` removing a duplicate, counts as delivered without error.

Enable it on the sink:

```yaml
sinks:
  out:
    acknowledgements:
      enabled: true
```

Not every source can acknowledge: the `socket` source cannot send a "resend" message. At startup Vector warns when an acknowledging sink consumes from a source lacking support, because silent data loss may occur.

Combine with a disk buffer: sinks with durable buffers mark events delivered once persisted.

Verify by checking startup logs for the warning.

## Checked

2026-11-03. Read architecture/end-to-end-acknowledgements and architecture/guarantees. Confirmed: the batch-notifier design, status propagation (HTTP codes, kafka and aws_sqs native acks), fanout worst-status rule, aggregate and reduce batch lists, the socket source limitation and the startup warning, and durable-buffer behaviour. Removed: the claim that it can be enabled globally (the pages only show the sink option).

Method: documentation only; no commands were run.
