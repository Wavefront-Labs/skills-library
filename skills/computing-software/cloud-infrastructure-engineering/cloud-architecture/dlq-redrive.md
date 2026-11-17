---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dlq-redrive
name: dlq-redrive
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, dlq-redrive, dead-letter-queue, poison-messages, max-receive-count, redrive-policy, message-replay]
level: practitioner
status: docs-checked
description: "Run dead-letter queues properly: max delivery counts, alerting, triage, redrive to source after fixes, and DLQ settings in SQS, Service Bus, Pub/Sub and Kafka."
sources: ["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html", "https://learn.microsoft.com/azure/service-bus-messaging/service-bus-dead-letter-queues", "https://cloud.google.com/pubsub/docs/handling-failures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead-letter queue handling

## Configuration
| System | Setting |
|---|---|
| SQS | Redrive policy `maxReceiveCount` to a DLQ in the same account and Region; DLQ retention longer than source retention; built-in **DLQ redrive** (console, or API `StartMessageMoveTask` with `SourceArn`, optional `DestinationArn` and `MaxNumberOfMessagesPerSecond`) |
| Service Bus | Per-queue/subscription `$DeadLetterQueue`; MaxDeliveryCount (default 10); TTL expiry dead-lettering optional |
| Pub/Sub | Dead-letter topic with a maximum number of delivery attempts (the page gives a range starting at 5; delivery counts can reset, so redelivery can exceed it); grant the Pub/Sub service account publisher and subscriber roles after creating the topic |

## Operations
1. **Alert** on DLQ depth > 0 (or growth) routed to the owning team.
2. **Triage**: inspect message + failure reason (Service Bus DeadLetterReason, logs by message ID).
   Classify: bad data (fix/discard), bug (fix code), transient dependency outage (redrive).
3. **Redrive** after fix, at controlled rate; consumers must be idempotent.
4. **Retention**: keep DLQ messages long enough for triage. On SQS standard queues expiry counts from the original enqueue time, so set DLQ retention longer than the source queue's; on FIFO queues the timestamp resets when a message moves.
5. Discard policy documented for unfixable messages, with audit.

## Gotchas
- DLQ with no alarm = silent data loss.
- `maxReceiveCount` of 1 dead-letters on a single failed receive; set it high enough for sufficient retries.
- SQS warns that a DLQ on a FIFO queue can break message ordering.

## Checked
2026-10-28. Confirmed: SQS dead-letter queue page (redrive policy `maxReceiveCount`, same account and Region, retention rules for standard and FIFO, FIFO ordering note, alarm guidance, redrive), botocore sqs model (`StartMessageMoveTask` inputs), Service Bus DLQ page (`$deadletterqueue`, default max delivery count 10, TTL dead-lettering, dead-letter reason `MaxDeliveryCountExceeded`), Pub/Sub handling-failures page (dead-letter topic, roles, delivery-attempt caveat). Removed: Kafka and Lambda async rows, the Kafka property name, the SQS 14 day maximum and the example value 5.
Method: documentation only; no commands were run.

## Verify
- [ ] Poison message test lands in DLQ, alerts, and redrive works after fix.
