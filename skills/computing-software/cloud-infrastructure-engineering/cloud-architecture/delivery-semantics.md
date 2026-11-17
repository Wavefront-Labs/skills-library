---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.delivery-semantics
name: delivery-semantics
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, distributed-systems-design, delivery-semantics, at-least-once, at-most-once, exactly-once, effectively-once, kafka-transactions, deduplication]
level: practitioner
status: docs-checked
description: "Pick delivery semantics and build effectively-once processing: idempotent consumers, dedup windows, Kafka transactions and what exactly-once really covers."
sources: ["https://raw.githubusercontent.com/apache/kafka/trunk/docs/design/design.md", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html", "https://learn.microsoft.com/azure/service-bus-messaging/duplicate-detection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message delivery semantics

## The three (Kafka's definitions)
- **At-most-once**: messages may be lost but are never redelivered. For a consumer: save the position, then process;
  a crash in between skips messages.
- **At-least-once**: messages are never lost but may be redelivered. For a consumer: process, then save the position;
  a crash in between means the new process re-processes some messages. Kafka's default. Where messages have a primary
  key, updates are often idempotent (a repeat overwrites a record with a copy of itself).
- **Exactly-once**: each message processed once and only once. Read the fine print: claims often do not hold when
  consumers or producers fail, with multiple consumer processes, or when written data can be lost.

## What exactly-once actually covers
- **Kafka**: the idempotent producer (broker assigns a producer ID and dedupes by sequence number, since 0.11.0.0) plus
  producer transactions that atomically write output records and the consumer's offsets. Consumers need
  `isolation.level=read_committed` and `enable.auto.commit=false`; the producer sets `transactional.id`. This covers
  read-process-write between Kafka topics (Kafka Streams is the simplest route). The default isolation level is
  `read_uncommitted`. For an external destination, Kafka says exactly-once needs cooperation from that system, for
  example storing the offset alongside the output.
- **SQS FIFO**: if you retry SendMessage within the 5-minute deduplication interval, no duplicate enters the queue.
  Configure content-based deduplication (SHA-256 of the body, not the attributes) or supply a message deduplication ID.
- **Service Bus duplicate detection**: tracks the application-set `MessageId` over a window; a repeat send reports
  success but is dropped. Window defaults to 10 minutes for queues and topics (minimum 20 seconds, maximum 7 days);
  a larger window reduces throughput. Not supported on the Basic tier. With partitioning, uniqueness is
  `MessageId` plus `PartitionKey`; the docs advise against combining deduplication, batching and partitioning.
- None of these cover side effects outside the broker (database writes, emails, payments).

## Effectively-once recipe
1. At-least-once delivery.
2. Message carries a unique ID, ideally derived from the business context so a resend reproduces it (Service Bus
   suggests e.g. purchase order number plus subject) rather than a random GUID.
3. Consumer records processed IDs in the same transaction as the side effect (inbox table with a unique
   constraint), or makes the operation naturally idempotent (upsert, set state).
4. External calls use the provider's idempotency key where one exists.
5. Producer side: transactional outbox so a DB change and its event cannot diverge.

## Gotchas
- Dedup windows expire; a redelivery after the window is a duplicate again.
- "Exactly-once" marketing assumed to cover your database.

## Verify
- [ ] Kill consumer mid-processing and replay: no double side effects.

## Checked
2026-11-08. Confirmed against the Apache Kafka design documentation (Message Delivery Semantics, Using Transactions;
read from the project's docs source because kafka.apache.org returned no text), the SQS Developer Guide page on
FIFO exactly-once processing, and the Service Bus duplicate detection page. Removed as not stated there: the list of
which services default to at-least-once (SQS standard, Pub/Sub, Service Bus peek-lock), the SQS visibility-timeout
gotcha, and the claim that Service Bus dedup window is merely "configurable" (replaced with the stated default and
range). Idempotent consumer, inbox and outbox steps are design guidance, not product claims.
Method: documentation only; no commands were run.
