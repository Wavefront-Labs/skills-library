---
id: computing-software.data-engineering.streaming-architecture.topic-topology-and-fan-out
name: topic-topology-and-fan-out
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, topic-topology, fan-out, event-routing, topic-design, kafka, multi-event-topics]
level: advanced
status: draft
description: "Design a topic topology: one topic per event type vs per entity, fan-out and fan-in, routing/filtering layers, internal vs public topics, and naming that scales across teams."
sources:
  - https://www.confluent.io/blog/put-several-event-types-kafka-topic/
  - https://martin.kleppmann.com/2018/01/18/event-types-in-kafka-topic.html
  - https://kafka.apache.org/documentation/#design
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Topic topology and fan-out design

## Granularity: what goes in one topic
- **Ordering rule**: events that must be processed in order relative to each other must be in the same topic and partition (same key). `OrderCreated`, `OrderPaid`, `OrderShipped` for one order belong in one `orders` topic keyed by order id, not three topics (consumers cannot restore cross-topic order).
- Different entities with independent lifecycles: separate topics.
- Multiple event types in one topic require a schema strategy (Avro union with references, or `TopicRecordNameStrategy`) and consumers that ignore unknown types.
- Very different volumes/retention/compaction needs: separate topics even if related (a compacted `customer-profile` table topic vs an append-only `customer-activity` stream).

## Layers
1. **Source/raw topics**: CDC or service output, owned by the producing team; may contain internals.
2. **Public/domain topics**: curated, versioned contracts for other teams (`<domain>.<entity>.v1`). Produced from raw via a translation job (anti-corruption layer) or via outbox events designed as public contracts.
3. **Derived topics**: enriched, filtered, aggregated by stream processors; owned by the processing team.
4. **Internal topics**: repartition/changelog/DLQ, prefixed so ACLs and tooling can treat them separately.

## Fan-out
- Kafka fan-out is free on the broker side: many consumer groups read the same topic independently. Prefer "one topic, many groups" over copying data to per-consumer topics.
- Create per-consumer **filtered** topics only when consumers need a small subset and reading everything costs too much (cross-region transfer, mobile/edge consumers), or for access control (consumers not allowed to see all events). Maintain these with one routing job, not per-team copies.
- Dynamic routing (topic per tenant/customer): avoid thousands of topics. Use one topic keyed by tenant plus filtering, unless isolation/retention per tenant is a hard requirement; partition counts multiply cluster metadata.

## Fan-in
- Merging streams from several sources into one topic: all producers must agree on the key and schema; otherwise merge in a processor that normalises.
- Per-source ordering is preserved only within each key's partition.

## Naming and ownership
`<domain>.<entity-or-event>.<version>` with suffixes for derived/internal (`.dlq`, `.retry.5m`), enforced via topic-as-code and ACLs on prefixes. Record owner, schema subject, retention and consumers in a catalog.

## Evolution
- Breaking changes: new version topic (`.v2`) with a migration period where the producer (or a bridge job) writes both.
- Splitting a topic later is hard (consumers and ordering); merging is easier. Start coarser when ordering matters.

## Verify
- [ ] Each topic has an owner, a key that matches its ordering requirement, and documented consumers.
- [ ] No consumer joins two topics only to restore an order that should have been a single topic.
