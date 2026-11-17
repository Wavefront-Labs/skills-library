---
id: computing-software.messaging-and-integration.apache-camel.seda-component
name: seda-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, seda, queue, concurrent-consumers, async]
level: practitioner
status: docs-checked
description: "Camel seda component: in-memory BlockingQueue, size 1000, concurrentConsumers, multipleConsumers, blockWhenFull, waitForTaskToComplete IfReplyExpected and discard options."
sources:
  - https://camel.apache.org/components/next/seda-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# seda:

`seda:someId[?options]`. Async via a `BlockingQueue` (default `LinkedBlockingQueue`), visible only inside one CamelContext, with no persistence if the JVM stops. Use JMS for durability, Direct for no threading.

Endpoint options (defaults):
- `size` 1000 (component `queueSize`); a custom `queue=` makes `size` unused
- `concurrentConsumers` 1; `limitConcurrentConsumers` true caps at 500
- `multipleConsumers` false (true = publish/subscribe copies; set it on every consumer)
- `pollTimeout` 1000 ms
- `blockWhenFull` false; `offerTimeout` none
- `discardWhenFull` false
- `discardIfNoConsumers` false; `failIfNoConsumers` false (only one may be on)
- `purgeWhenStopping` false
- `timeout` 30000 ms for producers awaiting async tasks (0 or less disables)
- `waitForTaskToComplete` `IfReplyExpected` (also `Always`, `Never`)
- `browseLimit` 100
- `virtualThreadPerTask` false (needs `camel.threads.virtual.enabled=true`)

Queue factories: `LinkedBlockingQueueFactory`, `ArrayBlockingQueueFactory`, `PriorityBlockingQueueFactory`.

Request-reply: the caller waits for the async route to finish and gets its result. Adding `.threads()` to a SEDA endpoint can create two blocking queues; prefer `concurrentConsumers`.

Java only: `seda.getExchanges().size()` gives queue size without JMX.

Verify: with the default `blockWhenFull=false` and `discardWhenFull=false`, sending to a full queue throws an exception stating that the queue is full; `blockWhenFull` makes the sender wait and `discardWhenFull` makes it give up and continue.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Compared against the Camel SEDA component page: every default and option listed (size and queueSize 1000, concurrentConsumers 1, limitConcurrentConsumers 500 cap, multipleConsumers, pollTimeout, blockWhenFull, offerTimeout, discard and fail options, purgeWhenStopping, timeout 30000, waitForTaskToComplete values, browseLimit 100, virtualThreadPerTask), the queue factories and the threads() warning match. The old verify line (third message with size=2) was replaced by the documented full-queue behaviour. No commands were run.
