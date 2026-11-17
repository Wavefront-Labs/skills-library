---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.priority-queue
name: priority-queue
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, priority-queue, message-priority, multiple-queues, weighted-consumers, starvation, rabbitmq-priority, service-tiers]
level: practitioner
status: docs-checked
description: "Process urgent messages first: single queue with priorities or separate queues per priority with shared or dedicated consumer pools, starvation guards, RabbitMQ priority limits."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/priority-queue", "https://www.rabbitmq.com/docs/priority"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Priority queue

Let high-priority requests be processed faster than low-priority ones, for example to honour different SLAs for
different customers. The producer assigns a priority value to each message.

## Options (Azure Architecture Center)
1. **Single queue**: every message carries a priority and the queue orders by it. Needs a broker that supports it
   (RabbitMQ does, below).
2. **Multiple queues, single consumer pool**: consumers drain the highest-priority queue first and take lower queues
   only when higher ones are empty. Simple to manage, suits similar task types, but low-priority messages can be
   delayed continually and may never be processed.
3. **Multiple queues, a pool per queue**: higher-priority queues get more consumers or higher-performance tiers. Use
   for strict independent performance requirements and fault isolation.

## Steps
- Define priorities clearly, e.g. high priority means processed within 10 seconds, and size consumers accordingly.
- Scale each consumer pool on the length of the queue it serves.
- Monitor queue depth, processing latency, delivery count and throughput per queue.
- Use dead-letter queues so a poison message after a set number of delivery attempts does not block the priority path.
- Starvation guard: dynamically raise the priority of old messages so low-priority work eventually runs.
- With multiple queues and one pool, implement preemption so high-priority queues are always serviced first.
- If bursts can exceed consumer capacity, combine with Queue-Based Load Leveling.

## RabbitMQ specifics
- Classic and quorum queues support priorities. Classic queues: declare with the `x-max-priority` argument
  (1 to 255, set by client argument, not by policy); RabbitMQ keeps a sub-queue per priority, so higher maximums use
  more CPU and memory. The docs recommend 2 to 4 (a single digit at most). Messages with no priority count as 0;
  higher than the maximum is treated as the maximum.
- Quorum queues in RabbitMQ 4.3 and later use strict priority over 32 levels (0-31), ignore `x-max-priority`, and a
  sustained stream of higher priorities can delay lower ones indefinitely. Classic queues cycle through sub-queues
  to avoid starvation. Returned (nacked) messages lose their priority in quorum queues.
- RabbitMQ lists alternatives to try first: multiple queues (such as `priority.low`, `priority.medium`,
  `priority.high`), separate channels with prefetch above 1, streams, or consumer priority.
- Prefetch defeats priority: if prefetch is full of low-priority messages, a new top-priority message waits. Use
  `basic.qos` with manual acks to limit messages out for delivery.
- With `max-length`, messages drop from the head, so higher-priority messages can be dropped for lower ones.

## Gotchas
- Strict FIFO matters more, or tasks have ordering dependencies across priorities: this pattern may not fit.
- Multiple queues can cost more where the service charges per post, retrieve or query.
- Autoscaling on total depth hides a high-priority backlog: scale each pool on its own queue.

## Verify
- [ ] Flood low with messages, then send a high one: processed within its target.
- [ ] Low tier age stays bounded under sustained high load (no starvation).

## Checked
2026-11-08. Confirmed against the Azure Priority Queue pattern page (single/multiple queue options, pool trade-offs,
starvation, age-based promotion, DLQ, monitoring, per-queue scaling, queue cost, when not to use) and the RabbitMQ
Priority Support in Queues guide (x-max-priority range and recommendation, no policy support, quorum 4.3 strict 32
levels, starvation behaviour, prefetch interaction, alternatives, max-length). Removed: the claim that SQS, Pub/Sub
and Service Bus have no per-message priority, weighted polling ratios, and server-side priority assignment advice
(neither page states them).
Method: documentation only; no commands were run.
