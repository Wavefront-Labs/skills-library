---
id: computing-software.software-engineering.software-architecture.asynchronous-messaging-and-queues
name: asynchronous-messaging-and-queues
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, scalability, message-queues, asynchronous-messaging, dead-letter-queue, kafka, rabbitmq, sqs]
level: practitioner
status: draft
description: "Design asynchronous messaging with queues and topics: point-to-point vs pub/sub, delivery guarantees, idempotent consumers, ordering, DLQs, backpressure and choosing a broker."
sources:
  - https://www.enterpriseintegrationpatterns.com/patterns/messaging/
  - https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html
  - https://www.rabbitmq.com/docs/reliability
  - https://kafka.apache.org/documentation/#semantics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Asynchronous messaging and queues

Queues decouple producers from consumers in time and load: absorb spikes, keep accepting work when consumers are down, and let consumers scale independently.

## Channels (Enterprise Integration Patterns)
- **Point-to-point queue:** each message processed by one consumer among competing consumers (work distribution). SQS, RabbitMQ queues, Azure Service Bus queues.
- **Publish-subscribe topic:** each subscriber gets a copy. SNS/EventBridge, RabbitMQ fanout/topic exchanges, Kafka topics with consumer groups (each group gets all messages; partitions split work within a group).
- Messages are **commands** (do this, one handler) or **events** (this happened, any number of subscribers).

## Choosing a broker
| Need | Fit |
|---|---|
| Simple managed work queue | SQS (standard or FIFO), Azure Storage Queues, Cloud Tasks |
| Routing, priorities, per-message ack, RPC-ish patterns | RabbitMQ |
| High-throughput ordered log, replay, stream processing | Kafka, Redpanda, Kinesis, Event Hubs |
| Enterprise features (sessions, transactions, scheduled delivery) | Azure Service Bus, ActiveMQ Artemis |

## Delivery guarantees
- Assume **at-least-once**. Consumers are idempotent: dedupe on message id (processed-ids table with TTL), or make the operation naturally idempotent (upsert, set state).
- Ack after processing, not before (otherwise a crash loses the message). Kafka: commit offsets after processing; RabbitMQ: manual ack; SQS: delete after success and set visibility timeout longer than max processing time.
- "Exactly once" exists only within limited scopes (Kafka transactions read-process-write within Kafka); side effects outside still need idempotency.

## Ordering
Global ordering kills parallelism. Use per-key ordering: Kafka partition key, SQS FIFO `MessageGroupId`, Service Bus sessions. Retrying a failed message can reorder unless the consumer blocks its key.

## Failure handling
- Retry with backoff; after N attempts move to a **dead-letter queue** (SQS redrive policy `maxReceiveCount`, RabbitMQ DLX, Kafka retry/DLT topics with Spring Kafka `DefaultErrorHandler`).
- Alert on DLQ depth; build a redrive tool to replay after fixing the bug.
- Poison messages (cannot be parsed) go straight to DLQ.

## Backpressure and sizing
- Monitor queue depth and age of oldest message (SQS `ApproximateAgeOfOldestMessage`, Kafka consumer lag via Burrow or `kafka-consumer-groups --describe`); autoscale consumers on lag (KEDA).
- Bound producers when the queue cannot absorb (max length + reject/publisher confirms) rather than letting memory grow.
- Message size limits (SQS 256 KB, Kafka default 1 MB): store large payloads in object storage and send a reference (claim check).

## Verify
- [ ] Kill a consumer mid-message: message is redelivered and processed once in effect.
- [ ] Poison message lands in DLQ without blocking the queue; alert fires.
- [ ] Load test shows lag recovers after a burst within the target time.
