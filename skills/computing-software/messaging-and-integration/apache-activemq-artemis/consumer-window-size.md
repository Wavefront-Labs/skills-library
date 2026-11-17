---
id: computing-software.messaging-and-integration.apache-activemq-artemis.consumer-window-size
name: consumer-window-size
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,consumerwindowsize,consumer-flow-control,default-consumer-window-size,slow-consumers,prefetch,activemq-artemis]
level: advanced
status: docs-checked
description: "Tune the Core consumer prefetch buffer with consumerWindowSize: 1 MiB default, -1 unbounded for fast consumers, 0 for no buffer so slow consumers don't hoard messages."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/flow-control.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer window size

**Goal:** balance throughput against fair distribution by sizing the client-side buffer of a Core consumer.

Core consumers prefetch messages into a client buffer so they avoid a network round trip per message. The maximum buffered bytes per consumer is `consumerWindowSize`, default 1 MiB (1024 * 1024) unless overridden by the `default-consumer-window-size` address-setting, which applies when the client does not set it. Values:
- `-1`: unbounded buffer.
- `0`: no buffering.
- `>0`: maximum bytes.

## Fast consumers
Use `-1` so the consumer never waits, but with caution: if it cannot keep up, client memory can overflow.

## Slow consumers
With two consumers on a queue and one slow, round-robin dispatch fills the slow one's buffer; the fast consumer drains its own and then idles while messages sit in the slow buffer. Set `consumerWindowSize=0` on the URI so messages stay on the server for other consumers. This can give deterministic distribution between consumers.

Most consumers lie in between; find the optimum by benchmarking, though 1 MiB is fine in most cases. A smaller window also minimizes messages in delivery, which helps ring queues.

```
tcp://localhost:61616?consumerWindowSize=0
```

## Checked
2026-11-03. Confirmed against the Artemis user manual pages flow-control (window-based flow control, fast and slow consumers), address-settings (default-consumer-window-size) and ring-queues (smaller consumerWindowSize). Removed: the Verify step.
Method: documentation only; no commands were run.
