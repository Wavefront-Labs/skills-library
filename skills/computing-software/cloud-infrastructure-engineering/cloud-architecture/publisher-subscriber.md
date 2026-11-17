---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.publisher-subscriber
name: publisher-subscriber
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, publisher-subscriber, pub-sub, fan-out, sns, event-grid, service-bus-topics, subscription-filters, event-schema]
level: practitioner
status: docs-checked
description: "Decouple one event producer from many consumers via a broker: topics, content filtering, ordering and delivery caveats, schema evolution, SNS filter policies and CloudEvents."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/publisher-subscriber", "https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html", "https://cloudevents.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publisher-subscriber

A publisher sends events to an input channel; a broker or event bus copies each message to the
output channel of every interested subscriber. The sender does not know who consumes (Azure pattern page).

## Why
Direct sending forces the sender to know every consumer. A plain queue links one sender to one
consumer and has no content filtering. Pub/sub decouples subsystems, isolates faults (a failed
subscriber does not affect the publisher or other subscribers, and the broker retains messages),
supports deferred processing and cross-platform integration.

## Choosing a service (Azure page)
- Service Bus: transactions, ordering, sessions, dead-letter queues.
- Event Grid: push-delivered event notifications, e.g. Azure resource state changes.
- Event Hubs: high-throughput streaming (telemetry, logs); log-based, with consumer groups reading
  the same stream independently.
- Use an existing product rather than building one. Redis, RabbitMQ and Kafka are named as pub/sub options.

## Design points
1. **Subsets**: topics (a channel per topic) or content filtering (broker inspects content). Broad
   topics need subscriber-side filtering; narrow topics mean more topics to manage.
2. **SNS filter policy**: by default every subscriber gets every message. A JSON filter policy on
   a subscription matches message attributes or the message body (body scope requires well-formed
   JSON); non-matching messages are not sent to that subscriber.
3. **Ordering** is not guaranteed across subscribers; design for any arrival order.
4. **Delivery**: at-most-once can lose messages; at-least-once can duplicate; exactly-once adds
   overhead. Without broker dedup, make subscribers idempotent.
5. **Poison messages**: store elsewhere for analysis, e.g. a dead-letter queue.
6. **Large payloads**: store externally and send a reference (Claim Check).
7. **Schema evolution**: publishers and subscribers deploy independently; prefer backward-compatible
   changes such as optional fields; version via topic name (`orders.v1`) or a metadata field;
   subscribers ignore unknown fields.
8. **Correlation**: include a correlation ID in every message.
9. **Security**: authenticate and authorise publishers and subscribers per topic; encrypt in transit
   and, for sensitive content, at rest.
10. **Backpressure**: limit unacknowledged messages per subscriber; scale with competing consumers.
11. **Channels are unidirectional**; use request-reply for acknowledgements.
12. **CloudEvents** is a CNCF specification for describing event data in a common way so consumers
    need not write new handling logic per source.

## Not suited
Few consumers needing different data; near real-time interaction; guaranteed order; a single atomic
transaction across publisher and consumers.

## Verify
- [ ] A slow or failed subscriber does not affect others.
- [ ] Each subscriber tolerates duplicate and reordered messages.

## Checked
Confirmed against the three cited pages. Removed as not stated there: EventBridge and Kafka
specifics, schema registry advice, replay claims and the tags for those.
Method: docs-only read of cited pages, 2026-11-08
