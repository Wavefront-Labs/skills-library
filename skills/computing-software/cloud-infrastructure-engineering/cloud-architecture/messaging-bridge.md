---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.messaging-bridge
name: messaging-bridge
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, messaging-bridge, enterprise-integration-patterns, message-broker, kafka-connect, amqp, hybrid-messaging]
level: practitioner
status: docs-checked
description: "Bridge two messaging systems without changing either: payload relay, shadow queues, deduplication, a bridge-specific retry policy and draining in-flight messages."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/messaging-bridge"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Messaging bridge

## When
Systems built on different messaging infrastructures (the Azure page names MSMQ, RabbitMQ, Azure Service Bus
and Amazon SQS) need to exchange messages without modifying either side, for example after mergers or when
extending on-premises systems to cloud components. Use it to integrate legacy applications, to extend
on-premises apps with cloud components, over unstable links between geo-distributed systems, or to migrate
endpoints incrementally. It beats adding HTTP endpoints, which needs code changes, retesting, hosted
endpoints and custom retry logic.
Avoid it when a system needs a feature missing from the other infrastructure, when the integration is
synchronous, or when specific security or privacy requirements apply.

## Steps
1. Add a bridge component connected to two or more messaging infrastructures at once. It pulls from one and
   pushes to the other without changing the payload. Endpoints should not be aware of the bridge.
2. Topology: either one designated bridging queue per infrastructure, or pairs of queues with a **shadow
   queue** created for each destination queue so the sender is unaware of the bridge.
3. **Delivery** is at-least-once. If a system relies on distributed transactions (such as Microsoft DTC),
   implement deduplication in the bridge.
4. **Scale** the bridge with the Competing Consumers approach when availability SLOs require it.
5. **Retry policy**: a regular consumer uses a retry counter to detect poison messages; the bridge may need a
   different policy so an infrastructure failure does not mislabel messages as poison. Consider a circuit
   breaker to pause forwarding.
6. **Migration**: keep the bridge until messages already queued on the old infrastructure, including those
   in an error queue awaiting retry, have reached the moved endpoint, not just until the last endpoint moves.
7. A system with no messaging at all can be bridged through a SQL Server emulated queue table filled using
   change data capture.

## Gotchas
- Advanced features of either technology may be unavailable on the bridged route.
- Limits differ between technologies (the page's example is a 4 MB MSMQ maximum message size against 64 KB
  for Azure Storage queues): design for the lower limit.

## Verify
- [ ] Duplicate injection shows consumers and the bridge stay correct.
- [ ] Messages queued before an endpoint moved still arrive after it moves.

## Checked
2026-11-01. Confirmed against the Azure Messaging Bridge pattern page. Removed: Kafka Connect, MirrorMaker,
RabbitMQ Shovel and Amazon MQ recommendations, the Service Bus and SQS size figures, header-mapping and
ordering rules, the loop-tagging advice and the retirement-date advice, none of which that page states. The
other cited pages were not used.
Method: documentation only; no commands were run.
