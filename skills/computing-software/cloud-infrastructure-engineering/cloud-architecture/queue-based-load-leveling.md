---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.queue-based-load-leveling
name: queue-based-load-leveling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, queue-based-load-leveling, load-leveling, buffering, sqs, azure-service-bus, pub-sub, backpressure, queue-depth-scaling, dead-letter-queue, visibility-timeout, keda]
level: practitioner
status: docs-checked
description: "Put a queue between a bursty producer and a rate-limited consumer: bound consumer scale-out, watch depth, make consumers idempotent and dead-letter poison messages."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/queue-based-load-leveling", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue-based load leveling

**Use when** the workload has intermittent spikes that can overwhelm a downstream service, and you want to
decouple request intake from processing throughput.
**Do not use when** the caller needs a low-latency synchronous response, or volume is low and stable so the
queue adds complexity for little benefit.

## Design steps
1. **Place the queue between task and service.** Tasks post messages; the service pulls them at its own
   pace. Tasks are not delayed if the service is unavailable, and you need only enough service instances
   for average rather than peak load.
2. **Bound the consumers' aggregate downstream rate.** Autoscaling consumers without a bound only moves the
   overload to the downstream dependency. Test under load and adjust the number of queues and consumer
   instances until the leveling you need is achieved.
3. **Watch queue depth.** If the average producer rate exceeds the consumer rate, the queue keeps growing and
   latency rises: scale consumers within safe limits or shed work at the producer.
4. **Pick a durable queue.** Understand its persistence, size quotas and retention limits; for regional
   failures evaluate geo-disaster-recovery options.
5. **Make consumers idempotent.** Most queues deliver at least once.
6. **Poison messages**: route messages that cannot be processed to a dead-letter queue, monitor its depth,
   fix the cause and resubmit.
7. **Ordering**: a queue does not preserve submission order under all conditions, especially with parallel
   consumers. For strict ordering use features such as Azure Service Bus message sessions; otherwise let
   consumers accept any order.

## SQS visibility timeout
- A received message stays in the queue but is invisible to other consumers for the visibility timeout; the
  queue default is 30 seconds. Delete the message before it expires or it becomes visible again.
- `ChangeMessageVisibility` extends or shortens the timeout per message. The maximum is 12 hours from first
  receipt, and extending does not reset that limit.
- Delivery is at least once, so the timeout does not guarantee a message is never delivered twice.
- Set the timeout to the maximum time your app normally needs to process and delete a message; too high
  delays retries of unprocessed messages. Configure a dead-letter queue for repeated failures.
- FIFO queues process messages with the same message group ID in strict sequence.

## Gotchas
- A queue is one-way: if the task expects a reply, you need a separate response mechanism.
- Services that throttle at a threshold are better protected by leveling than by relying on their throttle.

## Verify
- [ ] Load test a burst: downstream request rate stays within its limit and the queue drains.
- [ ] A malformed message lands in the dead-letter queue and someone is alerted.
- [ ] Consumers handle a duplicate delivery without side effects.

## Checked
2026-11-01. Confirmed against the Azure Queue-Based Load Leveling pattern page (bounded consumers, depth,
durability, at-least-once, dead-letter, ordering) and the SQS visibility timeout page (30 s default, 12 h
limit, ChangeMessageVisibility, FIFO groups). Removed: the SQS/Pub/Sub retention figures, metric names,
the 6x p99 rule, the SQS FIFO throughput figure, KEDA scaler names and the invented sizing formulas, none
of which those pages state.
Method: documentation only; no commands were run.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.competing-consumers
