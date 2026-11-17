---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.transactional-outbox
name: transactional-outbox
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, messaging-patterns, transactional-outbox, outbox-pattern, dual-write, change-data-capture, cdc, debezium, dynamodb-streams, cosmos-change-feed, message-relay, at-least-once]
level: advanced
status: docs-checked
description: "Avoid the dual-write bug between a database and a broker: write events to an outbox in the same transaction, relay by polling or CDC, and dedupe downstream."
sources: ["https://microservices.io/patterns/data/transactional-outbox.html", "https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html", "https://learn.microsoft.com/azure/architecture/databases/guide/transactional-outbox-cosmos"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactional outbox

**Problem:** `db.commit(); broker.publish()` — a crash between them loses the event; publishing
first can emit an event for a rolled-back change.

## Steps
1. Create `outbox(id uuid pk, aggregate_type, aggregate_id, event_type, payload jsonb,
   created_at, published_at null)`.
2. In the **same DB transaction** as the business change, insert the outbox row.
3. The message relay (a separate process) sends outbox rows to the broker. Two implementations:
   - **Polling publisher**: poll unpublished rows, publish, mark them published. Simple; latency
     is at least the poll interval.
   - **Transaction log tailing (CDC)**: for example Debezium with the Outbox Event Router SMT,
     or the Cosmos DB change feed (Azure's Cosmos pattern publishes to a Service Bus topic).
     More moving parts, no polling.
4. Make consumers idempotent / deduplicate on the event `id`. Microsoft's Cosmos guide pairs the
   outbox with Service Bus duplicate detection; the relay can republish after a crash, so
   treat delivery as at-least-once.
5. Housekeeping: the Cosmos example sets a TTL on event documents for automatic cleanup; on a
   relational outbox, delete or archive published rows.

## Ordering
Messages must reach the broker in the order the service sent them, across instances updating the
same aggregate. Debezium's default outbox table has `aggregateid`, which the SMT uses as the
Kafka message key to keep order within a partition. The Cosmos example keeps events for one
entity in one logical partition and sends Service Bus messages with `SessionId` set to the
partition key so sessions preserve FIFO order.

## Gotchas
- The outbox is a table (or, in NoSQL stores, a property of each record) in the same database
  as the business data, so one local transaction covers both. Do not move it elsewhere.
- Neither 2PC nor "publish after commit" works: the first may be unsupported or undesirable, the
  second loses the event if the service crashes before sending.
- Developers can forget to write the outbox row; centralise it (the Cosmos example raises domain
  events in the repository save path).
- Debezium emits other message types (heartbeats, tombstones); apply the SMT with a predicate so it only touches outbox-table events.

## Verify
- [ ] Kill the app between commit and publish (fault injection): event still arrives.
- [ ] Roll back a transaction: no event emitted.
- [ ] Relay lag (now minus oldest unpublished created_at) is monitored and alarmed.

## Checked
2026-11-08
Method: documentation only; no commands were run.
Confirmed against microservices.io Transactional outbox, the Debezium Outbox Event Router reference and the Azure Architecture Center Transactional Outbox with Cosmos DB guide. Removed unconfirmed claims: SKIP LOCKED polling query, DynamoDB Streams and Spanner change streams as CDC options, Postgres vacuum and WAL retention/slot lag advice, and the Kafka/FIFO MessageGroupId keying statement.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.publisher-subscriber
