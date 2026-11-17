---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.competing-consumers
name: competing-consumers
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, competing-consumers, worker-pool, message-queue, at-least-once, idempotency, message-ordering, prefetch, lock-renewal, service-bus, rabbitmq, pub-sub]
level: practitioner
status: docs-checked
description: "Scale message processing with many workers reading one queue: ack semantics, prefetch, lease renewal, ordering limits, idempotent handlers and poison messages."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/competing-consumers", "https://www.rabbitmq.com/docs/consumer-prefetch", "https://cloud.google.com/pubsub/docs/lease-management"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Competing consumers

Several consumer instances receive messages from the same queue; each message is processed by one consumer
(unlike publisher-subscriber, where all consumers get every message). The queue levels load, a failed instance does
not block producers, and autoscaling can add or remove consumers as volume changes.

## Implementation checklist
1. **Complete only after success.** With Service Bus PeekLock the message is hidden from other consumers while held;
   on success the Functions runtime calls Complete, on failure it may call Abandon so another consumer can retry. If
   the function outruns the lock timeout the runtime renews the lock while it runs.
2. **Idempotent handlers**: delivery is at least once and order is not guaranteed, so a message can be processed more
   than once; design operations to be idempotent (for example by recording processed message IDs).
3. **Prefetch**: in RabbitMQ `basic.qos` limits unacknowledged messages, applied per consumer on the channel (a
   deviation from AMQP 0-9-1, where it is channel-wide); 0 means unlimited. A global per-channel limit is slower
   because of coordination. A default can be set with `default_consumer_prefetch` in the advanced config.
4. **Lease management**: Pub/Sub subscribers must ack before the deadline or extend it. The high-level client
   libraries extend automatically, by default up to an hour; configurable: maximum extension period, and minimum and
   maximum duration of each extension. A low subscription-level deadline raises duplicates; a high one delays
   redelivery of failed messages. Deadlines are not guaranteed to be respected unless exactly-once delivery is on.
5. **Poison messages**: do not let them return to the queue forever. Service Bus dead-letters a message after the
   delivery count exceeds `MaxDeliveryCount`.
6. **Ordering**: not guaranteed. Service Bus message sessions can give FIFO ordering and group messages to one
   consumer; this bounds concurrency to the number of groups.
7. **Results**: if consumers must return results, use a shared location or a reply queue with correlation to the
   original message, and signal completion.
8. **Queue as bottleneck**: at large scale, partition the messaging system or load balance across several queues.

## When not to use
Tasks that cannot be split, depend strongly on each other, must run synchronously, or must run in a fixed sequence.

## Failure modes
- Handler succeeds but the completion fails: duplicate. Idempotency fixes it, not retries.
- Hot group under ordered processing: one consumer saturated while others idle.

## Verify
- [ ] Kill a worker mid-message: another worker processes it once (check the dedupe record).
- [ ] Double the worker count: throughput scales until the downstream limit, not lower.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.queue-based-load-leveling

## Checked
2026-11-08. Confirmed against the Azure Competing Consumers pattern page (benefits, ordering, idempotency, poison
messages and MaxDeliveryCount, result handling, queue scaling, PeekLock/Complete/Abandon and lock renewal, when not
to use), the RabbitMQ Consumer Prefetch page (per-consumer semantics, 0 as unlimited, global limit cost,
`default_consumer_prefetch`), and the Pub/Sub lease management page (automatic extension up to an hour, three
configurable properties, exactly-once caveat). Removed as not stated there: SQS parameters (`MaxNumberOfMessages`,
`ChangeMessageVisibility`, `WaitTimeSeconds`), FIFO MessageGroupId, Kafka and Pub/Sub ordering key mentions,
SIGTERM and `terminationGracePeriodSeconds` shutdown advice, and the oldest-message-age scaling signal.
Method: documentation only; no commands were run.
