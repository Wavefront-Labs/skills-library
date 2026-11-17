---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.sequential-convoy
name: sequential-convoy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, sequential-convoy, ordered-processing, message-sessions, fifo-message-groups]
level: advanced
status: docs-checked
description: "Process related messages in order without losing parallelism: sequential convoy using Service Bus sessions or SQS FIFO message groups, key choice, poison messages and lock tuning."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/sequential-convoy", "https://learn.microsoft.com/azure/service-bus-messaging/message-sessions", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sequential convoy

Group related messages by a category key and process each group sequentially, one message at a time,
while different groups run in parallel. A single consumer keeps order but cannot scale; competing
consumers scale but lose per-group order (Azure pattern page).

## Choose the key
The key is the unit of parallelism (for example order ID). Too coarse (one customer for all orders)
limits parallelism; too fine gives no ordering benefit. Throughput per key is bounded by one
message's processing time.

## Azure Service Bus sessions
- Producer sets `SessionId` (AMQP group-id). A consumer accepting a session holds an exclusive
  lock; messages arrive FIFO; other consumers take other sessions.
- Basic tier has no sessions; standard and premium do. Once sessions are enabled, clients cannot
  send or receive regular messages; peeking still works.
- Sequence number alone guarantees queuing and extraction order, not processing order; sessions are
  required for ordered processing.
- Lock: release on close or expiry; renew manually or with automatic renewal. Too short a duration
  causes reprocessing; too long delays recovery from a stalled consumer.
- Session state: opaque blob, 256 KB standard, 100 MB premium; counts toward storage quota; clear
  it when done.
- An abandoned message is redelivered until `MaxDeliveryCount` (default 10), then dead-lettered
  and the receiver continues with the next session message. A dead-lettered message resubmitted
  loses its original ordering (new enqueue time and sequence number).
- If one message in a session passes its TTL, all messages in that session expire.

## Amazon SQS FIFO
- Every message needs a message group ID; order holds within a group, not across groups.
- Messages with different group IDs can be processed concurrently by different consumers.
- Once messages of a group are received, no further messages of that group are returned until
  they are deleted or become visible again (visibility timeout).
- One group ID for all messages gives strict global order. You cannot request a specific group.
- Send retries with the same deduplication ID do not duplicate or reorder.

## Design points (Azure page)
- Verify the broker supports per-group ordering; otherwise you build coordination and risk
  duplicates or misordering.
- Poison message blocks its whole session; count delivery attempts and dead-letter after a threshold.
- Producers must set the key correctly; a wrong key corrupts another group's state.
- Add sequence numbers or an end-of-sequence flag when messages can arrive out of order.
- Monitor session backlogs and dead-lettered sessions.
- Not suited to extremely high throughput (millions per minute) or when order is irrelevant
  (use competing consumers).

## Verify
- [ ] Two messages for the same key are never processed concurrently.
- [ ] A poison message ends in a dead-letter queue and the key resumes.

## Checked
Confirmed against the three cited pages. Removed the Kafka partition key claims (no Kafka page
cited) and the Kafka tag.
Method: docs-only read of cited pages, 2026-11-08
